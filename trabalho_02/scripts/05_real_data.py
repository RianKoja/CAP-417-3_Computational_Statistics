"""
Script 05: Real Data — GARCH Fit for Financial Stocks
Reproduces the GARCH exercise from references/list2_rian_errata.pdf.
Adds a Normal vs. Student-t distribution comparison for GARCH(1,1).
Outputs: figures/05_returns.svg
         figures/05_volatility.svg
         figures/05_qq.svg
         figures/05_qq_t.svg
         figures/05_dist_comparison.svg
         figures/05_acf.svg
         sections/05_garch_params.csv
         sections/05_aic_bic.csv
         sections/05_dist_comparison.csv
"""
from pathlib import Path
import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import csv

HERE = Path(__file__).parent
FIGURES = HERE.parent / "figures"
SECTIONS = HERE.parent / "sections"
FIGURES.mkdir(exist_ok=True)
SECTIONS.mkdir(exist_ok=True)

# ── data download ─────────────────────────────────────────────────────────────
import yfinance as yf
from arch import arch_model
from scipy import stats

TICKERS = {"PETR4.SA": "Petrobras", "VALE3.SA": "Vale", "^BVSP": "Ibovespa", "SPY": "S&P 500"}
START, END = "2019-01-01", "2024-12-31"

print("Downloading data...")
raw = yf.download(list(TICKERS.keys()), start=START, end=END,
                  auto_adjust=True, progress=False)["Close"]
raw.columns = [TICKERS[t] for t in raw.columns]
raw = raw.dropna()

log_returns = np.log(raw / raw.shift(1)).dropna() * 100   # in %
print(f"Data shape: {log_returns.shape}  ({log_returns.index[0].date()} → {log_returns.index[-1].date()})")

# ── Figure 1: return series ───────────────────────────────────────────────────
fig, axes = plt.subplots(2, 2, figsize=(12, 6), sharex=True)
fig.suptitle("Daily Log-Returns (%)", fontsize=13)
for ax, col in zip(axes.flat, log_returns.columns):
    ax.plot(log_returns.index, log_returns[col], linewidth=0.6, color="#555")
    ax.axhline(0, color="red", linewidth=0.8, linestyle="--")
    ax.set_title(col, fontsize=10)
    ax.set_ylabel("Return (%)", fontsize=8)
    ax.grid(True, alpha=0.25)
plt.tight_layout()
fig.savefig(FIGURES / "05_returns.svg", format="svg", bbox_inches="tight")
print(f"Saved {FIGURES / '05_returns.svg'}")
plt.close()

# ── Linear regression: r_t on r_{t-1} (baseline) ─────────────────────────────
lin_results = {}
fig, axes = plt.subplots(2, 2, figsize=(10, 8))
fig.suptitle(r"Linear Regression: $r_t$ on $r_{t-1}$", fontsize=12)
for ax, col in zip(axes.flat, log_returns.columns):
    r = log_returns[col].values
    x_, y_ = r[:-1], r[1:]
    slope, intercept, r_val, p_val, _ = stats.linregress(x_, y_)
    ax.scatter(x_, y_, s=4, alpha=0.35, color="#555")
    xp = np.linspace(x_.min(), x_.max(), 200)
    ax.plot(xp, slope * xp + intercept, color="#e74c3c", linewidth=1.8,
            label=f"$\\hat{{a}}={slope:.3f}$, $R^2={r_val**2:.3f}$")
    ax.set_title(col, fontsize=10)
    ax.set_xlabel("$r_{t-1}$", fontsize=9)
    ax.set_ylabel("$r_t$", fontsize=9)
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.2)
    lin_results[col] = {"slope": slope, "intercept": intercept, "r2": r_val**2}
plt.tight_layout()
fig.savefig(FIGURES / "05_linear_fit.svg", format="svg", bbox_inches="tight")
print(f"Saved {FIGURES / '05_linear_fit.svg'}")
plt.close()

# ── GARCH fitting — Normal distribution ───────────────────────────────────────
garch_specs = [
    ("GARCH(1,1)", 1, 1),
    ("GARCH(2,1)", 2, 1),
    ("GARCH(1,2)", 1, 2),
]

garch_params_rows = []
aic_bic_rows = []

# For volatility and QQ plots:
fitted_models = {}   # col -> GARCH(1,1) Normal result

for col in log_returns.columns:
    r = log_returns[col].dropna().values
    print(f"\nFitting GARCH models for {col}...")

    aic_row = {"ticker": col}
    for spec_name, p, q in garch_specs:
        try:
            am = arch_model(r, vol="Garch", p=p, q=q, dist="normal")
            res = am.fit(disp="off")
            aic_row[f"{spec_name}_AIC"] = round(res.aic, 2)
            aic_row[f"{spec_name}_BIC"] = round(res.bic, 2)
            print(f"  {spec_name}: AIC={res.aic:.2f}, BIC={res.bic:.2f}")

            if spec_name == "GARCH(1,1)":
                fitted_models[col] = res
                params = res.params
                garch_params_rows.append({
                    "ticker": col,
                    "omega": round(params.get("omega", np.nan), 5),
                    "alpha[1]": round(params.get("alpha[1]", np.nan), 5),
                    "beta[1]": round(params.get("beta[1]", np.nan), 5),
                    "persistence": round(
                        params.get("alpha[1]", 0) + params.get("beta[1]", 0), 5),
                    "AIC": round(res.aic, 2),
                    "BIC": round(res.bic, 2),
                })
        except Exception as e:
            print(f"  {spec_name} failed: {e}")

    aic_bic_rows.append(aic_row)

# ── GARCH(1,1) — Student-t distribution (new) ─────────────────────────────────
fitted_models_t = {}   # col -> GARCH(1,1) Student-t result
dist_comparison_rows = []

print("\n--- Fitting GARCH(1,1) Normal vs. Student-t ---")
for col in log_returns.columns:
    r = log_returns[col].dropna().values
    row = {"ticker": col}
    try:
        # Normal
        res_n = fitted_models[col]
        row["normal_AIC"] = round(res_n.aic, 2)
        row["normal_BIC"] = round(res_n.bic, 2)

        # Student-t
        am_t = arch_model(r, vol="Garch", p=1, q=1, dist="t")
        res_t = am_t.fit(disp="off")
        fitted_models_t[col] = res_t
        nu = res_t.params.get("nu", np.nan)
        row["t_AIC"] = round(res_t.aic, 2)
        row["t_BIC"] = round(res_t.bic, 2)
        row["nu"] = round(nu, 2)
        print(f"  {col}: Normal AIC={row['normal_AIC']}, t AIC={row['t_AIC']}  (nu={nu:.2f})")
    except Exception as e:
        print(f"  {col} t-fit failed: {e}")
        row.setdefault("t_AIC", "—")
        row.setdefault("t_BIC", "—")
        row.setdefault("nu", "—")
    dist_comparison_rows.append(row)

# ── Figure 3: conditional volatility ─────────────────────────────────────────
fig, axes = plt.subplots(2, 2, figsize=(12, 7), sharex=False)
fig.suptitle("GARCH(1,1) — Conditional Volatility $\\hat{\\sigma}_t$", fontsize=12)
for ax, col in zip(axes.flat, log_returns.columns):
    res = fitted_models.get(col)
    if res is None:
        continue
    cond_vol = res.conditional_volatility
    dates = log_returns[col].dropna().index[-len(cond_vol):]
    ax.plot(dates, log_returns[col].dropna().values[-len(cond_vol):],
            color="#aaa", linewidth=0.5, alpha=0.7, label="Returns")
    ax.plot(dates, cond_vol, color="#e74c3c", linewidth=1.2, label="$\\hat{\\sigma}_t$")
    ax.plot(dates, -cond_vol, color="#e74c3c", linewidth=1.2)
    ax.set_title(col, fontsize=10)
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.2)
plt.tight_layout()
fig.savefig(FIGURES / "05_volatility.svg", format="svg", bbox_inches="tight")
print(f"\nSaved {FIGURES / '05_volatility.svg'}")
plt.close()

# ── Figure 4: Q-Q plots — Normal GARCH residuals vs Normal ───────────────────
fig, axes = plt.subplots(2, 2, figsize=(10, 8))
fig.suptitle("Q-Q Plot of GARCH(1,1)-Normal Standardised Residuals\nvs. Normal Distribution",
             fontsize=11)
for ax, col in zip(axes.flat, log_returns.columns):
    res = fitted_models.get(col)
    if res is None:
        continue
    std_resid = res.std_resid
    (osm, osr), (slope, intercept, r2) = stats.probplot(std_resid, dist="norm")
    ax.plot(osm, osr, ".", markersize=3, alpha=0.5, color="#555")
    ax.plot(osm, slope * np.array(osm) + intercept, "r-", linewidth=1.5)
    ax.set_title(col, fontsize=10)
    ax.set_xlabel("Normal quantiles", fontsize=8)
    ax.set_ylabel("Sample quantiles", fontsize=8)
    ax.grid(True, alpha=0.2)
plt.tight_layout()
fig.savefig(FIGURES / "05_qq.svg", format="svg", bbox_inches="tight")
print(f"Saved {FIGURES / '05_qq.svg'}")
plt.close()

# ── Figure 4b: Q-Q plots — Student-t GARCH residuals vs t(nu) ────────────────
fig, axes = plt.subplots(2, 2, figsize=(10, 8))
fig.suptitle("Q-Q Plot of GARCH(1,1)-t Standardised Residuals\nvs. Student-t Distribution",
             fontsize=11)
for ax, col in zip(axes.flat, log_returns.columns):
    res_t = fitted_models_t.get(col)
    if res_t is None:
        continue
    std_resid = res_t.std_resid
    nu = res_t.params.get("nu", 5.0)
    (osm, osr), (slope, intercept, r2) = stats.probplot(std_resid, dist="t",
                                                         sparams=(nu,))
    ax.plot(osm, osr, ".", markersize=3, alpha=0.5, color="#3498db")
    ax.plot(osm, slope * np.array(osm) + intercept, "r-", linewidth=1.5)
    ax.set_title(f"{col}  ($\\nu={nu:.1f}$)", fontsize=10)
    ax.set_xlabel(f"t({nu:.1f}) quantiles", fontsize=8)
    ax.set_ylabel("Sample quantiles", fontsize=8)
    ax.grid(True, alpha=0.2)
plt.tight_layout()
fig.savefig(FIGURES / "05_qq_t.svg", format="svg", bbox_inches="tight")
print(f"Saved {FIGURES / '05_qq_t.svg'}")
plt.close()

# ── Figure 6: side-by-side QQ comparison for one asset (Petrobras) ───────────
col_demo = "Petrobras"
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.5))
fig.suptitle(f"Distribution Comparison — {col_demo}: GARCH(1,1)-Normal vs. GARCH(1,1)-t",
             fontsize=11)

res_n = fitted_models.get(col_demo)
res_t = fitted_models_t.get(col_demo)

if res_n and res_t:
    # Normal residuals vs Normal
    sr_n = res_n.std_resid
    (osm, osr), (s, ic, _) = stats.probplot(sr_n, dist="norm")
    ax1.plot(osm, osr, ".", markersize=4, alpha=0.5, color="#555")
    ax1.plot(osm, s * np.array(osm) + ic, "r-", linewidth=1.8)
    ax1.set_title("GARCH-Normal: residuals vs. $\\mathcal{N}(0,1)$", fontsize=10)
    ax1.set_xlabel("Normal quantiles", fontsize=9)
    ax1.set_ylabel("Sample quantiles", fontsize=9)
    ax1.grid(True, alpha=0.2)

    # t residuals vs t(nu)
    sr_t = res_t.std_resid
    nu = res_t.params.get("nu", 5.0)
    (osm2, osr2), (s2, ic2, _) = stats.probplot(sr_t, dist="t", sparams=(nu,))
    ax2.plot(osm2, osr2, ".", markersize=4, alpha=0.5, color="#3498db")
    ax2.plot(osm2, s2 * np.array(osm2) + ic2, "r-", linewidth=1.8)
    ax2.set_title(f"GARCH-t: residuals vs. $t({nu:.1f})$", fontsize=10)
    ax2.set_xlabel(f"t({nu:.1f}) quantiles", fontsize=9)
    ax2.set_ylabel("Sample quantiles", fontsize=9)
    ax2.grid(True, alpha=0.2)

plt.tight_layout()
fig.savefig(FIGURES / "05_dist_comparison.svg", format="svg", bbox_inches="tight")
print(f"Saved {FIGURES / '05_dist_comparison.svg'}")
plt.close()

# ── Figure 5: ACF of squared returns before/after GARCH ─────────────────────
from statsmodels.graphics.tsaplots import plot_acf

fig, axes = plt.subplots(2, 4, figsize=(14, 6))
fig.suptitle("ACF of Squared Returns: Before vs. After GARCH(1,1)", fontsize=11)
for col_idx, col in enumerate(log_returns.columns):
    res = fitted_models.get(col)
    if res is None:
        continue
    r = log_returns[col].dropna().values
    std_resid = res.std_resid

    ax_raw = axes[0, col_idx]
    plot_acf(r ** 2, lags=30, ax=ax_raw, title=f"{col} — Raw $r_t^2$",
             alpha=0.05, zero=False)
    ax_raw.set_xlabel("")

    ax_fit = axes[1, col_idx]
    plot_acf(std_resid ** 2, lags=30, ax=ax_fit, title=f"{col} — Std Residuals$^2$",
             alpha=0.05, zero=False)

plt.tight_layout()
fig.savefig(FIGURES / "05_acf.svg", format="svg", bbox_inches="tight")
print(f"Saved {FIGURES / '05_acf.svg'}")
plt.close()

# ── save CSVs ─────────────────────────────────────────────────────────────────
with open(SECTIONS / "05_garch_params.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=garch_params_rows[0].keys())
    w.writeheader()
    w.writerows(garch_params_rows)
print(f"Saved sections/05_garch_params.csv")

with open(SECTIONS / "05_aic_bic.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=aic_bic_rows[0].keys())
    w.writeheader()
    w.writerows(aic_bic_rows)
print(f"Saved sections/05_aic_bic.csv")

with open(SECTIONS / "05_dist_comparison.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=dist_comparison_rows[0].keys())
    w.writeheader()
    w.writerows(dist_comparison_rows)
print(f"Saved sections/05_dist_comparison.csv")

print("\nDone.")
