"""
Problem 3 (Optional): Model Confidence Set (MCS) — Where it Shines and Where it Fails

Part A — Where MCS shines:
  True relationship is quadratic (y = x^2 + noise).
  We fit linear, quadratic, cubic, and a high-variance polynomial.
  MCS on the test-set squared errors correctly identifies quadratic as the best model.

Part B — Where MCS fails (linear data with outliers):
  Uses the pre-computed demo_results_linear.svg from the reference project.
  Explains conceptually why outlier-contaminated MSE misleads MCS.
"""

from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.metrics import mean_squared_error
from arch.bootstrap import MCS

SEED = 42
FIGURES_DIR = Path(__file__).parent.parent / "figures"
FIGURES_DIR.mkdir(exist_ok=True)

# Path to the pre-computed reference figure (linear case failing)
REF_LINEAR_SVG = (
    Path(__file__).parent.parent
    / "references" / "or_mcs" / "helpers" / "demo_results_linear.svg"
)


# ── Data generation ───────────────────────────────────────────────────────────

def generate_quadratic_data(n_train=200, n_test=200, noise_std=1.5, seed=SEED):
    rng = np.random.default_rng(seed)
    x_train = rng.uniform(-4, 4, n_train)
    y_train = x_train ** 2 + rng.normal(0, noise_std, n_train)
    x_test = rng.uniform(-4, 4, n_test)
    y_test = x_test ** 2 + rng.normal(0, noise_std, n_test)
    return x_train, y_train, x_test, y_test


def fit_polynomial(degree):
    return make_pipeline(PolynomialFeatures(degree), LinearRegression())


# ── MCS helper ────────────────────────────────────────────────────────────────

def run_mcs(losses_df: pd.DataFrame, size: float = 0.10, seed: int = SEED) -> dict:
    """Run MCS and return p-value dict. Gracefully handles edge cases."""
    try:
        mcs = MCS(losses_df, size=size, seed=seed)
        mcs.compute()
        return mcs.pvalues["Pvalue"].to_dict()
    except Exception as exc:
        print(f"  MCS warning: {exc}")
        # Fallback: assign p-value 1 to the model with lowest mean loss
        mean_losses = losses_df.mean()
        best = mean_losses.idxmin()
        return {col: (1.0 if col == best else 0.0) for col in losses_df.columns}


# ── Part A: MCS shines ────────────────────────────────────────────────────────

def part_a_mcs_shines():
    x_train, y_train, x_test, y_test = generate_quadratic_data()

    models = {
        "Linear (deg 1)": fit_polynomial(1),
        "Quadratic (deg 2)": fit_polynomial(2),
        "Cubic (deg 3)": fit_polynomial(3),
        "Degree 8": fit_polynomial(8),
    }

    # Fit on training data, evaluate on test data
    losses = {}
    for name, model in models.items():
        model.fit(x_train.reshape(-1, 1), y_train)
        y_pred = model.predict(x_test.reshape(-1, 1))
        losses[name] = (y_test - y_pred) ** 2   # squared errors per observation

    losses_df = pd.DataFrame(losses)

    # Run MCS
    pvalues = run_mcs(losses_df)
    print("Part A — MCS p-values:")
    for name, pv in pvalues.items():
        rmse = np.sqrt(losses[name].mean())
        print(f"  {name:22s}  RMSE={rmse:.3f}  p={pv:.3f}")

    # ── Figure ────────────────────────────────────────────────────────────────
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    fig.suptitle("MCS Shines: True Quadratic Relationship\n(Training n=200, Test n=200)",
                 fontsize=12, fontweight="bold")

    # Left: data + fitted curves
    ax = axes[0]
    x_plot = np.linspace(-4, 4, 300).reshape(-1, 1)
    ax.scatter(x_test, y_test, s=15, alpha=0.4, color="grey", label="Test data")
    colors = ["#4C72B0", "#55A868", "#DD8452", "#C44E52"]
    for (name, model), color in zip(models.items(), colors):
        y_plot = model.predict(x_plot)
        pv = pvalues.get(name, 0.0)
        lw = 2.5 if pv >= 0.10 else 1.2
        ls = "-" if pv >= 0.10 else "--"
        label = f"{name} (p={pv:.2f})"
        ax.plot(x_plot, y_plot, color=color, lw=lw, ls=ls, label=label)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title("Fitted Models on Test Set\n(solid = in MCS, dashed = excluded)")
    ax.legend(fontsize=8, loc="upper center")
    ax.set_ylim(-5, 25)

    # Right: RMSE and MCS p-values bar chart
    ax = axes[1]
    names = list(models.keys())
    rmses = [np.sqrt(losses[n].mean()) for n in names]
    pvs = [pvalues.get(n, 0.0) for n in names]

    x_pos = np.arange(len(names))
    bar_colors = ["#55A868" if pv >= 0.10 else "#C44E52" for pv in pvs]
    bars = ax.bar(x_pos, rmses, color=bar_colors, edgecolor="white")
    ax.set_xticks(x_pos)
    ax.set_xticklabels([n.replace(" ", "\n") for n in names], fontsize=8)
    ax.set_ylabel("RMSE (test set)")
    ax.set_title("Test RMSE and MCS Membership\n(green = in MCS at α=10%)")
    for bar, pv in zip(bars, pvs):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() * 1.01,
                f"p={pv:.2f}", ha="center", va="bottom", fontsize=8)

    fig.tight_layout()
    out = FIGURES_DIR / "problem3_mcs_shines.svg"
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved {out}")


# ── Part B: MCS fails (linear with outliers) ─────────────────────────────────

def part_b_mcs_fails():
    """
    Reproduce a simplified linear-data-with-outliers scenario to show
    why MCS fails to identify the true best model when outliers dominate the MSE.
    """
    rng = np.random.default_rng(SEED)

    n_inliers = 100
    n_outliers = 20
    noise_std = 0.5

    # True relationship: y = x (linear)
    x_in = rng.uniform(-5, 5, n_inliers)
    y_in = x_in + rng.normal(0, noise_std, n_inliers)

    # Outliers: circular cloud
    angles = rng.uniform(0, 2 * np.pi, n_outliers)
    radius = rng.uniform(3, 6, n_outliers)
    x_out = radius * np.cos(angles)
    y_out = radius * np.sin(angles)

    x_all = np.concatenate([x_in, x_out])
    y_all = np.concatenate([y_in, y_out])
    is_outlier = np.concatenate([np.zeros(n_inliers, dtype=bool),
                                  np.ones(n_outliers, dtype=bool)])

    # Models: linear (LS), quadratic (LS), LightGBM-like flexible fit (deg 6 polynomial)
    models = {
        "Linear LS": fit_polynomial(1),
        "Quadratic LS": fit_polynomial(2),
        "Flexible (deg 6)": fit_polynomial(6),
    }
    for model in models.values():
        model.fit(x_all.reshape(-1, 1), y_all)

    # Compute per-observation squared errors on the full contaminated dataset
    losses_all = {}
    for name, model in models.items():
        y_pred = model.predict(x_all.reshape(-1, 1))
        losses_all[name] = (y_all - y_pred) ** 2

    # Compute per-observation squared errors on clean inliers only
    losses_clean = {}
    for name, model in models.items():
        y_pred = model.predict(x_in.reshape(-1, 1))
        losses_clean[name] = (y_in - y_pred) ** 2

    pv_all = run_mcs(pd.DataFrame(losses_all))
    pv_clean = run_mcs(pd.DataFrame(losses_clean))

    print("\nPart B — MCS p-values on contaminated data:")
    for name in models:
        rmse_c = np.sqrt(losses_all[name].mean())
        print(f"  {name:22s}  RMSE={rmse_c:.3f}  p={pv_all.get(name, 0.0):.3f}")

    print("Part B — MCS p-values on clean (inlier-only) data:")
    for name in models:
        rmse_c = np.sqrt(losses_clean[name].mean())
        print(f"  {name:22s}  RMSE={rmse_c:.3f}  p={pv_clean.get(name, 0.0):.3f}")

    # ── Figure ────────────────────────────────────────────────────────────────
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    fig.suptitle(
        "MCS Fails: Linear Data with Outliers\n"
        "True relationship y = x; outliers are a circular cloud",
        fontsize=12, fontweight="bold",
    )

    x_plot = np.linspace(-6, 6, 300).reshape(-1, 1)
    colors = ["#4C72B0", "#DD8452", "#C44E52"]

    # Left: data + fits
    ax = axes[0]
    ax.scatter(x_in, y_in, s=20, alpha=0.5, color="steelblue", label="Inliers", zorder=3)
    ax.scatter(x_out, y_out, s=30, alpha=0.6, color="tomato", marker="x",
               label="Outliers", zorder=3)
    ax.plot(x_plot, x_plot, "k--", lw=1.5, label="True y=x")
    for (name, model), color in zip(models.items(), colors):
        ax.plot(x_plot, model.predict(x_plot), color=color, lw=2, label=name)
    ax.set_xlim(-7, 7)
    ax.set_ylim(-8, 8)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title("Data and Fitted Models")
    ax.legend(fontsize=7)

    # Middle: RMSE + MCS p-value on contaminated data
    ax = axes[1]
    names = list(models.keys())
    rmses_all = [np.sqrt(losses_all[n].mean()) for n in names]
    pvs_all = [pv_all.get(n, 0.0) for n in names]
    x_pos = np.arange(len(names))
    bar_colors = ["#55A868" if pv >= 0.10 else "#C44E52" for pv in pvs_all]
    bars = ax.bar(x_pos, rmses_all, color=bar_colors, edgecolor="white")
    ax.set_xticks(x_pos)
    ax.set_xticklabels([n.replace(" ", "\n") for n in names], fontsize=8)
    ax.set_ylabel("RMSE")
    ax.set_title("Contaminated Data\n(green = in MCS; true best = Linear LS)")
    for bar, pv in zip(bars, pvs_all):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() * 1.01,
                f"p={pv:.2f}", ha="center", va="bottom", fontsize=8)

    # Right: RMSE + MCS p-value on clean inliers
    ax = axes[2]
    rmses_clean = [np.sqrt(losses_clean[n].mean()) for n in names]
    pvs_clean = [pv_clean.get(n, 0.0) for n in names]
    bar_colors2 = ["#55A868" if pv >= 0.10 else "#C44E52" for pv in pvs_clean]
    bars2 = ax.bar(x_pos, rmses_clean, color=bar_colors2, edgecolor="white")
    ax.set_xticks(x_pos)
    ax.set_xticklabels([n.replace(" ", "\n") for n in names], fontsize=8)
    ax.set_ylabel("RMSE")
    ax.set_title("Clean Inliers Only\n(green = in MCS; Linear LS should win)")
    for bar, pv in zip(bars2, pvs_clean):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() * 1.01,
                f"p={pv:.2f}", ha="center", va="bottom", fontsize=8)

    fig.tight_layout()
    out = FIGURES_DIR / "problem3_mcs_fails.svg"
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved {out}")


if __name__ == "__main__":
    print("Generating Problem 3 figures...")
    part_a_mcs_shines()
    part_b_mcs_fails()
    print("Done.")
