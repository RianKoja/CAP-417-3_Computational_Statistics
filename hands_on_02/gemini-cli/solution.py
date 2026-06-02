"""
Hands-on 02 — CAP 417 — Part C: Structure, Randomness, and the Cullen-Frey-Pearson Space.
Author: Antigravity AI
Date: 2026-04-26
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from scipy.signal import correlate
import os

# =============================================================================
# CONSTANTS & CONFIGURATION
# =============================================================================
SEED = 42
N_POINTS = 1000
N_REALIZATIONS = 100
BETA_WHITE = 0.0
BETA_PINK = 1.0
BETA_RED = 2.0

# Set global seed for reproducibility
np.random.seed(SEED)

# Ensure output directories exist
os.makedirs('figures', exist_ok=True)
os.makedirs('results', exist_ok=True)

# Helper for ACF
def compute_acf(series):
    """Compute normalized Autocorrelation Function."""
    n = len(series)
    # Mean subtract
    data = series - np.mean(series)
    # Correlate
    acf = correlate(data, data, mode='full')
    acf = acf[n-1:]  # Keep only positive lags
    acf = acf / acf[0]  # Normalize
    return acf

# =============================================================================
# PART 2.1 — SHUFFLE ANALYSIS
# =============================================================================
print("Running Part 2.1: Shuffle Analysis...")

# 1. Generate Brownian (red noise) time series
# Brownian noise is the cumulative sum of white noise (Gaussian increments)
increments = np.random.normal(0, 1, N_POINTS)
brownian_series = np.cumsum(increments)

# 2. Create shuffled version
shuffled_series = np.random.permutation(brownian_series)

# 3. Compute statistical moments
def get_moments(data, label):
    m = np.mean(data)
    v = np.var(data)
    s = stats.skew(data)
    # Using Pearson's Kurtosis (raw) to match K=3 Gaussian reference
    k = stats.kurtosis(data, fisher=False) 
    return {
        'Series': label,
        'Mean': m,
        'Variance': v,
        'Skewness': s,
        'Kurtosis (Raw)': k
    }

moments_orig = get_moments(brownian_series, 'Original (Brownian)')
moments_shuf = get_moments(shuffled_series, 'Shuffled')

# 4. Print comparison table
df_moments = pd.DataFrame([moments_orig, moments_shuf])
print("\nComparison of Statistical Moments:")
print(df_moments.to_string(index=False))

# Save table to CSV
df_moments.to_csv('results/moments_table.csv', index=False)

# 5. Plotting
# Time series plot
plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
plt.plot(brownian_series, label='Original (Brownian)', alpha=0.8, color='#ff7f0e')
plt.plot(shuffled_series, label='Shuffled', alpha=0.6, color='#1f77b4')
plt.title('Time Series Comparison')
plt.xlabel('Time')
plt.ylabel('Value')
plt.legend()
plt.grid(True, alpha=0.3)

plt.subplot(1, 2, 2)
plt.hist(brownian_series, bins=30, alpha=0.5, label='Original', density=True, color='#ff7f0e')
plt.hist(shuffled_series, bins=30, alpha=0.5, label='Shuffled', density=True, color='#1f77b4')
plt.title('Distribution (Histogram)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('figures/fig_2_1_series.png', dpi=150)
plt.close()

# ACF Plot
acf_orig = compute_acf(brownian_series)
acf_shuf = compute_acf(shuffled_series)
lags = np.arange(len(acf_orig))

plt.figure(figsize=(10, 5))
plt.plot(lags, acf_orig, label='Original (Brownian)', color='#ff7f0e')
plt.plot(lags, acf_shuf, label='Shuffled', color='#1f77b4')
plt.axhline(0, color='black', linestyle='--', alpha=0.5)
plt.title('Autocorrelation Function (ACF)')
plt.xlabel('Lag')
plt.ylabel('Autocorrelation')
plt.legend()
plt.grid(True, alpha=0.3)
plt.xlim(0, 200) # Zoom in on first 200 lags for clarity
plt.savefig('figures/fig_2_1_acf.png', dpi=150)
plt.close()

# Optional: Moments table as figure
fig, ax = plt.subplots(figsize=(6, 2))
ax.axis('off')
ax.table(cellText=df_moments.values, colLabels=df_moments.columns, loc='center')
plt.title('Statistical Moments Comparison')
plt.savefig('figures/fig_2_1_moments.png', dpi=150, bbox_inches='tight')
plt.close()

"""
Part 2.1 Analysis:
- Do the moment values change after shuffling?
  The moments (Mean, Variance, Skewness, Kurtosis) remain identical (or nearly identical due to floating point precision).
  This is because these moments are calculated from the marginal distribution of the data points, which is preserved 
  during a random permutation.

- What does this indicate about temporal dependence vs. marginal distribution?
  Shuffling completely destroys the temporal dependence (the order of points), as evidenced by the ACF plot 
  where the shuffled series shows near-zero correlation for all lags > 0. However, the marginal distribution 
  is invariant to shuffling.

- Does shuffling preserve the distribution?
  Yes, shuffling preserves the marginal distribution (the set of values remains the same). However, it does 
  not preserve the "structure" or joint distribution of the time series.
"""

# =============================================================================
# PART 2.2 — COLORED NOISE GENERATION
# =============================================================================
print("\nRunning Part 2.2: Colored Noise Generation...")

def generate_colored_noise(N, beta, seed=None):
    """
    Generates noise with a power spectrum proportional to f^-beta.
    """
    if seed is not None:
        np.random.seed(seed)
    
    # 1. Generate white noise
    white = np.random.normal(0, 1, N)
    
    # 2. Compute FFT
    X = np.fft.fft(white)
    freqs = np.fft.fftfreq(N)
    
    # 3. Multiply by f^(-beta/2)
    # Amplitude scaling factor
    # Handle DC component (freq=0) to avoid division by zero
    # We use absolute frequency for the scaling
    s_filter = np.zeros(N)
    with np.errstate(divide='ignore', invalid='ignore'):
        s_filter = np.power(np.abs(freqs), -beta/2.0)
    
    # Set DC component to 0 (or keep it if beta=0)
    s_filter[0] = 0 if beta > 0 else 1.0
    
    X_colored = X * s_filter
    
    # 4. Inverse FFT
    colored_noise = np.fft.ifft(X_colored).real
    
    # Normalize to zero mean and unit variance for consistency
    colored_noise = (colored_noise - np.mean(colored_noise)) / np.std(colored_noise)
    
    return colored_noise

# Generate 100 realizations for each beta
noises = {
    'White (beta=0)': (BETA_WHITE, []),
    'Pink (beta=1)': (BETA_PINK, []),
    'Red (beta=2)': (BETA_RED, [])
}

noise_data_list = []

for label, (beta, realizations) in noises.items():
    for i in range(N_REALIZATIONS):
        # Use i as seed offset for independence but reproducibility
        noise = generate_colored_noise(N_POINTS, beta, seed=SEED + i + int(beta*1000))
        realizations.append(noise)
        
        # Compute moments for Part 2.3
        s = stats.skew(noise)
        k = stats.kurtosis(noise, fisher=False)
        noise_data_list.append({
            'Type': label,
            'Beta': beta,
            'Realization': i,
            'Skewness': s,
            'Kurtosis': k,
            'SkewnessSq': s**2
        })

df_noise_moments = pd.DataFrame(noise_data_list)
df_noise_moments.to_csv('results/noise_moments.csv', index=False)

# Plot example realizations
plt.figure(figsize=(12, 8))
colors = ['#1f77b4', '#e377c2', '#d62728']
for i, (label, (beta, realizations)) in enumerate(noises.items()):
    plt.subplot(3, 1, i+1)
    plt.plot(realizations[0], color=colors[i], lw=1)
    plt.title(f'Example: {label}')
    plt.grid(True, alpha=0.3)
    if i == 2: plt.xlabel('Sample index')
plt.tight_layout()
plt.savefig('figures/fig_2_2_examples.png', dpi=150)
plt.close()

# =============================================================================
# PART 2.3 — CULLEN-FREY-PEARSON PLOT
# =============================================================================
print("\nRunning Part 2.3: Cullen-Frey-Pearson Plot...")

plt.style.use('dark_background')
plt.figure(figsize=(10, 8))

# Define colors for the plot
plot_colors = {
    'White (beta=0)': '#00ffcc',
    'Pink (beta=1)': '#ff00ff',
    'Red (beta=2)': '#ffff00'
}

for label, color in plot_colors.items():
    subset = df_noise_moments[df_noise_moments['Type'] == label]
    plt.scatter(subset['SkewnessSq'], subset['Kurtosis'], 
                alpha=0.6, label=label, color=color, s=40, edgecolors='white', linewidth=0.5)

# Mark Gaussian reference point (S^2=0, K=3)
plt.scatter([0], [3], color='red', marker='X', s=200, label='Gaussian (S²=0, K=3)', zorder=5)
plt.annotate('Gaussian', (0, 3), xytext=(0.5, 3.2), fontsize=12, fontweight='bold', color='red')

# Formatting
plt.xlabel('Skewness² ($S^2$)', fontsize=12)
plt.ylabel('Kurtosis ($K$)', fontsize=12)
plt.title('Cullen-Frey-Pearson Space', fontsize=14, pad=20)
plt.legend(frameon=True, facecolor='black', edgecolor='white')
plt.grid(True, linestyle='--', alpha=0.4)

# Set limits to see the clusters clearly
plt.xlim(-0.1, max(df_noise_moments['SkewnessSq']) * 1.2)
plt.ylim(min(df_noise_moments['Kurtosis']) * 0.8, max(df_noise_moments['Kurtosis']) * 1.2)

plt.savefig('figures/fig_2_3_cullen_frey.png', dpi=150)
plt.close()

print("\nAll tasks completed successfully.")
print("Results saved in 'results/' and 'figures/'.")
