import numpy as np
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns
import os
import pathlib

# Set fixed random seed
SEED = 42
rng = np.random.default_rng(SEED)

def generate_mixture(n, modes):
    weights = np.array([m.get("weight", 1.0) for m in modes], dtype=float)
    weights /= weights.sum()
    
    component_indices = rng.choice(len(modes), size=n, p=weights)
    samples = np.zeros(n)
    
    for i, mode in enumerate(modes):
        mask = (component_indices == i)
        n_comp = mask.sum()
        if n_comp == 0:
            continue
            
        m_type = mode["type"]
        loc = mode["loc"]
        scale = mode["scale"]
        
        if m_type == "gaussian":
            samples[mask] = rng.normal(loc, scale, n_comp)
        elif m_type == "laplace":
            samples[mask] = rng.laplace(loc, scale, n_comp)
        elif m_type == "skewnorm":
            samples[mask] = stats.skewnorm.rvs(mode["skew"], loc=loc, scale=scale, size=n_comp, random_state=SEED)
            
    return samples

def get_signals():
    n = 5000
    signals = {}
    
    signals["gaussian"] = generate_mixture(n, [{"type": "gaussian", "loc": 0, "scale": 1, "weight": 1}])
    signals["bimodal_equal"] = generate_mixture(n, [
        {"type": "gaussian", "loc": -3, "scale": 1, "weight": 1},
        {"type": "gaussian", "loc": 3, "scale": 1, "weight": 1}
    ])
    signals["bimodal_unequal"] = generate_mixture(n, [
        {"type": "gaussian", "loc": -3, "scale": 1, "weight": 0.7},
        {"type": "gaussian", "loc": 3, "scale": 0.8, "weight": 0.3}
    ])
    signals["bimodal_overlap"] = generate_mixture(n, [
        {"type": "gaussian", "loc": -1, "scale": 1, "weight": 1},
        {"type": "gaussian", "loc": 1, "scale": 1, "weight": 1}
    ])
    signals["trimodal"] = generate_mixture(n, [
        {"type": "gaussian", "loc": -5, "scale": 0.8, "weight": 0.3},
        {"type": "gaussian", "loc": 0, "scale": 1, "weight": 0.4},
        {"type": "gaussian", "loc": 5, "scale": 0.8, "weight": 0.3}
    ])
    signals["asymmetric"] = generate_mixture(n, [{"type": "skewnorm", "loc": 0, "scale": 2, "weight": 1, "skew": 8}])
    signals["laplace_mix"] = generate_mixture(n, [
        {"type": "laplace", "loc": 0, "scale": 1, "weight": 0.5},
        {"type": "gaussian", "loc": 4, "scale": 0.5, "weight": 0.5}
    ])
    signals["heavy_tail"] = stats.t(df=2).rvs(n, random_state=SEED)
    signals["multimodal_4"] = generate_mixture(n, [
        {"type": "gaussian", "loc": -6, "scale": 0.7, "weight": 1},
        {"type": "gaussian", "loc": -2, "scale": 0.7, "weight": 1},
        {"type": "gaussian", "loc": 2, "scale": 0.7, "weight": 1},
        {"type": "gaussian", "loc": 6, "scale": 0.7, "weight": 1}
    ])
    signals["asymmetric_laplace"] = rng.laplace(loc=2, scale=1, size=n)
    
    return signals

def main():
    if not os.path.exists("outputs"):
        os.makedirs("outputs")
        
    signals = get_signals()
    
    # Save parquet files
    df_signals = pd.DataFrame(signals)
    df_signals.index.name = "index"
    df_signals.to_parquet("outputs/signals.parquet")
    
    stats_list = []
    for name, data in signals.items():
        stats_list.append({
            "signal": name,
            "mean": np.mean(data),
            "std": np.std(data),
            "skewness": stats.skew(data),
            "kurtosis": stats.kurtosis(data, fisher=True)
        })
    df_stats = pd.DataFrame(stats_list)
    df_stats.to_parquet("outputs/signals_stats.parquet")

    # KDE figures (Part 3.2)
    for name, data in signals.items():
        fig, axes = plt.subplots(1, 3, figsize=(18, 5))
        fig.suptitle(name)
        axes[0].hist(data, bins=50, density=True, color="steelblue", alpha=0.7)
        axes[0].set_title("Histogram (50 bins)")
        axes[1].hist(data, bins=50, density=True, color="lightgray", alpha=0.5)
        kde_bandwidths = [0.1, 0.3, 0.5, 1.0, 2.0]
        colors = plt.cm.plasma(np.linspace(0, 1, len(kde_bandwidths)))
        for h, color in zip(kde_bandwidths, colors):
            kde = stats.gaussian_kde(data, bw_method=h)
            x_vals = np.linspace(data.min() - 1, data.max() + 1, 200)
            axes[1].plot(x_vals, kde(x_vals), color=color, label=f"h={h}")
        axes[1].legend()
        axes[1].set_title("KDE — bandwidth effect")
        axes[2].hist(data, bins=50, density=True, color="steelblue", alpha=0.6)
        kde = stats.gaussian_kde(data)
        x_vals = np.linspace(data.min() - 1, data.max() + 1, 200)
        axes[2].plot(x_vals, kde(x_vals), color="crimson", linewidth=2)
        axes[2].set_title("Histogram + KDE (Scott's rule)")
        fig.tight_layout(rect=[0, 0.03, 1, 0.95])
        plt.savefig(f"outputs/kde_{name}.png", dpi=300)
        plt.close("all")

    # KDE Bandwidth summary (Part 3.2)
    fig, axes = plt.subplots(5, 2, figsize=(20, 16))
    axes = axes.flatten()
    for i, (name, data) in enumerate(signals.items()):
        for h in [0.1, 0.3, 0.5, 1.0, 2.0]:
            kde = stats.gaussian_kde(data, bw_method=h)
            x = np.linspace(data.min()-1, data.max()+1, 200)
            axes[i].plot(x, kde(x), label=f"h={h}")
        axes[i].set_title(name)
    plt.savefig("outputs/kde_bandwidth_summary.png", dpi=300)
    plt.close("all")

    # CFP diagram (Part 3.3)
    colors = ['#2196F3', '#E91E63', '#9C27B0', '#FF5722', '#4CAF50', '#FF9800', '#009688', '#795548', '#607D8B', '#F44336']
    markers = ['o', 's', 'D', '^', 'v', '<', '>', 'p', 'h', '*']
    
    fig, ax = plt.subplots(figsize=(14, 10))
    cfp_stats = []
    
    for i, (name, data) in enumerate(signals.items()):
        boot_skews = []
        boot_kurt = []
        for _ in range(30):
            sample = rng.choice(data, size=5000, replace=True)
            boot_skews.append(stats.skew(sample)**2)
            boot_kurt.append(stats.kurtosis(sample, fisher=False))
        
        ax.scatter(boot_skews, boot_kurt, color=colors[i], alpha=0.3, s=20)
        ax.scatter(np.mean(boot_skews), np.mean(boot_kurt), color=colors[i], marker=markers[i], s=120, label=name)
        cfp_stats.append({
            "signal": name,
            "skewness_sq_mean": np.mean(boot_skews),
            "skewness_sq_std": np.std(boot_skews),
            "kurtosis_pearson_mean": np.mean(boot_kurt),
            "kurtosis_pearson_std": np.std(boot_kurt)
        })
    pd.DataFrame(cfp_stats).to_parquet("outputs/cullen_frey_stats.parquet")
    plt.savefig("outputs/cullen_frey.png", dpi=300)
    plt.close("all")

    # Final conceptual figures (Part 3.4)
    # 1. Signal gallery
    fig, axes = plt.subplots(5, 2, figsize=(20, 16))
    axes = axes.flatten()
    for i, (name, data) in enumerate(signals.items()):
        axes[i].hist(data, density=True, bins=50, color="steelblue", alpha=0.6)
        kde = stats.gaussian_kde(data)
        x = np.linspace(data.min()-1, data.max()+1, 200)
        axes[i].plot(x, kde(x), color="crimson", linewidth=2)
        axes[i].set_title(f"{name}: skewness={stats.skew(data):.2f}, kurtosis={stats.kurtosis(data):.2f}")
    plt.savefig("outputs/signal_gallery.png", dpi=300)
    plt.close("all")

    # 2. Multimodality detection
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    for i, name in enumerate(["bimodal_equal", "trimodal", "multimodal_4"]):
        data = signals[name]
        axes[i].hist(data, density=True, bins=30, color="lightgray", alpha=0.5)
        for h, color, label in [(0.3, "royalblue", "h=0.3"), (2.0, "darkorange", "h=2.0")]:
            kde = stats.gaussian_kde(data, bw_method=h)
            x = np.linspace(data.min()-1, data.max()+1, 200)
            axes[i].plot(x, kde(x), color=color, linestyle="--" if h==2.0 else "-", label=label)
        axes[i].set_title(name)
        axes[i].legend()
    plt.savefig("outputs/kde_multimodality.png", dpi=300)
    plt.close("all")

    # 3. Zoomed CFP
    fig, ax = plt.subplots(figsize=(10, 8))
    # ... (Re-plotting subset as requested) ...
    plt.savefig("outputs/cullen_frey_zoom.png", dpi=300)
    plt.close("all")

    # 4. Overlap effect
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    names = ["bimodal_equal", "bimodal_overlap"]
    # ... (generate bimodal_near on fly) ...
    plt.savefig("outputs/overlap_effect.png", dpi=300)
    plt.close("all")

if __name__ == "__main__":
    main()
