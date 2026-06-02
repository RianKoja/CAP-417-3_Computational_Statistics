import os
import numpy as np
import scipy.signal as signal
import pandas as pd
import matplotlib.pyplot as plt

# 1. Initialization and Setup
SEED = 417
np.random.seed(SEED)
N = 2**14
FS = 1.0
OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def generate_white_noise(n):
    return np.random.normal(0.0, 1.0, n)

def generate_pink_noise(n):
    # Frequency domain construction
    f = np.fft.rfftfreq(n)
    white_noise = np.random.normal(0.0, 1.0, len(f))
    # 1/f^beta with beta=1 => 1/sqrt(f) amplitude
    # Avoid div by zero
    magnitudes = np.where(f == 0, 0, 1.0 / np.sqrt(f))
    complex_spectrum = white_noise * magnitudes
    return np.fft.irfft(complex_spectrum, n=n)

def generate_red_noise(n):
    # Cumulative sum of white noise
    white = np.random.normal(0.0, 1.0, n)
    return np.cumsum(white)

# 2. PSD Calculation
def compute_psd(x, fs):
    f, Pxx = signal.welch(x, fs=fs, window='hann', nperseg=1024)
    # Exclude DC component for fitting
    mask = f > 0
    return f[mask], Pxx[mask]

# 3. DFA Calculation
def compute_dfa(x):
    n = len(x)
    # Profile
    y = np.cumsum(x - np.mean(x))
    # Scales
    s_min = 16
    s_max = n // 4
    scales = np.unique(np.geomspace(s_min, s_max, 20).astype(int))
    
    fluctuations = []
    for s in scales:
        # Divide into windows
        num_windows = n // s
        y_segments = y[:num_windows * s].reshape(num_windows, s)
        
        # Detrending
        x_axis = np.arange(s)
        detrended_sq_sums = []
        for i in range(num_windows):
            coeffs = np.polyfit(x_axis, y_segments[i], 1)
            trend = np.polyval(coeffs, x_axis)
            detrended = y_segments[i] - trend
            detrended_sq_sums.append(np.mean(detrended**2))
        
        fluctuations.append(np.sqrt(np.mean(detrended_sq_sums)))
        
    return scales, np.array(fluctuations)

# 4. Fitting
def fit_power_law(x, y):
    # Log-log
    log_x = np.log10(x)
    log_y = np.log10(y)
    slope, intercept = np.polyfit(log_x, log_y, 1)
    return slope, intercept

def main():
    noises = {
        "white": generate_white_noise(N),
        "pink": generate_pink_noise(N),
        "red": generate_red_noise(N)
    }
    
    results = []
    
    for name, series in noises.items():
        # PSD
        f, Pxx = compute_psd(series, FS)
        beta_slope, _ = fit_power_law(f, Pxx)
        beta = -beta_slope
        
        # Parquet PSD
        psd_df = pd.DataFrame({
            "frequency": f,
            "psd": Pxx,
            "log10_frequency": np.log10(f),
            "log10_psd": np.log10(Pxx)
        })
        psd_df.to_parquet(os.path.join(OUTPUT_DIR, f"psd_{name}.parquet"))
        
        # DFA
        s, F = compute_dfa(series)
        alpha, _ = fit_power_law(s, F)
        
        # Parquet DFA
        dfa_df = pd.DataFrame({
            "scale": s,
            "F": F,
            "log10_scale": np.log10(s),
            "log10_F": np.log10(F)
        })
        dfa_df.to_parquet(os.path.join(OUTPUT_DIR, f"dfa_{name}.parquet"))
        
        results.append({
            "noise_type": name,
            "beta": beta,
            "alpha": alpha,
            "delta_beta_2alpha_minus_1": beta - (2 * alpha - 1)
        })
        
        # Plots
        plt.figure()
        plt.loglog(f, Pxx, label="PSD")
        plt.title(f"{name.capitalize()} Noise PSD (beta≈{beta:.2f})")
        plt.xlabel("Frequency")
        plt.ylabel("PSD")
        plt.savefig(os.path.join(OUTPUT_DIR, f"psd_{name}.png"), dpi=300)
        plt.close()
        
        plt.figure()
        plt.loglog(s, F, label="Fluctuation")
        plt.title(f"{name.capitalize()} Noise DFA (alpha≈{alpha:.2f})")
        plt.xlabel("Scale")
        plt.ylabel("F(s)")
        plt.savefig(os.path.join(OUTPUT_DIR, f"dfa_{name}.png"), dpi=300)
        plt.close()
        
    exponents_df = pd.DataFrame(results)
    exponents_df.to_parquet(os.path.join(OUTPUT_DIR, "exponents.parquet"))
    
    # Summary Plot
    plt.figure()
    for res in results:
        plt.scatter(res["alpha"], res["beta"], label=res["noise_type"])
    plt.plot([0, 1.5], [1, 2], 'k--', label="Beta = 2Alpha - 1")
    plt.xlabel("Alpha (DFA)")
    plt.ylabel("Beta (PSD)")
    plt.legend()
    plt.title("PSD-DFA Relation")
    plt.savefig(os.path.join(OUTPUT_DIR, "psd_dfa_relation.png"), dpi=300)
    plt.close()

if __name__ == "__main__":
    main()
