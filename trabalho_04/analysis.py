"""
Analysis of the CongNaMul Soybean Sprout dataset.
Focuses on physical feature data (no image processing).
Outputs figures to figs/ directory.
"""

import json
import re
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats
import statsmodels.api as sm
from statsmodels.stats.diagnostic import het_breuschpagan
from sklearn.linear_model import RANSACRegressor, LinearRegression

# ── Paths ───────────────────────────────────────────────────────────────────
DATA_PATH = Path.home() / ".cache/kagglehub/datasets/byunghyunban/congnamul/versions/1"
JSON_PATH = DATA_PATH / "Semantic Segmentation Dataset/Single Sample/3024_3024/single_sample_physical_features.json"
FIGS_DIR = Path("figs")
FIGS_DIR.mkdir(exist_ok=True)

plt.rcParams.update({"font.family": "serif", "axes.spines.top": False, "axes.spines.right": False})

FEATURES = ["length_head", "length_body", "thickness_body", "length_tail"]
LABELS = {
    "length_head":    "Head Length (mm)",
    "length_body":    "Body Length (mm)",
    "thickness_body": "Body Thickness (mm)",
    "length_tail":    "Tail Length (mm)",
    "weight":         "Weight (mg)",
}

# ── Load, deduplicate, clean ─────────────────────────────────────────────────
def load_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    with open(JSON_PATH) as f:
        raw = json.load(f)

    rows, seen = [], set()
    for fname, vals in raw.items():
        m = re.match(r"(.+)_(\d+)\.jpg", fname)
        if not m:
            continue
        sid = int(m.group(2))
        if sid in seen:
            continue
        seen.add(sid)
        rows.append({"id": sid, **vals})

    df = pd.DataFrame(rows).sort_values("id").reset_index(drop=True)

    # Remove obvious measurement errors (3× IQR fence)
    for col in FEATURES:
        q1, q3 = df[col].quantile(0.25), df[col].quantile(0.75)
        iqr = q3 - q1
        before = len(df)
        df = df[(df[col] >= q1 - 3 * iqr) & (df[col] <= q3 + 3 * iqr)]
        if len(df) < before:
            print(f"Removed {before - len(df)} outlier(s) from {col}")

    df = df.reset_index(drop=True)
    df_w = df[df["weight"] != -1].copy().reset_index(drop=True)
    return df, df_w


# ── Figure 1: Distributions ──────────────────────────────────────────────────
def fig_distributions(df: pd.DataFrame) -> None:
    fig, axes = plt.subplots(2, 2, figsize=(8, 5.5))
    axes = axes.ravel()
    for ax, feat in zip(axes, FEATURES):
        x = df[feat].dropna()
        ax.hist(x, bins=25, density=True, alpha=0.5, color="#4878CF", edgecolor="white", linewidth=0.4)
        kde_x = np.linspace(x.min(), x.max(), 300)
        ax.plot(kde_x, stats.gaussian_kde(x)(kde_x), color="#4878CF", lw=2)
        mu, sigma = x.mean(), x.std()
        ax.plot(kde_x, stats.norm.pdf(kde_x, mu, sigma), "k--", lw=1.2,
                label=f"N({mu:.1f}, {sigma:.1f}²)")
        ax.set_xlabel(LABELS[feat], fontsize=9)
        ax.set_ylabel("Density", fontsize=9)
        ax.legend(fontsize=7, frameon=False)
    fig.suptitle(f"Morphological Feature Distributions (n = {len(df)})", fontsize=11)
    fig.tight_layout()
    fig.savefig(FIGS_DIR / "fig1_distributions.svg", bbox_inches="tight")
    plt.close(fig)
    print("Saved fig1_distributions.svg")


# ── Figure 2: Q-Q plots ──────────────────────────────────────────────────────
def fig_qqplots(df: pd.DataFrame) -> None:
    fig, axes = plt.subplots(2, 2, figsize=(8, 5.5))
    axes = axes.ravel()
    for ax, feat in zip(axes, FEATURES):
        x = df[feat].dropna().values
        (osm, osr), (slope, intercept, _) = stats.probplot(x, dist="norm")
        ax.scatter(osm, osr, s=12, alpha=0.6, color="#4878CF")
        ax.plot(osm, slope * np.array(osm) + intercept, "k--", lw=1.2)
        _, sw_p = stats.shapiro(x)
        ks_stat, ks_p = stats.kstest(x, "norm", args=(x.mean(), x.std(ddof=1)))
        ax.set_title(
            f"{LABELS[feat]}\nS-W p={sw_p:.3f}   K-S p={ks_p:.3f}",
            fontsize=8,
        )
        ax.set_xlabel("Theoretical quantiles", fontsize=8)
        ax.set_ylabel("Sample quantiles", fontsize=8)
    fig.suptitle("Normal Q-Q Plots with Normality Test p-values", fontsize=11)
    fig.tight_layout()
    fig.savefig(FIGS_DIR / "fig2_qqplots.svg", bbox_inches="tight")
    plt.close(fig)
    print("Saved fig2_qqplots.svg")


# ── Figure 3: Correlation heatmap ────────────────────────────────────────────
def fig_correlation(df_w: pd.DataFrame) -> None:
    cols = FEATURES + ["weight"]
    sub = df_w[cols].rename(columns=LABELS)

    fig, ax = plt.subplots(figsize=(5.5, 4.5))
    corr = sub.corr()
    mask = np.triu(np.ones_like(corr, dtype=bool))
    sns.heatmap(corr, mask=mask, annot=True, fmt=".2f", cmap="RdBu_r", center=0,
                vmin=-1, vmax=1, ax=ax, square=True,
                annot_kws={"size": 9}, linewidths=0.5)
    ax.set_title(f"Pearson Correlations (n = {len(df_w)})", fontsize=10)
    ax.tick_params(labelsize=8)
    fig.tight_layout()
    fig.savefig(FIGS_DIR / "fig3_correlation.svg", bbox_inches="tight")
    plt.close(fig)
    print("Saved fig3_correlation.svg")


# ── Figure 4: OLS vs RANSAC — fitted vs actual with inlier/outlier marking ──
def fig_ransac(df_w: pd.DataFrame) -> dict:
    X = df_w[FEATURES].values
    y = df_w["weight"].values

    # OLS
    ols = LinearRegression().fit(X, y)
    y_ols = ols.predict(X)

    # RANSAC
    ransac = RANSACRegressor(
        estimator=LinearRegression(),
        min_samples=0.5,
        residual_threshold=None,   # MAD-based automatic threshold
        random_state=42,
        max_trials=500,
    )
    ransac.fit(X, y)
    y_ransac = ransac.predict(X)
    inlier_mask = ransac.inlier_mask_
    outlier_mask = ~inlier_mask

    # R² values
    ss_tot = np.sum((y - y.mean()) ** 2)
    r2_ols = 1 - np.sum((y - y_ols) ** 2) / ss_tot
    r2_ransac_all = 1 - np.sum((y - y_ransac) ** 2) / ss_tot
    r2_ransac_in = 1 - np.sum((y[inlier_mask] - y_ransac[inlier_mask]) ** 2) / np.sum(
        (y[inlier_mask] - y[inlier_mask].mean()) ** 2
    )

    fig, axes = plt.subplots(1, 2, figsize=(10, 4.5))

    # Panel A: OLS fitted vs actual
    ax = axes[0]
    ax.scatter(y_ols, y, s=18, alpha=0.6, color="#4878CF")
    lims = [min(y_ols.min(), y.min()) - 0.02, max(y_ols.max(), y.max()) + 0.02]
    ax.plot(lims, lims, "k--", lw=1.2, label=f"OLS  R²={r2_ols:.3f}")
    ax.set_xlabel("Fitted weight (mg)", fontsize=9)
    ax.set_ylabel("Actual weight (mg)", fontsize=9)
    ax.set_title("OLS: Fitted vs Actual", fontsize=10)
    ax.legend(fontsize=8, frameon=False)
    ax.set_xlim(lims); ax.set_ylim(lims)

    # Panel B: RANSAC fitted vs actual — colour by inlier/outlier
    ax = axes[1]
    ax.scatter(y_ransac[inlier_mask], y[inlier_mask],
               s=18, alpha=0.65, color="#4878CF", label=f"Inliers (n={inlier_mask.sum()})")
    ax.scatter(y_ransac[outlier_mask], y[outlier_mask],
               s=30, alpha=0.75, color="#E84A5F", marker="x",
               label=f"Outliers (n={outlier_mask.sum()})")
    ax.plot(lims, lims, "k--", lw=1.2,
            label=f"RANSAC  R²(inliers)={r2_ransac_in:.3f}")
    ax.set_xlabel("Fitted weight (mg)", fontsize=9)
    ax.set_ylabel("Actual weight (mg)", fontsize=9)
    ax.set_title("RANSAC: Fitted vs Actual", fontsize=10)
    ax.legend(fontsize=8, frameon=False)
    ax.set_xlim(lims); ax.set_ylim(lims)

    fig.tight_layout()
    fig.savefig(FIGS_DIR / "fig4_ransac.svg", bbox_inches="tight")
    plt.close(fig)
    print("Saved fig4_ransac.svg")

    return {
        "ols": ols, "ransac": ransac,
        "r2_ols": r2_ols,
        "r2_ransac_all": r2_ransac_all,
        "r2_ransac_inliers": r2_ransac_in,
        "n_inliers": inlier_mask.sum(),
        "n_outliers": outlier_mask.sum(),
        "inlier_mask": inlier_mask,
    }


# ── Print summaries ──────────────────────────────────────────────────────────
def print_summaries(df: pd.DataFrame, df_w: pd.DataFrame, ransac_results: dict) -> None:
    print(f"\n=== DESCRIPTIVE STATISTICS (n={len(df)}) ===")
    rows = []
    for feat in FEATURES:
        x = df[feat].dropna()
        rows.append({
            "feature": feat,
            "mean": x.mean(), "sd": x.std(),
            "median": x.median(),
            "skewness": stats.skew(x),
            # scipy kurtosis default: Fisher (excess) definition → Normal = 0
            "excess_kurtosis": stats.kurtosis(x, fisher=True),
        })
    desc = pd.DataFrame(rows).set_index("feature")
    print(desc.to_string(float_format="{:.4f}".format))

    print("\n(Note: excess kurtosis = Pearson kurtosis − 3; Normal distribution has excess kurtosis = 0)")

    print("\n=== NORMALITY TESTS ===")
    print(f"{'Feature':20s}  {'S-W W':>8}  {'S-W p':>8}  {'K-S D':>8}  {'K-S p':>8}")
    for feat in FEATURES:
        x = df[feat].dropna().values
        sw_stat, sw_p = stats.shapiro(x)
        ks_stat, ks_p = stats.kstest(x, "norm", args=(x.mean(), x.std(ddof=1)))
        print(f"{feat:20s}  {sw_stat:8.4f}  {sw_p:8.4f}  {ks_stat:8.4f}  {ks_p:8.4f}")

    print(f"\n=== PEARSON CORRELATIONS WITH WEIGHT (n={len(df_w)}) ===")
    for feat in FEATURES:
        r, p = stats.pearsonr(df_w[feat], df_w["weight"])
        print(f"  {feat:20s}: r={r:.4f}, p={p:.4f}")

    print("\n=== OLS REGRESSION ===")
    X_sm = sm.add_constant(df_w[FEATURES])
    model = sm.OLS(df_w["weight"], X_sm).fit()
    print(model.summary())
    bp_stat, bp_p, _, _ = het_breuschpagan(model.resid, model.model.exog)
    print(f"Breusch-Pagan: stat={bp_stat:.4f}, p={bp_p:.4f}")

    print("\n=== RANSAC REGRESSION ===")
    ransac = ransac_results["ransac"]
    print(f"  Inliers : {ransac_results['n_inliers']}")
    print(f"  Outliers: {ransac_results['n_outliers']}")
    print(f"  R² (OLS, all):          {ransac_results['r2_ols']:.4f}")
    print(f"  R² (RANSAC, all):       {ransac_results['r2_ransac_all']:.4f}")
    print(f"  R² (RANSAC, inliers):   {ransac_results['r2_ransac_inliers']:.4f}")
    coefs = dict(zip(FEATURES, ransac.estimator_.coef_))
    print(f"  Intercept: {ransac.estimator_.intercept_:.4f}")
    for feat, c in coefs.items():
        print(f"  {feat:20s}: {c:.6f}")


def main():
    df, df_w = load_data()
    print(f"Unique sprouts after cleaning: {len(df)}")
    print(f"Sprouts with weight data:      {len(df_w)}")

    fig_distributions(df)
    fig_qqplots(df)
    fig_correlation(df_w)
    ransac_results = fig_ransac(df_w)
    print_summaries(df, df_w, ransac_results)


if __name__ == "__main__":
    main()
