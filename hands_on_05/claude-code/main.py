"""Hands-on 05 - PSD, DFA and spectral exponents for colored noises.

Generates white, pink and red noise; computes Power Spectral Density (PSD)
and Detrended Fluctuation Analysis (DFA); estimates the spectral exponents
beta (from PSD) and alpha (from DFA); and validates the theoretical relation
beta = 2*alpha - 1.

All artifacts are written to the ``outputs`` directory next to this file.
Run with::

    uv run main.py
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.signal import welch

# --------------------------------------------------------------------------- #
# Global configuration
# --------------------------------------------------------------------------- #
SEED = 417
N = 2 ** 14          # 16384 samples
FS = 1.0             # unit sampling rate (cycles per sample)
NPERSEG = 1024       # Welch segment length
HERE = Path(__file__).resolve().parent
OUTPUTS = HERE / "outputs"

# Theoretical spectral exponent beta for each noise type.
THEORY_BETA = {"white": 0.0, "pink": 1.0, "red": 2.0}


# --------------------------------------------------------------------------- #
# 1. Colored noise generation
# --------------------------------------------------------------------------- #
def white_noise(n: int) -> np.ndarray:
    """Standard normal white noise (beta approx 0)."""
    return np.random.normal(0.0, 1.0, n)


def colored_noise(n: int, beta: float) -> np.ndarray:
    """Frequency-domain colored noise with amplitude spectrum ~ 1/f^(beta/2).

    A complex Gaussian spectrum is shaped by ``1 / f**(beta/2)`` on the
    real-FFT frequency grid, the DC (and Nyquist imaginary) components are
    forced so that the inverse real FFT yields a strictly real-valued
    series, and the result is normalized to zero mean and unit variance.
    """
    freqs = np.fft.rfftfreq(n, d=1.0 / FS)          # 0 .. FS/2
    scale = np.zeros_like(freqs)
    scale[1:] = 1.0 / (freqs[1:] ** (beta / 2.0))   # skip DC to avoid /0
    scale[0] = 0.0                                   # remove DC offset

    real_part = np.random.normal(0.0, 1.0, freqs.size)
    imag_part = np.random.normal(0.0, 1.0, freqs.size)
    spectrum = (real_part + 1j * imag_part) * scale

    # Hermitian-consistent endpoints for a real inverse transform.
    spectrum[0] = 0.0
    if n % 2 == 0:
        spectrum[-1] = spectrum[-1].real

    series = np.fft.irfft(spectrum, n=n)
    series -= series.mean()
    std = series.std()
    if std > 0:
        series /= std
    return series


def pink_noise(n: int) -> np.ndarray:
    """Pink (1/f) noise: frequency-domain construction with beta = 1."""
    return colored_noise(n, beta=1.0)


def red_noise(n: int) -> np.ndarray:
    """Red / Brownian noise: frequency-domain construction with beta = 2.

    Equivalent in spectral slope to a cumulative sum of white noise, but the
    frequency-domain route keeps the construction identical to pink noise.
    """
    return colored_noise(n, beta=2.0)


# --------------------------------------------------------------------------- #
# 2. Power Spectral Density
# --------------------------------------------------------------------------- #
def compute_psd(x: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Welch PSD with a Hann window and fixed segment length."""
    f, pxx = welch(x, fs=FS, window="hann", nperseg=NPERSEG)
    return f, pxx


# --------------------------------------------------------------------------- #
# 3. Detrended Fluctuation Analysis
# --------------------------------------------------------------------------- #
def compute_dfa(
    x: np.ndarray,
    s_min: int = 16,
    n_scales: int = 20,
    min_windows: int = 4,
) -> tuple[np.ndarray, np.ndarray]:
    """DFA-1 fluctuation function F(s) over logarithmically spaced scales."""
    x = np.asarray(x, dtype=np.float64)
    profile = np.cumsum(x - x.mean())

    s_max = len(x) // 4
    scales = np.unique(
        np.logspace(np.log10(s_min), np.log10(s_max), n_scales).astype(int)
    )

    used_scales: list[int] = []
    fluct: list[float] = []
    for s in scales:
        n_windows = len(profile) // s
        if n_windows < min_windows:
            continue
        segments = profile[: n_windows * s].reshape(n_windows, s)
        t = np.arange(s)
        # Least-squares linear detrend within each non-overlapping window.
        coeffs = np.polyfit(t, segments.T, 1)
        trend = np.polyval(coeffs, t[:, None]).T
        msd = np.mean((segments - trend) ** 2, axis=1)
        used_scales.append(int(s))
        fluct.append(float(np.sqrt(np.mean(msd))))

    return np.asarray(used_scales, dtype=np.float64), np.asarray(fluct)


# --------------------------------------------------------------------------- #
# 4. Log-log least-squares fit
# --------------------------------------------------------------------------- #
def loglog_fit(x: np.ndarray, y: np.ndarray) -> tuple[float, float]:
    """Fit log10(y) = a + k*log10(x); return (slope k, intercept a)."""
    mask = (x > 0) & (y > 0) & np.isfinite(x) & np.isfinite(y)
    lx = np.log10(x[mask])
    ly = np.log10(y[mask])
    k, a = np.polyfit(lx, ly, 1)
    return float(k), float(a)


# --------------------------------------------------------------------------- #
# 5. Plotting helpers
# --------------------------------------------------------------------------- #
def plot_psd(f, pxx, beta, noise: str, path: Path) -> None:
    fig, ax = plt.subplots(figsize=(7, 5))
    pos = f > 0
    ax.loglog(f[pos], pxx[pos], color="tab:blue", lw=1.2, label="PSD (Welch)")
    lx = np.log10(f[pos])
    fit_line = 10 ** (np.polyval([-beta, np.log10(pxx[pos][0]) + beta * lx[0]], lx))
    ax.loglog(f[pos], fit_line, "r--", lw=1.5, label=f"fit slope = {-beta:.3f}")
    ax.set_xlabel("Frequency [cycles/sample]")
    ax.set_ylabel("PSD")
    ax.set_title(f"PSD - {noise} noise (beta = {beta:.3f})")
    ax.legend()
    ax.grid(True, which="both", ls=":", alpha=0.5)
    fig.tight_layout()
    fig.savefig(path, dpi=300)
    plt.close(fig)


def plot_dfa(s, fvals, alpha, noise: str, path: Path) -> None:
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.loglog(s, fvals, "o-", color="tab:green", ms=5, label="F(s)")
    ls = np.log10(s)
    intercept = np.log10(fvals[0]) - alpha * ls[0]
    ax.loglog(s, 10 ** (alpha * ls + intercept), "r--", lw=1.5,
              label=f"fit slope = {alpha:.3f}")
    ax.set_xlabel("Scale s")
    ax.set_ylabel("Fluctuation F(s)")
    ax.set_title(f"DFA - {noise} noise (alpha = {alpha:.3f})")
    ax.legend()
    ax.grid(True, which="both", ls=":", alpha=0.5)
    fig.tight_layout()
    fig.savefig(path, dpi=300)
    plt.close(fig)


def plot_relation(exponents: pd.DataFrame, path: Path) -> None:
    fig, ax = plt.subplots(figsize=(7, 5))
    x = 2 * exponents["alpha"] - 1
    y = exponents["beta"]
    lim = [min(x.min(), y.min()) - 0.3, max(x.max(), y.max()) + 0.3]
    ax.plot(lim, lim, "k--", alpha=0.6, label="beta = 2*alpha - 1")
    for _, row in exponents.iterrows():
        ax.scatter(2 * row["alpha"] - 1, row["beta"], s=90,
                   label=f"{row['noise_type']} (delta = "
                         f"{row['delta_beta_2alpha_minus_1']:+.3f})")
    ax.set_xlabel("2*alpha - 1")
    ax.set_ylabel("beta")
    ax.set_title("Theoretical relation: beta vs 2*alpha - 1")
    ax.set_xlim(lim)
    ax.set_ylim(lim)
    ax.legend()
    ax.grid(True, ls=":", alpha=0.5)
    fig.tight_layout()
    fig.savefig(path, dpi=300)
    plt.close(fig)


# --------------------------------------------------------------------------- #
# 6. Main pipeline
# --------------------------------------------------------------------------- #
def main() -> None:
    np.random.seed(SEED)
    OUTPUTS.mkdir(exist_ok=True)

    # Generate the three colored noises (draw order fixed by the seed).
    series = {
        "white": white_noise(N),
        "pink": pink_noise(N),
        "red": red_noise(N),
    }

    exponent_rows = []
    for noise, x in series.items():
        # --- PSD ---
        f, pxx = compute_psd(x)
        pos = f > 0
        # Fit excluding DC; trim the noisiest extreme bins.
        f_fit, p_fit = f[pos], pxx[pos]
        lo = max(1, int(0.01 * f_fit.size))
        hi = int(0.90 * f_fit.size)
        k_psd, _ = loglog_fit(f_fit[lo:hi], p_fit[lo:hi])
        beta = -k_psd

        psd_df = pd.DataFrame(
            {
                "frequency": f[pos],
                "psd": pxx[pos],
                "log10_frequency": np.log10(f[pos]),
                "log10_psd": np.log10(pxx[pos]),
            }
        )
        psd_df.to_parquet(OUTPUTS / f"psd_{noise}.parquet", index=False)
        plot_psd(f, pxx, beta, noise, OUTPUTS / f"psd_{noise}.png")

        # --- DFA ---
        s, fvals = compute_dfa(x)
        alpha, _ = loglog_fit(s, fvals)

        dfa_df = pd.DataFrame(
            {
                "scale": s,
                "F": fvals,
                "log10_scale": np.log10(s),
                "log10_F": np.log10(fvals),
            }
        )
        dfa_df.to_parquet(OUTPUTS / f"dfa_{noise}.parquet", index=False)
        plot_dfa(s, fvals, alpha, noise, OUTPUTS / f"dfa_{noise}.png")

        delta = beta - (2.0 * alpha - 1.0)
        exponent_rows.append(
            {
                "noise_type": noise,
                "beta": beta,
                "alpha": alpha,
                "delta_beta_2alpha_minus_1": delta,
            }
        )
        print(
            f"{noise:>5s}: beta={beta:+.4f} (theory {THEORY_BETA[noise]:+.1f})"
            f"  alpha={alpha:+.4f}  delta={delta:+.4f}"
        )

    exponents = pd.DataFrame(exponent_rows)
    exponents.to_parquet(OUTPUTS / "exponents.parquet", index=False)
    plot_relation(exponents, OUTPUTS / "psd_dfa_relation.png")

    print(f"\nAll outputs written to: {OUTPUTS}")


if __name__ == "__main__":
    main()
