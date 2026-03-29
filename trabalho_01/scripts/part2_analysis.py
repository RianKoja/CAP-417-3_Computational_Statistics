import numpy as np
import matplotlib.pyplot as plt
from scipy import stats


def calculate_stats(samples):
    return {
        "min": float(np.min(samples)),
        "avg": float(np.mean(samples)),
        "mode": float(stats.mode(samples, keepdims=True).mode[0]),
        "median": float(np.median(samples)),
        "max": float(np.max(samples)),
        "range": float(np.ptp(samples)),
        "sum": float(np.sum(samples)),
        "var": float(np.var(samples, ddof=1)),
        "std": float(np.std(samples, ddof=1)),
    }


def run_part2(seed=42):
    np.random.seed(seed)
    s5 = np.random.randint(1, 11, size=5)
    s100 = np.random.randint(1, 11, size=100)
    stats5 = calculate_stats(s5)
    stats100 = calculate_stats(s100)
    p25, p50, p75 = np.percentile(s100, [25, 50, 75])
    unique, counts = np.unique(s100, return_counts=True)
    weighted_avg = float(np.sum(unique * (counts / len(s100))))

    # Plot 1: Side-by-side frequency distributions with summary lines
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    for ax, samples, st, title in [
        (axes[0], s5, stats5, f"n=5  (seed={seed})"),
        (axes[1], s100, stats100, f"n=100  (seed={seed})"),
    ]:
        cnts = np.bincount(samples, minlength=11)[1:]
        ax.bar(range(1, 11), cnts, color="skyblue", edgecolor="black", alpha=0.8)
        ax.axvline(st["avg"], color="red", ls="--", lw=1.5, label=f"Mean={st['avg']:.1f}")
        ax.axvline(st["median"], color="green", ls=":", lw=2, label=f"Median={st['median']:.1f}")
        ax.set_title(f"Frequency Distribution ({title})")
        ax.set_xlabel("Value")
        ax.set_ylabel("Count")
        ax.set_xticks(range(1, 11))
        ax.legend(fontsize=9)
    # Add quartile lines only to n=100 panel
    axes[1].axvline(p25, color="orange", ls="-.", lw=1.5, label=f"Q1={p25:.0f}")
    axes[1].axvline(p75, color="purple", ls="-.", lw=1.5, label=f"Q3={p75:.0f}")
    axes[1].legend(fontsize=9)
    plt.tight_layout()
    plt.savefig("outputs/plots/part2_distribution.png", dpi=150)
    plt.close()

    # Plot 2: Box plots + empirical CDF with quartile markers
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    bp = ax1.boxplot(
        [s5, s100], labels=["n=5", "n=100"], patch_artist=True,
        boxprops=dict(facecolor="lightblue"), medianprops=dict(color="red", lw=2),
    )
    ax1.set_title("Box Plot Comparison: n=5 vs n=100")
    ax1.set_ylabel("Value")
    ax1.set_yticks(range(1, 11))
    ax1.grid(axis="y", alpha=0.3)

    sorted_s = np.sort(s100)
    ecdf = np.arange(1, len(sorted_s) + 1) / len(sorted_s)
    ax2.step(sorted_s, ecdf, where="post", color="steelblue", lw=2, label="ECDF")
    for pct, val, col, name in [
        (25, p25, "orange", "Q1"), (50, p50, "red", "Q2/Median"), (75, p75, "purple", "Q3")
    ]:
        ax2.axvline(val, color=col, ls="--", alpha=0.85, label=f"{name}={val:.0f}")
        ax2.axhline(pct / 100, color=col, ls=":", alpha=0.4)
    ax2.set_title("Empirical CDF with Quartiles (n=100)")
    ax2.set_xlabel("Value")
    ax2.set_ylabel("Cumulative Probability")
    ax2.set_xticks(range(1, 11))
    ax2.legend(fontsize=9)
    ax2.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig("outputs/plots/part2_percentiles.png", dpi=150)
    plt.close()

    metrics = {}
    for k, v in stats5.items():
        metrics[f"p2_5_{k}"] = f"{v:.2f}"
    for k, v in stats100.items():
        metrics[f"p2_100_{k}"] = f"{v:.2f}"
    metrics.update({
        "p2_100_weighted_avg": f"{weighted_avg:.2f}",
        "p2_100_p25": f"{p25:.2f}",
        "p2_100_p50": f"{p50:.2f}",
        "p2_100_p75": f"{p75:.2f}",
    })
    return metrics


if __name__ == "__main__":
    import os
    os.makedirs("outputs/plots", exist_ok=True)
    metrics = run_part2()
    print(metrics)
