# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "numpy",
#     "pandas",
#     "pyarrow",
#     "matplotlib",
#     "scipy",
# ]
# ///

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import skew, kurtosis
import os

def generate_brownian_series(n):
    # Gaussian noise (mean=0, std=1)
    noise = np.random.normal(0, 1, n)
    # Cumulative sum to get Brownian motion
    series = np.cumsum(noise)
    return series

def main():
    ns = [100, 1000, 10000]
    
    for n in ns:
        print(f"Processing N={n}...")
        
        # Part 1: Time Series Generation
        series = generate_brownian_series(n)
        df_series = pd.DataFrame({
            'index': np.arange(n),
            'value': series
        })
        filename_series = f"tseries_{n}.parquet"
        df_series.to_parquet(filename_series)
        print(f"  Saved {filename_series}")
        
        # Part 2: Visualization (Histogram)
        plt.figure(figsize=(10, 6))
        plt.hist(series, bins=min(50, n // 10 + 5), color='skyblue', edgecolor='black', alpha=0.7)
        plt.title(f"Histogram of Brownian Motion (N={n})")
        plt.xlabel("Value")
        plt.ylabel("Frequency")
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        
        filename_hist = f"histogram_{n}.svg"
        plt.savefig(filename_hist)
        plt.close()
        print(f"  Saved {filename_hist}")
        
        # Part 3: Statistical Moments
        m1_mean = np.mean(series)
        m2_var = np.var(series)
        m3_skew = skew(series)
        # Fisher kurtosis (default in scipy is Fisher, which is excess kurtosis: Pearson - 3)
        m4_fisher = kurtosis(series, fisher=True)
        # Pearson kurtosis (Fisher + 3)
        m4_pearson = kurtosis(series, fisher=False)
        
        moments = pd.DataFrame({
            'moment': ['mean', 'variance', 'skewness', 'kurtosis_fisher', 'kurtosis_pearson'],
            'value': [m1_mean, m2_var, m3_skew, m4_fisher, m4_pearson]
        })
        
        filename_moments = f"moments_{n}.parquet"
        moments.to_parquet(filename_moments)
        print(f"  Saved {filename_moments}")

if __name__ == "__main__":
    main()
