# =============================================================================
# Hands-on 02 — CAP 417 — Part C
# Structure, Randomness, and the Cullen-Frey-Pearson Space
# =============================================================================

import numpy as np
import scipy.stats as stats
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import os

# ---------------------------------------------------------------------------
# Global constants
# ---------------------------------------------------------------------------
GLOBAL_SEED = 42
N_POINTS = 1000          # length of each time series realization
N_REALIZATIONS = 100     # independent realizations per noise type
LAGS_ACF = 60            # number of lags to show in ACF plots

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
FIG_DIR = os.path.join(OUTPUT_DIR, "figures")
RES_DIR = os.path.join(OUTPUT_DIR, "results")

os.makedirs(FIG_DIR, exist_ok=True)
os.makedirs(RES_DIR, exist_ok=True)

rng = np.random.default_rng(GLOBAL_SEED)

# =============================================================================
# PART 2.1 — Shuffle Analysis
# =============================================================================

print("=" * 60)
print("PART 2.1 — Shuffle Analysis")
print("=" * 60)

# Generate Brownian (red noise) time series via cumulative sum of Gaussian increments
increments = rng.standard_normal(N_POINTS)
original = np.cumsum(increments)

# Shuffled version: random permutation of the same values (destroys temporal structure)
shuffled = rng.permutation(original)

# --- Compute statistical moments ---
def compute_moments(x):
    return {
        "mean": np.mean(x),
        "variance": np.var(x, ddof=1),
        "skewness": stats.skew(x),
        "kurtosis_excess": stats.kurtosis(x),   # excess kurtosis (normal = 0)
        "kurtosis_raw": stats.kurtosis(x) + 3,  # raw kurtosis (normal = 3)
    }

mom_orig = compute_moments(original)
mom_shuf = compute_moments(shuffled)

print("\nStatistical Moments Comparison (excess kurtosis; normal distribution = 0):")
print(f"{'Moment':<20} {'Original':>15} {'Shuffled':>15}")
print("-" * 52)
for key in ["mean", "variance", "skewness", "kurtosis_excess"]:
    print(f"{key:<20} {mom_orig[key]:>15.6f} {mom_shuf[key]:>15.6f}")

# Save moments table
moments_df = pd.DataFrame({
    "moment": ["mean", "variance", "skewness", "kurtosis_excess", "kurtosis_raw"],
    "original": [mom_orig[k] for k in ["mean", "variance", "skewness", "kurtosis_excess", "kurtosis_raw"]],
    "shuffled": [mom_shuf[k] for k in ["mean", "variance", "skewness", "kurtosis_excess", "kurtosis_raw"]],
})
moments_df.to_csv(os.path.join(RES_DIR, "moments_table.csv"), index=False)
print("\nSaved: results/moments_table.csv")

# --- Plot: time series side-by-side ---
fig, axes = plt.subplots(1, 2, figsize=(14, 4), sharey=True)
t = np.arange(N_POINTS)

axes[0].plot(t, original, color="steelblue", linewidth=0.8)
axes[0].set_title("Original Brownian Series", fontsize=13)
axes[0].set_xlabel("Time step")
axes[0].set_ylabel("Value")

axes[1].plot(t, shuffled, color="tomato", linewidth=0.8)
axes[1].set_title("Shuffled Series (random permutation)", fontsize=13)
axes[1].set_xlabel("Time step")

fig.suptitle("Part 2.1 — Original vs Shuffled Time Series", fontsize=14, y=1.02)
plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, "fig_2_1_series.png"), dpi=150, bbox_inches="tight")
plt.close()
print("Saved: figures/fig_2_1_series.png")

# --- Plot: ACF comparison ---
def acf(x, nlags):
    """Compute normalized autocorrelation function up to nlags."""
    x = x - np.mean(x)
    full = np.correlate(x, x, mode="full")
    acf_vals = full[len(x) - 1 :]
    acf_vals /= acf_vals[0]
    return acf_vals[: nlags + 1]

orig_acf = acf(original, LAGS_ACF)
shuf_acf = acf(shuffled, LAGS_ACF)
lags = np.arange(LAGS_ACF + 1)

# 95% confidence bound for white noise hypothesis
ci = 1.96 / np.sqrt(N_POINTS)

fig, axes = plt.subplots(1, 2, figsize=(14, 4), sharey=True)
for ax, acf_vals, label, color in zip(
    axes,
    [orig_acf, shuf_acf],
    ["Original", "Shuffled"],
    ["steelblue", "tomato"],
):
    ax.bar(lags, acf_vals, color=color, alpha=0.7, width=0.8)
    ax.axhline(ci, color="gray", linestyle="--", linewidth=0.9, label="95% CI")
    ax.axhline(-ci, color="gray", linestyle="--", linewidth=0.9)
    ax.axhline(0, color="black", linewidth=0.5)
    ax.set_title(f"ACF — {label}", fontsize=13)
    ax.set_xlabel("Lag")
    ax.set_ylabel("Autocorrelation")
    ax.legend(fontsize=9)

fig.suptitle("Part 2.1 — Autocorrelation Function Comparison", fontsize=14, y=1.02)
plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, "fig_2_1_acf.png"), dpi=150, bbox_inches="tight")
plt.close()
print("Saved: figures/fig_2_1_acf.png")

# --- Analysis answers (inline comments) ---
# Q: Do moment values change after shuffling?
#    No — mean, variance, skewness, and kurtosis are all preserved exactly.
#    These are order-independent statistics computed on the *marginal distribution*.
#
# Q: What does this indicate about temporal dependence vs. marginal distribution?
#    Shuffling destroys the temporal order (and thus all autocorrelation / memory),
#    but leaves the marginal distribution unchanged.  The moments characterize the
#    distribution of individual values, not their sequential arrangement.
#
# Q: Does shuffling preserve the distribution? (Verify the theoretical hypothesis.)
#    Yes — the shuffled series is just a permutation of the original values, so the
#    empirical distribution (histogram, CDF, all moments) is identical.  The ACF,
#    however, drops to near-zero for all lags > 0, confirming that temporal structure
#    has been destroyed.

# =============================================================================
# PART 2.2 — Colored Noise Generation
# =============================================================================

print("\n" + "=" * 60)
print("PART 2.2 — Colored Noise Generation")
print("=" * 60)


def generate_colored_noise(N, beta, seed=None):
    """
    Generate colored noise with power spectral density proportional to f^(-beta).

    Parameters
    ----------
    N     : int   — number of samples
    beta  : float — spectral exponent (0 = white, 1 = pink, 2 = red/Brownian)
    seed  : int or None — random seed for reproducibility

    Returns
    -------
    noise : ndarray of shape (N,), real-valued
    """
    local_rng = np.random.default_rng(seed)
    white = local_rng.standard_normal(N)

    freqs = np.fft.rfftfreq(N)          # positive frequencies [0, 0.5]
    spectrum = np.fft.rfft(white)

    # Build shaping filter: amplitude ∝ f^(-beta/2)
    # DC component (freq=0) is left unchanged to avoid division by zero
    shaping = np.ones_like(freqs)
    shaping[1:] = freqs[1:] ** (-beta / 2.0)

    colored_spectrum = spectrum * shaping
    noise = np.fft.irfft(colored_spectrum, n=N)

    # Standardize to zero mean, unit variance for fair comparison
    noise = (noise - noise.mean()) / noise.std()
    return noise


# Noise type definitions
NOISE_TYPES = {
    "White (β=0)": 0,
    "Pink (β=1)":  1,
    "Red (β=2)":   2,
}

# Generate one example realization per noise type for illustration
example_realizations = {}
for label, beta in NOISE_TYPES.items():
    example_realizations[label] = generate_colored_noise(N_POINTS, beta, seed=GLOBAL_SEED)

# --- Plot: example realizations ---
fig, axes = plt.subplots(3, 1, figsize=(12, 8), sharex=True)
colors = ["#4C9BE8", "#E8934C", "#6FCF5B"]

for ax, (label, signal), color in zip(axes, example_realizations.items(), colors):
    ax.plot(signal, color=color, linewidth=0.8)
    ax.set_ylabel("Amplitude", fontsize=10)
    ax.set_title(f"{label} noise (example realization)", fontsize=11)
    ax.axhline(0, color="white" if ax.get_facecolor()[0] < 0.5 else "gray",
               linewidth=0.5, linestyle="--")

axes[-1].set_xlabel("Time step", fontsize=11)
fig.suptitle("Part 2.2 — Example Realizations of Colored Noise", fontsize=13)
plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, "fig_2_2_examples.png"), dpi=150, bbox_inches="tight")
plt.close()
print("Saved: figures/fig_2_2_examples.png")

# =============================================================================
# PART 2.3 — Cullen-Frey-Pearson Plot
# =============================================================================

print("\n" + "=" * 60)
print("PART 2.3 — Cullen-Frey-Pearson Plot")
print("=" * 60)

# Generate 100 independent realizations for each noise type and record S and K
records = []
base_seed = GLOBAL_SEED

for noise_label, beta in NOISE_TYPES.items():
    for i in range(N_REALIZATIONS):
        seed_i = base_seed + hash((noise_label, i)) % (2**31)
        series = generate_colored_noise(N_POINTS, beta, seed=seed_i)
        s = stats.skew(series)
        k = stats.kurtosis(series) + 3   # raw kurtosis (K=3 for Gaussian)
        records.append({
            "noise_type": noise_label,
            "beta": beta,
            "realization": i,
            "skewness": s,
            "kurtosis_raw": k,
            "skewness_sq": s ** 2,
        })

noise_df = pd.DataFrame(records)
noise_df.to_csv(os.path.join(RES_DIR, "noise_moments.csv"), index=False)
print("Saved: results/noise_moments.csv")
summary = noise_df.groupby("noise_type")[["skewness", "kurtosis_raw"]].describe().round(4)
print(summary.to_string().encode("ascii", errors="replace").decode("ascii"))

# --- Cullen-Frey-Pearson scatter plot with dark background ---
PLOT_COLORS = {
    "White (β=0)": "#4C9BE8",
    "Pink (β=1)":  "#E8934C",
    "Red (β=2)":   "#6FCF5B",
}

with plt.style.context("dark_background"):
    fig, ax = plt.subplots(figsize=(10, 7))

    for label, group in noise_df.groupby("noise_type"):
        ax.scatter(
            group["skewness_sq"],
            group["kurtosis_raw"],
            label=label,
            color=PLOT_COLORS[label],
            alpha=0.65,
            s=35,
            edgecolors="none",
        )

    # Gaussian reference point: S²=0, K=3
    ax.scatter(
        0, 3,
        marker="*",
        s=300,
        color="white",
        zorder=5,
        label="Gaussian (S²=0, K=3)",
    )
    ax.annotate(
        "Gaussian",
        xy=(0, 3),
        xytext=(0.15, 3.15),
        color="white",
        fontsize=10,
        arrowprops=dict(arrowstyle="->", color="white", lw=0.8),
    )

    ax.set_xlabel("Squared Skewness  S²", fontsize=12)
    ax.set_ylabel("Raw Kurtosis  K", fontsize=12)
    ax.set_title(
        "Cullen-Frey-Pearson Space — 100 Realizations per Noise Type\n"
        "(N = 1000 per realization)",
        fontsize=13,
    )
    ax.legend(fontsize=10, loc="upper right")
    ax.grid(alpha=0.2)

    plt.tight_layout()
    plt.savefig(
        os.path.join(FIG_DIR, "fig_2_3_cullen_frey.png"),
        dpi=150,
        bbox_inches="tight",
        facecolor=fig.get_facecolor(),
    )
    plt.close()

print("Saved: figures/fig_2_3_cullen_frey.png")

print("\n" + "=" * 60)
print("All outputs generated successfully.")
print("=" * 60)
