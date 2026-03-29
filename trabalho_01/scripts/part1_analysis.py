import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from statsmodels.tsa.stattools import acf
from scipy.signal import welch
from wrappers import PythonRNG, JuliaRNG, RRNG, RustRNGWrapper

def run_part1(n=10000, seed=42):
    rngs = {
        "Python": PythonRNG(seed),
        "Julia": JuliaRNG(seed),
        "R": RRNG(seed),
        "Rust": RustRNGWrapper(seed)
    }
    
    data = {name: [rng.random() for _ in range(n)] for name, rng in rngs.items()}
    df = pd.DataFrame(data)
    
    languages = list(rngs.keys())
    metrics = {}
    
    # 4x4 Figure
    fig, axes = plt.subplots(4, 4, figsize=(16, 16))
    plt.subplots_adjust(hspace=0.3, wspace=0.3)
    
    for i, lang in enumerate(languages):
        samples = df[lang].values
        
        # Stats
        hist, _ = np.histogram(samples, bins=10, range=(0, 1))
        chi2, p_chi2 = stats.chisquare(hist)
        ks_stat, p_ks = stats.kstest(samples, 'uniform')
        
        metrics[f"{lang.lower()}_chi2_stat"] = f"{chi2:.2f}"
        metrics[f"{lang.lower()}_chi2_p"] = f"{p_chi2:.4f}"
        metrics[f"{lang.lower()}_ks_stat"] = f"{ks_stat:.4f}"
        metrics[f"{lang.lower()}_ks_p"] = f"{p_ks:.4f}"
        
        # Row 1: Hist + KDE
        axes[0, i].hist(samples, bins=50, density=True, alpha=0.7, color='skyblue')
        kde = stats.gaussian_kde(samples)
        x_kde = np.linspace(0, 1, 100)
        axes[0, i].plot(x_kde, kde(x_kde), 'r-', label='KDE')
        axes[0, i].set_title(f"Dist - {lang}")
        
        # Row 2: QQ-plot
        stats.probplot(samples, dist="uniform", plot=axes[1, i])
        axes[1, i].set_title(f"QQ - {lang}")
        
        # Row 3: ACF
        lag_acf = acf(samples, nlags=40)
        axes[2, i].bar(range(len(lag_acf)), lag_acf, color='orange')
        axes[2, i].set_title(f"ACF - {lang}")
        
        # Row 4: PSD
        f, pxx = welch(samples - np.mean(samples))
        axes[3, i].plot(f, pxx, color='green')
        axes[3, i].set_title(f"PSD - {lang}")
        
    plt.tight_layout()
    plt.savefig("outputs/plots/part1_matrix.png", dpi=300)
    plt.close()
    
    return metrics

if __name__ == "__main__":
    import os
    results = run_part1()
    print(results)
