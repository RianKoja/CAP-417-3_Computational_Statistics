"""
Problem 1: Sampling Distribution, Averaging Small Variances vs Large Pooled Variance, and Bootstrap Inference
"""

from pathlib import Path
import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import stats

SEED = 42
POPULATION_SIZE = 1_000_000
SMALL_N = 25
N_CHUNKS = 20
LARGE_N = 500
N_REPEATS = 1000

FIGURES_DIR = Path(__file__).parent.parent / "figures"
FIGURES_DIR.mkdir(exist_ok=True)


def generate_populations(seed=SEED):
    rng = np.random.default_rng(seed)
    bernoulli_pop = rng.binomial(1, 0.3, POPULATION_SIZE).astype(float)
    exponential_pop = rng.exponential(scale=1.0, size=POPULATION_SIZE)
    return bernoulli_pop, exponential_pop


def run_experiment(population, seed):
    rng = np.random.default_rng(seed)

    boot_means = []
    boot_stds = []

    large_means = []
    large_stds = []

    for _ in range(N_REPEATS):
        # --- "Bootstrap" (20 samples of 25 drawn directly) ---
        chunked_samples = rng.choice(
            population, size=(N_CHUNKS, SMALL_N), replace=False
        )

        # Mean of means (exactly equivalent to the mean of all 500 values here)
        boot_mean = np.mean(np.mean(chunked_samples, axis=1))
        boot_means.append(boot_mean)

        # Average of the 20 individual variances, then sqrt
        boot_var_mean = np.mean(np.var(chunked_samples, axis=1, ddof=1))
        boot_stds.append(np.sqrt(boot_var_mean))

        # --- Large Sample Procedure (500 drawn directly) ---
        large_sample = rng.choice(population, size=LARGE_N, replace=False)
        large_means.append(np.mean(large_sample))
        large_stds.append(np.std(large_sample, ddof=1))

    return (
        np.array(boot_means),
        np.array(boot_stds),
        np.array(large_means),
        np.array(large_stds),
    )


def main():
    print("Generating Problem 1 figures... (1000 repeats)")
    bernoulli_pop, exponential_pop = generate_populations()

    b_boot_means, b_boot_stds, b_large_means, b_large_stds = run_experiment(
        bernoulli_pop, SEED
    )
    e_boot_means, e_boot_stds, e_large_means, e_large_stds = run_experiment(
        exponential_pop, SEED + 1
    )

    # FIGURE 1: Mean Estimates
    fig, axes = plt.subplots(2, 2, figsize=(10, 8))
    fig.suptitle(
        "Mean Estimators: 20x25 vs 1x500 (Identical Distributions)",
        fontsize=14,
        fontweight="bold",
    )

    for i, (pop, name, color, boot_m, large_m) in enumerate(
        [
            (bernoulli_pop, "Bernoulli(0.3)", "#4C72B0", b_boot_means, b_large_means),
            (exponential_pop, "Exponential(1)", "#DD8452", e_boot_means, e_large_means),
        ]
    ):
        true_mu = pop.mean()
        true_std = pop.std()

        # True distribution
        ax = axes[i, 0]
        if "Bernoulli" in name:
            vals, counts = np.unique(pop, return_counts=True)
            ax.bar(
                vals,
                counts / POPULATION_SIZE,
                width=0.4,
                color=color,
                edgecolor="white",
            )
        else:
            x = np.linspace(0, 6, 300)
            ax.plot(x, stats.expon.pdf(x, scale=1.0), color=color, lw=2)
            ax.fill_between(x, stats.expon.pdf(x, scale=1.0), alpha=0.3, color=color)
        ax.set_title(f"{name} Population", fontsize=10)
        ax.set_xlabel("Value")
        ax.set_ylabel("Probability / Density")
        ax.text(
            0.95,
            0.85,
            f"μ={true_mu:.3f}\nσ={true_std:.3f}",
            transform=ax.transAxes,
            ha="right",
            bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.5),
        )

        # Overlapping Means - exactly the same
        ax = axes[i, 1]
        ax.hist(
            boot_m,
            bins=40,
            density=True,
            color="#C44E52",
            edgecolor="white",
            alpha=0.6,
            label="Mean of 20x25 (Batch)",
        )
        ax.hist(
            large_m,
            bins=40,
            density=True,
            color="#55A868",
            edgecolor="white",
            alpha=0.6,
            label="Mean of 500 (Pooled)",
        )
        ax.axvline(true_mu, color="black", linestyle="--", lw=1.5, label="True μ")
        ax.set_title(f"1000 Estimated Means", fontsize=10)
        ax.set_xlabel("Sample Mean")
        ax.legend(fontsize=8)

    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "problem1_sampling.svg", bbox_inches="tight")
    plt.close(fig)

    # FIGURE 2: STD Estimates
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    fig.suptitle(
        "Standard Deviation Estimators over 1000 Repeats: 20x25 vs 1x500",
        fontsize=14,
        fontweight="bold",
    )

    for ax, (pop, name, boot_s, large_s) in zip(
        axes,
        [
            (bernoulli_pop, "Bernoulli(0.3)", b_boot_stds, b_large_stds),
            (exponential_pop, "Exponential(1)", e_boot_stds, e_large_stds),
        ],
    ):
        true_std = pop.std()

        # Plot histograms overlapping
        ax.hist(
            boot_s,
            bins=40,
            density=True,
            color="#C44E52",
            alpha=0.6,
            label="Avg Var of 20 subsets of 25",
        )
        ax.hist(
            large_s,
            bins=40,
            density=True,
            color="#55A868",
            alpha=0.6,
            label="Var of single pool of 500",
        )
        ax.axvline(
            true_std,
            color="black",
            linestyle="--",
            lw=2,
            label=f"True Pop Std ({true_std:.3f})",
        )

        ax.set_title(f"{name}", fontsize=11)
        ax.set_xlabel("Estimated Standard Deviation")
        ax.set_ylabel("Density")
        ax.legend(fontsize=9)

    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "problem1_std_comparison.svg", bbox_inches="tight")
    plt.close(fig)

    # FIGURE 3: ACTUAL BOOTSTRAP INFERENCE
    # Demonstrating how exactly one sample of size N can tell us about our own error distribution
    fig, axes = plt.subplots(2, 2, figsize=(11, 8))
    fig.suptitle(
        "Bootstrap Inference: Estimating Our Own Error from 1 Sample of N=50",
        fontsize=14,
        fontweight="bold",
    )

    N_BOOT = 50
    rng = np.random.default_rng(999)
    for i, (pop, name, color) in enumerate(
        [
            (bernoulli_pop, "Bernoulli", "#4C72B0"),
            (exponential_pop, "Exponential", "#DD8452"),
        ]
    ):
        # The single data we collected in the real world
        real_sample = rng.choice(pop, size=N_BOOT, replace=False)
        sample_mean = np.mean(real_sample)
        sample_std = np.std(real_sample, ddof=1)

        # Resampling 1000 times from our single sample
        resamples = rng.choice(real_sample, size=(1000, N_BOOT), replace=True)
        resampled_means = np.mean(resamples, axis=1)
        resampled_stds = np.std(resamples, axis=1, ddof=1)

        # True errors calculated globally
        macro_samples = rng.choice(pop, size=(1000, N_BOOT), replace=False)
        true_mean_se = np.std(np.mean(macro_samples, axis=1))
        true_std_se = np.std(np.std(macro_samples, axis=1, ddof=1))

        # Plot 1: Mean Error
        ax = axes[i, 0]
        ax.hist(
            resampled_means,
            bins=30,
            density=True,
            color=color,
            alpha=0.7,
            edgecolor="white",
        )
        ax.axvline(sample_mean, color="black", lw=2, label="Sample Mean")
        ax.axvline(
            pop.mean(), color="red", linestyle="--", lw=1.5, label="True Pop Mean"
        )
        ax.set_title(f"{name}: Bootstrap Dist. of the Mean", fontsize=10)

        text_mean = (
            f"Bootstrap SE: {np.std(resampled_means):.4f}\nTrue SE: {true_mean_se:.4f}"
        )
        ax.text(
            0.95,
            0.85,
            text_mean,
            transform=ax.transAxes,
            ha="right",
            bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.5),
        )
        ax.legend(fontsize=8)

        # Plot 2: Std Error
        ax = axes[i, 1]
        ax.hist(
            resampled_stds,
            bins=30,
            density=True,
            color="#9B59B6",
            alpha=0.7,
            edgecolor="white",
        )
        ax.axvline(sample_std, color="black", lw=2, label="Sample Std")
        ax.axvline(pop.std(), color="red", linestyle="--", lw=1.5, label="True Pop Std")
        ax.set_title(f"{name}: Bootstrap Dist. of the Std Dev", fontsize=10)

        text_std = (
            f"Bootstrap SE: {np.std(resampled_stds):.4f}\nTrue SE: {true_std_se:.4f}"
        )
        ax.text(
            0.95,
            0.85,
            text_std,
            transform=ax.transAxes,
            ha="right",
            bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.5),
        )
        ax.legend(fontsize=8)

    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "problem1_bootstrap_inference.svg", bbox_inches="tight")
    plt.close(fig)
    print("Bootstrap inference figure saved.")


if __name__ == "__main__":
    main()
