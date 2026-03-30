"""
Problem 1: Sampling Distribution of the Sample Mean

Creates figures illustrating:
1. True distribution of discrete (Bernoulli) and continuous (Exponential) variables
2. Sampling distribution of the mean via bootstrap (small sample) vs large sample
3. Comparison of standard deviation of mean estimates
"""

from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy import stats

SEED = 42
POPULATION_SIZE = 1_000_000
FIGURES_DIR = Path(__file__).parent.parent / "figures"
FIGURES_DIR.mkdir(exist_ok=True)


def generate_populations(seed=SEED):
    rng = np.random.default_rng(seed)
    bernoulli_pop = rng.binomial(1, 0.3, POPULATION_SIZE).astype(float)
    exponential_pop = rng.exponential(scale=1.0, size=POPULATION_SIZE)
    return bernoulli_pop, exponential_pop


def bootstrap_mean_estimates(population, n_bootstrap=2000, sample_size=30, seed=SEED):
    """Estimate the mean repeatedly using small bootstrap samples."""
    rng = np.random.default_rng(seed)
    means = np.array([
        rng.choice(population, size=sample_size, replace=True).mean()
        for _ in range(n_bootstrap)
    ])
    return means


def large_sample_mean_estimates(population, n_repeats=2000, sample_size=1000, seed=SEED):
    """Estimate the mean repeatedly using large samples."""
    rng = np.random.default_rng(seed)
    means = np.array([
        rng.choice(population, size=sample_size, replace=False).mean()
        for _ in range(n_repeats)
    ])
    return means


def plot_problem1(bernoulli_pop, exponential_pop):
    fig, axes = plt.subplots(2, 3, figsize=(14, 8))
    fig.suptitle("Sampling Distribution of the Sample Mean", fontsize=14, fontweight="bold")

    # ── Row 0: Bernoulli ──────────────────────────────────────────────────────
    true_mu_b = bernoulli_pop.mean()
    true_std_b = bernoulli_pop.std()

    bootstrap_b = bootstrap_mean_estimates(bernoulli_pop, sample_size=30)
    large_b = large_sample_mean_estimates(bernoulli_pop, sample_size=1000)

    # True distribution
    ax = axes[0, 0]
    vals, counts = np.unique(bernoulli_pop, return_counts=True)
    ax.bar(vals, counts / POPULATION_SIZE, width=0.4, color="#4C72B0", edgecolor="white")
    ax.set_title("Bernoulli(0.3) — True Distribution", fontsize=10)
    ax.set_xlabel("Value")
    ax.set_ylabel("Probability")
    ax.text(0.95, 0.85, f"μ={true_mu_b:.3f}\nσ={true_std_b:.3f}",
            transform=ax.transAxes, ha="right", fontsize=9,
            bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.5))

    # Bootstrap means (n=30)
    ax = axes[0, 1]
    ax.hist(bootstrap_b, bins=40, density=True, color="#DD8452", edgecolor="white", alpha=0.8)
    x_range = np.linspace(bootstrap_b.min(), bootstrap_b.max(), 300)
    ax.plot(x_range, stats.norm.pdf(x_range, true_mu_b, true_std_b / np.sqrt(30)),
            'k--', lw=1.5, label=f"N(μ, σ²/n)")
    ax.set_title("Bootstrap Sample Means (n=30)", fontsize=10)
    ax.set_xlabel("Sample Mean")
    ax.set_ylabel("Density")
    ax.text(0.95, 0.85, f"std={bootstrap_b.std():.4f}",
            transform=ax.transAxes, ha="right", fontsize=9,
            bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.5))
    ax.legend(fontsize=8)

    # Large sample means (n=1000)
    ax = axes[0, 2]
    ax.hist(large_b, bins=40, density=True, color="#55A868", edgecolor="white", alpha=0.8)
    x_range = np.linspace(large_b.min(), large_b.max(), 300)
    ax.plot(x_range, stats.norm.pdf(x_range, true_mu_b, true_std_b / np.sqrt(1000)),
            'k--', lw=1.5, label=f"N(μ, σ²/n)")
    ax.set_title("Large Sample Means (n=1000)", fontsize=10)
    ax.set_xlabel("Sample Mean")
    ax.set_ylabel("Density")
    ax.text(0.95, 0.85, f"std={large_b.std():.4f}",
            transform=ax.transAxes, ha="right", fontsize=9,
            bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.5))
    ax.legend(fontsize=8)

    # ── Row 1: Exponential ────────────────────────────────────────────────────
    true_mu_e = exponential_pop.mean()
    true_std_e = exponential_pop.std()

    bootstrap_e = bootstrap_mean_estimates(exponential_pop, sample_size=30, seed=SEED + 1)
    large_e = large_sample_mean_estimates(exponential_pop, sample_size=1000, seed=SEED + 1)

    # True distribution
    ax = axes[1, 0]
    x_range = np.linspace(0, 6, 300)
    ax.plot(x_range, stats.expon.pdf(x_range, scale=1.0), color="#4C72B0", lw=2)
    ax.fill_between(x_range, stats.expon.pdf(x_range, scale=1.0), alpha=0.3, color="#4C72B0")
    ax.set_title("Exponential(λ=1) — True Distribution", fontsize=10)
    ax.set_xlabel("Value")
    ax.set_ylabel("Density")
    ax.text(0.95, 0.85, f"μ={true_mu_e:.3f}\nσ={true_std_e:.3f}",
            transform=ax.transAxes, ha="right", fontsize=9,
            bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.5))

    # Bootstrap means (n=30)
    ax = axes[1, 1]
    ax.hist(bootstrap_e, bins=40, density=True, color="#DD8452", edgecolor="white", alpha=0.8)
    x_range2 = np.linspace(bootstrap_e.min(), bootstrap_e.max(), 300)
    ax.plot(x_range2, stats.norm.pdf(x_range2, true_mu_e, true_std_e / np.sqrt(30)),
            'k--', lw=1.5, label="N(μ, σ²/n)")
    ax.set_title("Bootstrap Sample Means (n=30)", fontsize=10)
    ax.set_xlabel("Sample Mean")
    ax.set_ylabel("Density")
    ax.text(0.95, 0.85, f"std={bootstrap_e.std():.4f}",
            transform=ax.transAxes, ha="right", fontsize=9,
            bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.5))
    ax.legend(fontsize=8)

    # Large sample means (n=1000)
    ax = axes[1, 2]
    ax.hist(large_e, bins=40, density=True, color="#55A868", edgecolor="white", alpha=0.8)
    x_range2 = np.linspace(large_e.min(), large_e.max(), 300)
    ax.plot(x_range2, stats.norm.pdf(x_range2, true_mu_e, true_std_e / np.sqrt(1000)),
            'k--', lw=1.5, label="N(μ, σ²/n)")
    ax.set_title("Large Sample Means (n=1000)", fontsize=10)
    ax.set_xlabel("Sample Mean")
    ax.set_ylabel("Density")
    ax.text(0.95, 0.85, f"std={large_e.std():.4f}",
            transform=ax.transAxes, ha="right", fontsize=9,
            bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.5))
    ax.legend(fontsize=8)

    fig.tight_layout()
    out = FIGURES_DIR / "problem1_sampling.svg"
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved {out}")

    return {
        "bernoulli": {
            "true_mu": true_mu_b, "true_std": true_std_b,
            "bootstrap_std": bootstrap_b.std(), "large_std": large_b.std(),
            "theoretical_bootstrap_std": true_std_b / np.sqrt(30),
            "theoretical_large_std": true_std_b / np.sqrt(1000),
        },
        "exponential": {
            "true_mu": true_mu_e, "true_std": true_std_e,
            "bootstrap_std": bootstrap_e.std(), "large_std": large_e.std(),
            "theoretical_bootstrap_std": true_std_e / np.sqrt(30),
            "theoretical_large_std": true_std_e / np.sqrt(1000),
        },
    }


def plot_std_comparison(stats_dict):
    """Bar chart comparing empirical vs theoretical std of the mean."""
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    fig.suptitle("Std of Sample Mean: Bootstrap vs Large Sample vs Theory",
                 fontsize=12, fontweight="bold")

    for ax, (dist_name, s) in zip(axes, stats_dict.items()):
        labels = ["Bootstrap\n(n=30)", "Large Sample\n(n=1000)"]
        empirical = [s["bootstrap_std"], s["large_std"]]
        theoretical = [s["theoretical_bootstrap_std"], s["theoretical_large_std"]]

        x = np.arange(len(labels))
        width = 0.35
        bars1 = ax.bar(x - width / 2, empirical, width, label="Empirical", color="#4C72B0")
        bars2 = ax.bar(x + width / 2, theoretical, width, label="Theoretical σ/√n",
                       color="#DD8452", alpha=0.8)
        ax.set_title(dist_name.capitalize(), fontsize=11)
        ax.set_ylabel("Std of Sample Mean")
        ax.set_xticks(x)
        ax.set_xticklabels(labels)
        ax.legend(fontsize=9)

        for bar in bars1:
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() * 1.01,
                    f"{bar.get_height():.4f}", ha="center", va="bottom", fontsize=8)
        for bar in bars2:
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() * 1.01,
                    f"{bar.get_height():.4f}", ha="center", va="bottom", fontsize=8)

    fig.tight_layout()
    out = FIGURES_DIR / "problem1_std_comparison.svg"
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved {out}")


if __name__ == "__main__":
    print("Generating Problem 1 figures...")
    bernoulli_pop, exponential_pop = generate_populations()
    result = plot_problem1(bernoulli_pop, exponential_pop)
    plot_std_comparison(result)
    print("Done.")
