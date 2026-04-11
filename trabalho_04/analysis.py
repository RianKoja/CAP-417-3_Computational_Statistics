"""
Analysis of the CongNaMul Soybean Sprout dataset.
Focuses on physical feature data (no image processing).
Outputs figures to figs/ and computed results to outputs/.
"""

import json
import re
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pypst
import seaborn as sns
from scipy import stats
import statsmodels.api as sm
from statsmodels.stats.diagnostic import het_breuschpagan
from sklearn.linear_model import RANSACRegressor, LinearRegression

# -- Configuration --
REMOVE_OUTLIERS = True

# ── Paths ───────────────────────────────────────────────────────────────────
DATA_PATH = Path.home() / ".cache/kagglehub/datasets/byunghyunban/congnamul/versions/1"
JSON_PATH = DATA_PATH / "Semantic Segmentation Dataset/Single Sample/3024_3024/single_sample_physical_features.json"
FIGS_DIR = Path("figs")
OUTPUTS_DIR = Path("outputs")
FIGS_DIR.mkdir(exist_ok=True)
OUTPUTS_DIR.mkdir(exist_ok=True)

plt.rcParams.update({"font.family": "serif", "axes.spines.top": False, "axes.spines.right": False})

FEATURES = ["length_head", "length_body", "thickness_body", "length_tail"]
LABELS = {
    "length_head":    "Head Length (mm)",
    "length_body":    "Body Length (mm)",
    "thickness_body": "Body Thickness (mm)",
    "length_tail":    "Tail Length (mm)",
    "weight":         "Weight (mg)",
}
SHORT_LABELS = {
    "length_head":    "Head length",
    "length_body":    "Body length",
    "thickness_body": "Body thickness",
    "length_tail":    "Tail length",
    "weight":         "Weight",
}


# ── Helpers ──────────────────────────────────────────────────────────────────
def fmt_p(p: float) -> str:
    """Format a p-value; bold (Typst markup) if significant at α = 0.05."""
    if p < 0.001:
        return "*< 0.001*"
    if p < 0.05:
        return f"*{p:.3f}*"
    return f"{p:.3f}"


def make_booktabs_table(df: pd.DataFrame) -> pypst.Table:
    """Return a styled pypst Table with booktabs-style hlines."""
    n_data = len(df)
    n_cols = len(df.columns)
    align_str = "(left, " + ", ".join(["center"] * n_cols) + ")"

    t = pypst.Table.from_dataframe(df)
    t.stroke = "none"
    t.align = align_str
    t.add_hline(0, stroke="0.8pt")
    t.add_hline(1, stroke="0.4pt")
    t.add_hline(n_data + 1, stroke="0.8pt")
    return t


def write_toml(sections: dict, path: Path) -> None:
    """Write a simple nested TOML file (one level of sections)."""
    lines = []
    for section, values in sections.items():
        lines.append(f"[{section}]")
        for key, value in values.items():
            if isinstance(value, str):
                val_esc = value.replace('\\', r'\\').replace('"', r'\"')
                lines.append(f'{key} = "{val_esc}"')
            elif isinstance(value, bool):
                lines.append(f'{key} = {"true" if value else "false"}')
            else:
                lines.append(f"{key} = {value}")
        lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


# ── Load, deduplicate, clean ──────────────────────────────────────────────────
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

    if REMOVE_OUTLIERS:
        mask = pd.Series(True, index=df.index)
        for col in FEATURES:
            q1, q3 = df[col].quantile(0.25), df[col].quantile(0.75)
            iqr = q3 - q1
            mask &= df[col].between(q1 - 3 * iqr, q3 + 3 * iqr)
        df = df[mask]

    df = df.reset_index(drop=True)
    df_w = df[df["weight"] != -1].copy().reset_index(drop=True)
    return df, df_w


# ── Figures ───────────────────────────────────────────────────────────────────
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


def fig_weight_distribution(df_w: pd.DataFrame) -> None:
    x = df_w["weight"].dropna()
    fig, ax = plt.subplots(figsize=(5.5, 3.5))
    ax.hist(x, bins=25, density=True, alpha=0.5, color="#4878CF", edgecolor="white", linewidth=0.4)
    kde_x = np.linspace(x.min(), x.max(), 300)
    ax.plot(kde_x, stats.gaussian_kde(x)(kde_x), color="#4878CF", lw=2, label="KDE")
    mu, sigma = x.mean(), x.std()
    ax.plot(kde_x, stats.norm.pdf(kde_x, mu, sigma), "k--", lw=1.2,
            label=f"N({mu:.3f}, {sigma:.3f}²)")
    ax.set_xlabel(LABELS["weight"], fontsize=9)
    ax.set_ylabel("Density", fontsize=9)
    ax.legend(fontsize=8, frameon=False)
    ax.set_title(f"Weight Distribution (n = {len(df_w)})", fontsize=10)
    fig.tight_layout()
    fig.savefig(FIGS_DIR / "fig5_weight_dist.svg", bbox_inches="tight")
    plt.close(fig)


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


def fig_ransac(df_w: pd.DataFrame) -> dict:
    X = df_w[FEATURES].values
    y = df_w["weight"].values

    ols = LinearRegression().fit(X, y)
    y_ols = ols.predict(X)

    ransac = RANSACRegressor(
        estimator=LinearRegression(),
        min_samples=0.5,
        residual_threshold=None,
        random_state=42,
        max_trials=500,
    )
    ransac.fit(X, y)
    y_ransac = ransac.predict(X)
    inlier_mask = ransac.inlier_mask_
    outlier_mask = ~inlier_mask

    ss_tot = np.sum((y - y.mean()) ** 2)
    r2_ols = 1 - np.sum((y - y_ols) ** 2) / ss_tot
    r2_ransac_in = 1 - np.sum((y[inlier_mask] - y_ransac[inlier_mask]) ** 2) / np.sum(
        (y[inlier_mask] - y[inlier_mask].mean()) ** 2
    )

    fig, axes = plt.subplots(1, 2, figsize=(10, 4.5))

    ax = axes[0]
    ax.scatter(y_ols, y, s=18, alpha=0.6, color="#4878CF")
    lims = [min(y_ols.min(), y.min()) - 0.02, max(y_ols.max(), y.max()) + 0.02]
    ax.plot(lims, lims, "k--", lw=1.2, label=f"OLS  R²={r2_ols:.3f}")
    ax.set_xlabel("Fitted weight (mg)", fontsize=9)
    ax.set_ylabel("Actual weight (mg)", fontsize=9)
    ax.set_title("OLS: Fitted vs Actual", fontsize=10)
    ax.legend(fontsize=8, frameon=False)
    ax.set_xlim(lims); ax.set_ylim(lims)

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

    return {
        "ransac": ransac,
        "r2_ols": r2_ols,
        "r2_ransac_inliers": r2_ransac_in,
        "n_inliers": int(inlier_mask.sum()),
        "n_outliers": int(outlier_mask.sum()),
        "inlier_mask": inlier_mask,
    }


# ── Statistics computation ────────────────────────────────────────────────────
def compute_stats(df: pd.DataFrame, df_w: pd.DataFrame, ransac_results: dict) -> dict:
    # Descriptive statistics table
    desc_rows = []
    for feat in FEATURES:
        x = df[feat].dropna()
        desc_rows.append({
            "Feature": LABELS[feat],
            "Mean": f"{x.mean():.2f}",
            "SD": f"{x.std():.2f}",
            "Median": f"{x.median():.2f}",
            "Skewness": f"{stats.skew(x):.2f}",
            "Ex. Kurt.": f"{stats.kurtosis(x, fisher=True):.2f}",
            "Range": f"{x.min():.1f}\u2013{x.max():.1f}",
        })
    xw = df_w["weight"]
    desc_rows.append({
        "Feature": LABELS["weight"],
        "Mean": f"{xw.mean():.3f}",
        "SD": f"{xw.std():.3f}",
        "Median": f"{xw.median():.3f}",
        "Skewness": f"{stats.skew(xw):.2f}",
        "Ex. Kurt.": f"{stats.kurtosis(xw, fisher=True):.2f}",
        "Range": f"{xw.min():.2f}\u2013{xw.max():.2f}",
    })
    desc_df = pd.DataFrame(desc_rows).set_index("Feature")

    # Normality tests table
    norm_feats = FEATURES + ["weight"]
    norm_raw = []
    for feat in norm_feats:
        x = (df[feat] if feat in FEATURES else df_w[feat]).dropna().values
        sw_stat, sw_p = stats.shapiro(x)
        ks_stat, ks_p = stats.kstest(x, "norm", args=(x.mean(), x.std(ddof=1)))
        norm_raw.append({
            "feat": feat,
            "sw_stat": sw_stat, "sw_p": sw_p,
            "ks_stat": ks_stat, "ks_p": ks_p,
        })

    norm_df = pd.DataFrame([
        {
            "Feature": SHORT_LABELS[r["feat"]],
            "S-W W": f"{r['sw_stat']:.4f}",
            "S-W p": fmt_p(r["sw_p"]),
            "K-S D": f"{r['ks_stat']:.4f}",
            "K-S p": fmt_p(r["ks_p"]),
        }
        for r in norm_raw
    ]).set_index("Feature")

    ks_min_p = min(r["ks_p"] for r in norm_raw)
    weight_norm = norm_raw[-1]

    # Pearson correlations with weight
    corr = {}
    for feat in FEATURES:
        r, p = stats.pearsonr(df_w[feat], df_w["weight"])
        corr[feat] = {"r": r, "p": p}

    # OLS regression with statsmodels (for p-values)
    X_sm = sm.add_constant(df_w[FEATURES])
    ols_model = sm.OLS(df_w["weight"], X_sm).fit()

    # Model comparison table
    predictors = ["const"] + FEATURES
    labels_model = ["Intercept"] + [SHORT_LABELS[f] for f in FEATURES]
    ransac = ransac_results["ransac"]
    ransac_coefs = [ransac.estimator_.intercept_] + list(ransac.estimator_.coef_)

    model_rows = []
    for pred, label, ransac_c in zip(predictors, labels_model, ransac_coefs):
        ols_c = ols_model.params[pred]
        ols_p = ols_model.pvalues[pred]
        model_rows.append({
            "Predictor": label,
            "OLS coef.": f"{ols_c:.4f}",
            "OLS p": fmt_p(ols_p),
            "RANSAC coef.": f"{ransac_c:.4f}",
        })
    model_df = pd.DataFrame(model_rows).set_index("Predictor")

    return {
        "n_total": len(df),
        "n_weight": len(df_w),
        "n_missing": len(df) - len(df_w),
        "desc_df": desc_df,
        "norm_df": norm_df,
        "ks_min_p": ks_min_p,
        "weight_norm": weight_norm,
        "corr": corr,
        "model_df": model_df,
        "r2_ols": ols_model.rsquared,
        "r2_ransac_inliers": ransac_results["r2_ransac_inliers"],
        "n_inliers": ransac_results["n_inliers"],
        "n_outliers": ransac_results["n_outliers"],
    }


# ── Save outputs ──────────────────────────────────────────────────────────────
def save_outputs(s: dict) -> None:
    # Scalar results → TOML
    corr = s["corr"]
    toml_data = {
        "data": {
            "n_total": s["n_total"],
            "n_weight": s["n_weight"],
            "n_missing": s["n_missing"],
        },
        "normality": {
            "ks_min_p": f"{s['ks_min_p']:.3f}",
            "weight_sw_p": fmt_p(s["weight_norm"]["sw_p"]).replace("*", ""),
            "weight_ks_p": fmt_p(s["weight_norm"]["ks_p"]).replace("*", ""),
        },
        "correlations": {
            "head_r": f"{corr['length_head']['r']:.2f}",
            "head_p": fmt_p(corr["length_head"]["p"]).replace("*", ""),
            "body_r": f"{corr['length_body']['r']:.2f}",
            "body_p": fmt_p(corr["length_body"]["p"]).replace("*", ""),
            "thickness_r": f"{corr['thickness_body']['r']:.2f}",
            "thickness_p": fmt_p(corr["thickness_body"]["p"]).replace("*", ""),
            "tail_r": f"{corr['length_tail']['r']:.2f}",
            "tail_p": fmt_p(corr["length_tail"]["p"]).replace("*", ""),
        },
        "regression": {
            "r2_ols": f"{s['r2_ols']:.3f}",
            "r2_ransac_inliers": f"{s['r2_ransac_inliers']:.3f}",
            "n_inliers": s["n_inliers"],
            "n_outliers": s["n_outliers"],
        },
    }
    write_toml(toml_data, OUTPUTS_DIR / "results.toml")

    # Tables → .typ files
    for name, df in [
        ("tbl_desc", s["desc_df"]),
        ("tbl_norm", s["norm_df"]),
        ("tbl_models", s["model_df"]),
    ]:
        t = make_booktabs_table(df)
        (OUTPUTS_DIR / f"{name}.typ").write_text(t.render(), encoding="utf-8")


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    print("[1/4] Loading data...")
    df, df_w = load_data()

    print("[2/4] Generating figures...")
    fig_distributions(df)
    fig_qqplots(df)
    fig_weight_distribution(df_w)
    fig_correlation(df_w)
    ransac_results = fig_ransac(df_w)

    print("[3/4] Computing statistics...")
    s = compute_stats(df, df_w, ransac_results)

    print("[4/4] Saving outputs...")
    save_outputs(s)

    print("Done.")


if __name__ == "__main__":
    main()
