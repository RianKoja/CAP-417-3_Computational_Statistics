"""
Problem 2: Central Limit Theorem and Confidence Intervals

Motivation: n=25 adult males, sample mean cholesterol=186, sample std=12.
Assume the population is normally distributed.

Creates figures illustrating:
1. CLT: how the distribution of the sample mean converges to normal
2. The 95% confidence interval for the mean (using t-distribution)
3. The 95% confidence interval for the variance (using chi-squared)
"""

from pathlib import Path
import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import stats

SEED = 42
FIGURES_DIR = Path(__file__).parent.parent / "figures"
FIGURES_DIR.mkdir(exist_ok=True)

# Problem data
N = 25
SAMPLE_MEAN = 186.0
SAMPLE_STD = 12.0
ALPHA = 0.05


def plot_clt_convergence():
    """
    Show how the sampling distribution of the mean converges to Normal
    for the cholesterol population (Normal(186, 12)) as n grows.
    """
    rng = np.random.default_rng(SEED)
    population_mean = SAMPLE_MEAN
    population_std = SAMPLE_STD
    n_repeats = 5000
    sample_sizes = [2, 5, 10, 25, 100]

    fig, axes = plt.subplots(1, len(sample_sizes), figsize=(15, 4), sharey=False)
    fig.suptitle(
        "Central Limit Theorem: Sampling Distribution of the Mean\n"
        "Population: Normal(μ=186, σ=12)",
        fontsize=12,
        fontweight="bold",
    )

    for ax, n in zip(axes, sample_sizes):
        sample_means = np.array(
            [
                rng.normal(population_mean, population_std, n).mean()
                for _ in range(n_repeats)
            ]
        )
        theoretical_std = population_std / np.sqrt(n)
        x = np.linspace(sample_means.min(), sample_means.max(), 300)

        ax.hist(
            sample_means,
            bins=50,
            density=True,
            color="#4C72B0",
            edgecolor="white",
            alpha=0.7,
            label="Simulated",
        )
        ax.plot(
            x,
            stats.norm.pdf(x, population_mean, theoretical_std),
            "r-",
            lw=2,
            label=f"N(μ, σ²/{n})",
        )
        ax.set_title(f"n = {n}", fontsize=11)
        ax.set_xlabel("Sample Mean")
        if ax is axes[0]:
            ax.set_ylabel("Density")
        ax.legend(fontsize=7)
        ax.text(
            0.97,
            0.95,
            f"σ/√n={theoretical_std:.2f}",
            transform=ax.transAxes,
            ha="right",
            va="top",
            fontsize=8,
            bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.5),
        )

    fig.tight_layout()
    out = FIGURES_DIR / "problem2_clt.svg"
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved {out}")


def plot_confidence_intervals():
    """
    Visualise the 95% CI for the mean and variance from the cholesterol sample.
    Also show the CI coverage property via simulation.
    """
    # ── Analytical CIs ────────────────────────────────────────────────────────
    df = N - 1  # degrees of freedom

    # CI for the mean  (t-distribution because σ is unknown)
    t_crit = stats.t.ppf(1 - ALPHA / 2, df=df)
    se_mean = SAMPLE_STD / np.sqrt(N)
    ci_mean = (SAMPLE_MEAN - t_crit * se_mean, SAMPLE_MEAN + t_crit * se_mean)

    # CI for the variance  (chi-squared)
    chi2_low = stats.chi2.ppf(ALPHA / 2, df=df)
    chi2_high = stats.chi2.ppf(1 - ALPHA / 2, df=df)
    ci_var = (df * SAMPLE_STD**2 / chi2_high, df * SAMPLE_STD**2 / chi2_low)
    ci_std = (np.sqrt(ci_var[0]), np.sqrt(ci_var[1]))

    print(f"95% CI for mean:  ({ci_mean[0]:.2f}, {ci_mean[1]:.2f})")
    print(f"95% CI for std:   ({ci_std[0]:.2f}, {ci_std[1]:.2f})")

    # ── Coverage simulation ───────────────────────────────────────────────────
    rng = np.random.default_rng(SEED)
    n_sims = 1000
    true_mu = SAMPLE_MEAN
    true_sigma = SAMPLE_STD
    covered = 0
    ci_lo_all, ci_hi_all = [], []

    for _ in range(n_sims):
        samp = rng.normal(true_mu, true_sigma, N)
        s_mean = samp.mean()
        s_std = samp.std(ddof=1)
        t = stats.t.ppf(1 - ALPHA / 2, df=N - 1)
        lo = s_mean - t * s_std / np.sqrt(N)
        hi = s_mean + t * s_std / np.sqrt(N)
        ci_lo_all.append(lo)
        ci_hi_all.append(hi)
        if lo <= true_mu <= hi:
            covered += 1

    coverage = covered / n_sims

    # ── Figure ────────────────────────────────────────────────────────────────
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    fig.suptitle(
        "95% Confidence Interval — Cholesterol Data (n=25, x̄=186, s=12)",
        fontsize=12,
        fontweight="bold",
    )

    # Left: t-distribution for the mean
    ax = axes[0]
    df_plot = N - 1
    x = np.linspace(-5, 5, 500)
    ax.plot(x, stats.t.pdf(x, df=df_plot), "k-", lw=2, label=f"t({df_plot})")
    x_fill_lo = np.linspace(-5, -t_crit, 200)
    x_fill_hi = np.linspace(t_crit, 5, 200)
    ax.fill_between(
        x_fill_lo,
        stats.t.pdf(x_fill_lo, df_plot),
        alpha=0.4,
        color="red",
        label=f"α/2 = {ALPHA / 2}",
    )
    ax.fill_between(x_fill_hi, stats.t.pdf(x_fill_hi, df_plot), alpha=0.4, color="red")
    ax.axvline(-t_crit, color="red", ls="--", lw=1.2)
    ax.axvline(t_crit, color="red", ls="--", lw=1.2)
    ax.set_xlabel("t statistic")
    ax.set_ylabel("Density")
    ax.set_title(
        f"t-distribution (df={df_plot})\n"
        f"95% CI for μ: ({ci_mean[0]:.1f}, {ci_mean[1]:.1f})",
        fontsize=10,
    )
    ax.legend(fontsize=9)
    ax.text(
        0.5,
        0.05,
        f"t_crit = ±{t_crit:.3f}\nSE = {se_mean:.3f}",
        transform=ax.transAxes,
        ha="center",
        fontsize=9,
        bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.5),
    )

    # Right: CI coverage plot (first 100 simulations)
    ax = axes[1]
    show = 100
    colors = [
        "#4C72B0" if lo <= true_mu <= hi else "#C44E52"
        for lo, hi in zip(ci_lo_all[:show], ci_hi_all[:show])
    ]
    for i, (lo, hi, c) in enumerate(zip(ci_lo_all[:show], ci_hi_all[:show], colors)):
        ax.plot([lo, hi], [i, i], color=c, lw=0.8, alpha=0.7)
    ax.axvline(true_mu, color="black", lw=1.5, ls="--", label=f"True μ={true_mu}")
    ax.set_xlabel("Cholesterol Level")
    ax.set_ylabel("Simulation index")
    ax.set_title(
        f"CI Coverage ({show} of {n_sims} simulations)\n"
        f"Empirical coverage = {coverage:.1%}",
        fontsize=10,
    )
    ax.legend(fontsize=9)

    fig.tight_layout()
    out = FIGURES_DIR / "problem2_ci.svg"
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved {out}")

    return ci_mean, ci_std


if __name__ == "__main__":
    print("Generating Problem 2 figures...")
    plot_clt_convergence()
    ci_mean, ci_std = plot_confidence_intervals()
    print(f"95% CI for mean: {ci_mean}")
    print(f"95% CI for std:  {ci_std}")
    print("Done.")
