"""
Hands-On 3 -- Time Series Models
Course: Computational Statistics -- INPE/MCTI
Student: Rian Koja

==============================================================================
Task iv -- Discussion: Spatio-Temporal Extension of the P-Model (STM-Model 2+1D)
==============================================================================

The 1D P-model of Meneveau and Sreenivasan (1987) is a hierarchical
multiplicative cascade: at each level n, each energy segment is split into two
sub-segments with weights p and (1-p), controlled by p in (0, 0.5). After N
levels, a series of 2^N points is obtained with multifractal behaviour --
self-similarity and statistical intermittency -- by construction.

EXTENSION TO THE STM-MODEL (2+1D)
-----------------------------------
The extension replaces the 1D vector with a three-dimensional field A(t, x, y),
where x and y are spatial dimensions and t is time. At each cascade level, every
voxel is expanded into 2x2x2 = 8 sub-voxels with weights determined by
independent choices of p along each axis (px, py, pz in {p, 1-p}), producing a
multifractal structure that is simultaneously:

  * self-similar in space (x, y): fluctuations at large scales determine the
    distribution at small scales through the same multiplicative rule;
  * evolving in time (t): the third cascade dimension generates emergent
    temporal correlation without explicit dynamics.

NEW PARAMETERS AND STRUCTURAL CHOICES
----------------------------------------
  1. Parameter p may differ per axis (px, py, pz), introducing directional
     anisotropy -- relevant for stratified atmospheric turbulence.
  2. A Gaussian filter of width sigma applied to the final field controls
     spatial roughness (post-cascade smoothing).
  3. The number of levels N sets the resolution: N=6 -> 64x64x64 field;
     N=8 -> 256x256x256 (cost grows as 8^N).

MODELABLE PHENOMENA AND LIMITATIONS
--------------------------------------
The STM-Model is suitable for: geophysical turbulence (ocean, atmosphere),
extreme precipitation with organized spatial structure, solar wind fields, and
any system exhibiting multifractal intermittency in space and time.

Limitations:
  (i)   No exact energy balance in 3D without additional normalisation;
  (ii)  Independence of p per axis ignores physical correlations between
        directions;
  (iii) Computational cost O(8^N) limits resolution on conventional hardware;
  (iv)  Temporal evolution is statistically stationary -- no propagating waves,
        advection, or explicit dynamics.
"""

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import stats
from scipy.stats import lognorm, gamma, weibull_min, norm, expon
from scipy.stats import kstest
from scipy.ndimage import gaussian_filter
from scipy.special import gamma as sp_gamma

# ==============================================================================
#  Global seed for full reproducibility
# ==============================================================================

SEED = 42
RNG = np.random.default_rng(SEED)

# ==============================================================================
#  P-model parameters
# ==============================================================================

N_ORDERS = 10  # 2^10 = 1024 points per series
N_SERIES = 10  # original series per class
N_AUG = 10  # augmented series per class

# Valid p ranges per class (Didier-Sornette / reference script)
P_ENDO_LO, P_ENDO_HI = 0.32, 0.42  # endogenous
P_EXO_LO, P_EXO_HI = 0.18, 0.28  # exogenous


# ==============================================================================
#  1D P-model functions
# ==============================================================================


def _next_step_1d(dx, p, rng):
    y2 = np.zeros(dx.size * 2)
    sign = np.sign(rng.random(dx.size) - 0.5)
    y2[0::2] = dx + sign * (1 - 2 * p) * dx
    y2[1::2] = dx - sign * (1 - 2 * p) * dx
    return y2


def pmodel_1d(n_orders, p, rng):
    """Generate a 1D P-model series with n_orders cascade levels."""
    dx = np.array([1.0])
    for _ in range(n_orders):
        dx = _next_step_1d(dx, p, rng)
    return dx[: 2**n_orders]


def _normalize(x):
    """Min-max normalisation with a positive shift to avoid zeros."""
    x = x - x.min() + 1e-6
    return x / (x.max() + 1e-8)


# ==============================================================================
#  Task i -- Generation of original series and data augmentation
# ==============================================================================


def task_i_augmentation():
    """
    Generate 10 original series per class and 10 augmented series per class,
    for a total of 40 series.

    Augmentation strategy (parametric perturbation):
        Values of p are sampled from a uniform distribution within the valid
        range of each class, with independent seeds derived from the global RNG.
        This preserves the multifractal structure while introducing statistical
        variability across replicates -- analogous to different physical
        realisations of the same turbulent process.
    """
    # Uniform p values within each class range
    p_endo_orig = RNG.uniform(P_ENDO_LO, P_ENDO_HI, N_SERIES)
    p_exo_orig = RNG.uniform(P_EXO_LO, P_EXO_HI, N_SERIES)
    p_endo_aug = RNG.uniform(P_ENDO_LO, P_ENDO_HI, N_AUG)
    p_exo_aug = RNG.uniform(P_EXO_LO, P_EXO_HI, N_AUG)

    def _gen(p_vals):
        series = []
        for p in p_vals:
            seed_i = int(RNG.integers(0, 2**31))
            s = _normalize(pmodel_1d(N_ORDERS, p, np.random.default_rng(seed_i)))
            series.append(s)
        return series

    ser_orig_endo = _gen(p_endo_orig)
    ser_orig_exo = _gen(p_exo_orig)
    ser_aug_endo = _gen(p_endo_aug)
    ser_aug_exo = _gen(p_exo_aug)

    return (
        ser_orig_endo,
        ser_orig_exo,
        ser_aug_endo,
        ser_aug_exo,
        p_endo_orig,
        p_exo_orig,
        p_endo_aug,
        p_exo_aug,
    )


# ==============================================================================
#  Task ii -- Cullen-Frey diagram
# ==============================================================================


def _moments(series_list):
    b1 = np.array([stats.skew(s) ** 2 for s in series_list])
    b2 = np.array([stats.kurtosis(s, fisher=True) for s in series_list])
    return b1, b2


def _cullen_frey_loci():
    """Theoretical loci in the (skewness^2, excess kurtosis) plane."""
    loci = {
        "Normal": ([0.0], [0.0]),
        "Uniform": ([0.0], [-1.2]),
        "Logistic": ([0.0], [1.2]),
        "Exponential": ([4.0], [6.0]),
    }

    # Lognormal: parametric curve in sigma
    sv = np.linspace(0.01, 3.0, 300)
    loci["Lognormal"] = (
        (np.exp(sv**2) - 1) * (np.exp(sv**2) + 2) ** 2,
        np.exp(4 * sv**2) + 2 * np.exp(3 * sv**2) + 3 * np.exp(2 * sv**2) - 6,
    )

    # Gamma: parametric curve in alpha (shape)
    av = np.linspace(0.1, 50, 500)
    loci["Gamma"] = (4.0 / av, 6.0 / av)

    # Weibull: parametric curve in k (shape)
    kv = np.linspace(0.5, 10, 500)
    m1 = sp_gamma(1 + 1 / kv)
    m2 = sp_gamma(1 + 2 / kv)
    m3 = sp_gamma(1 + 3 / kv)
    m4 = sp_gamma(1 + 4 / kv)
    var = m2 - m1**2
    sk = (m3 - 3 * m1 * m2 + 2 * m1**3) / (var**1.5 + 1e-12)
    ku = (m4 - 4 * m1 * m3 + 6 * m1**2 * m2 - 3 * m1**4) / (var**2 + 1e-12) - 3
    loci["Weibull"] = (sk**2, ku)

    return loci


def task_ii_cullen_frey(ser_orig_endo, ser_orig_exo, ser_aug_endo, ser_aug_exo):
    """
    Plot the Cullen-Frey diagram with all 40 series and theoretical loci.
    Saves 'cullen_frey.png'.
    """
    b1_oe, b2_oe = _moments(ser_orig_endo)
    b1_oo, b2_oo = _moments(ser_orig_exo)
    b1_ae, b2_ae = _moments(ser_aug_endo)
    b1_ao, b2_ao = _moments(ser_aug_exo)

    loci = _cullen_frey_loci()

    fig, ax = plt.subplots(figsize=(10, 7))

    loci_style = {
        "Normal": dict(color="black", marker="*", ls="none"),
        "Uniform": dict(color="gray", marker="s", ls="none"),
        "Logistic": dict(color="purple", marker="D", ls="none"),
        "Exponential": dict(color="brown", marker="p", ls="none"),
        "Lognormal": dict(color="blue", marker=None, ls="-"),
        "Gamma": dict(color="green", marker=None, ls="-"),
        "Weibull": dict(color="orange", marker=None, ls="-"),
    }

    for name, (b1l, b2l) in loci.items():
        b1l, b2l = np.asarray(b1l), np.asarray(b2l)
        st = loci_style[name]
        if st["marker"]:
            ax.scatter(
                b1l,
                b2l,
                marker=st["marker"],
                s=150,
                c=st["color"],
                zorder=5,
                label=name,
            )
        else:
            ax.plot(
                b1l, b2l, st["ls"], color=st["color"], lw=1.8, label=name, alpha=0.85
            )

    ax.scatter(
        b1_oe,
        b2_oe,
        c="crimson",
        marker="o",
        s=70,
        zorder=6,
        label="Endogenous -- original",
        alpha=0.85,
    )
    ax.scatter(
        b1_ae,
        b2_ae,
        c="crimson",
        marker="^",
        s=70,
        zorder=6,
        label="Endogenous -- augmented",
        alpha=0.85,
    )
    ax.scatter(
        b1_oo,
        b2_oo,
        c="steelblue",
        marker="o",
        s=70,
        zorder=6,
        label="Exogenous -- original",
        alpha=0.85,
    )
    ax.scatter(
        b1_ao,
        b2_ao,
        c="steelblue",
        marker="^",
        s=70,
        zorder=6,
        label="Exogenous -- augmented",
        alpha=0.85,
    )

    ax.set_xlabel("Skewness squared (b1 = skewness^2)")
    ax.set_ylabel("Excess kurtosis (b2)")
    ax.set_title("Cullen-Frey Diagram -- 40 P-model series")
    ax.legend(loc="upper right", fontsize=8, ncol=2, framealpha=0.9)
    ax.grid(alpha=0.3)

    all_b1 = np.concatenate([b1_oe, b1_oo, b1_ae, b1_ao])
    ax.set_xlim(-0.1, all_b1.max() * 1.25 + 0.3)

    plt.tight_layout()
    plt.savefig("cullen_frey.png", dpi=150)
    plt.close()
    print("cullen_frey.png saved.")

    # Median position to identify the best-fit PDF family
    b1_endo = np.median(np.concatenate([b1_oe, b1_ae]))
    b2_endo = np.median(np.concatenate([b2_oe, b2_ae]))
    b1_exo = np.median(np.concatenate([b1_oo, b1_ao]))
    b2_exo = np.median(np.concatenate([b2_oo, b2_ao]))

    print(f"  Median endogenous: b1={b1_endo:.3f}, b2={b2_endo:.3f}")
    print(f"  Median exogenous:  b1={b1_exo:.3f},  b2={b2_exo:.3f}")
    print("  -> Both classes lie in the Lognormal/Gamma region of the diagram.")

    return "lognorm", "lognorm"


# ==============================================================================
#  Task iii -- Fitting verification
# ==============================================================================

_DIST_MAP = {
    "lognorm": lognorm,
    "gamma": gamma,
    "weibull_min": weibull_min,
    "norm": norm,
    "expon": expon,
}
_DIST_COLORS = {
    "lognorm": "red",
    "gamma": "blue",
    "weibull_min": "orange",
    "norm": "green",
    "expon": "purple",
}
_FLOC0 = {"lognorm", "gamma", "weibull_min", "expon"}


def _fit_candidates(data, label):
    n = len(data)
    results = []
    for name, dist in _DIST_MAP.items():
        try:
            kw = {"floc": 0} if name in _FLOC0 else {}
            params = dist.fit(data, **kw)
            ll = np.sum(dist.logpdf(data, *params))
            k = len(params)
            aic = 2 * k - 2 * ll
            bic = k * np.log(n) - 2 * ll
            ks, p = kstest(data, dist.cdf, args=params)
            results.append(
                dict(dist=name, params=params, ks=ks, ks_p=p, aic=aic, bic=bic)
            )
        except Exception as exc:
            print(f"  Warning [{label}]: failed to fit {name}: {exc}")
    return sorted(results, key=lambda r: r["aic"])


def task_iii_fitting(ser_orig_endo, ser_orig_exo, ser_aug_endo, ser_aug_exo):
    """
    Compute the mean histogram for each class, fit distributions by MLE,
    and print the KS/AIC/BIC table. Saves 'fitting.png'.
    """
    data_endo = np.concatenate(ser_orig_endo + ser_aug_endo)
    data_exo = np.concatenate(ser_orig_exo + ser_aug_exo)

    res_endo = _fit_candidates(data_endo, "Endogenous")
    res_exo = _fit_candidates(data_exo, "Exogenous")

    # Goodness-of-fit table
    sep = "=" * 66
    for label, results in [
        ("Endogenous class (p in [0.32, 0.42])", res_endo),
        ("Exogenous class  (p in [0.18, 0.28])", res_exo),
    ]:
        print(f"\n{sep}")
        print(f"  {label}")
        print(sep)
        print(
            f"  {'Distribution':<14} {'KS':>8} {'KS p-val':>10} {'AIC':>12} {'BIC':>12}"
        )
        print(f"  {'-' * 60}")
        for r in results:
            print(
                f"  {r['dist']:<14} {r['ks']:>8.4f} {r['ks_p']:>10.4f}"
                f" {r['aic']:>12.1f} {r['bic']:>12.1f}"
            )

    # Figure
    n_bins = 60
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))

    for ax, data, results, title in [
        (axes[0], data_endo, res_endo, "Endogenous class (p in [0.32, 0.42])"),
        (axes[1], data_exo, res_exo, "Exogenous class  (p in [0.18, 0.28])"),
    ]:
        ax.hist(
            data,
            bins=n_bins,
            density=True,
            alpha=0.35,
            color="gray",
            label="Mean histogram",
        )
        x_plot = np.linspace(data.min() + 1e-9, data.max(), 500)
        for r in results:
            dist = _DIST_MAP[r["dist"]]
            y_pdf = dist.pdf(x_plot, *r["params"])
            ax.plot(
                x_plot,
                y_pdf,
                "-",
                lw=1.8,
                color=_DIST_COLORS[r["dist"]],
                label=f"{r['dist']} (AIC={r['aic']:.0f})",
            )
        ax.set_xlabel("Normalised amplitude")
        ax.set_ylabel("Probability density")
        ax.set_title(title)
        ax.legend(fontsize=7, framealpha=0.9)
        ax.grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig("fitting.png", dpi=150)
    plt.close()
    print("\nfitting.png saved.")

    # Consistency check: original vs. augmented (two-sample KS test)
    print("\n-- Consistency: original vs. augmented (two-sample KS test) --")
    for cls, orig, aug in [
        ("Endogenous", np.concatenate(ser_orig_endo), np.concatenate(ser_aug_endo)),
        ("Exogenous", np.concatenate(ser_orig_exo), np.concatenate(ser_aug_exo)),
    ]:
        ks2, p2 = stats.ks_2samp(orig, aug)
        verdict = "consistent (p > 0.05)" if p2 > 0.05 else "detectable difference"
        print(f"  {cls}: KS={ks2:.4f}, p={p2:.4f} -- {verdict}")


# ==============================================================================
#  STM-Model 2+1D -- helper functions and demo (Task iv)
# ==============================================================================


def _next_step_2d(field, p, rng):
    nx, ny, nz = field.shape
    nf = np.zeros((2 * nx, 2 * ny, 2 * nz))
    for i in range(nx):
        for j in range(ny):
            for k in range(nz):
                base = field[i, j, k]
                px = p if rng.random() < 0.5 else (1 - p)
                py = p if rng.random() < 0.5 else (1 - p)
                pz = p if rng.random() < 0.5 else (1 - p)
                w = 2 * np.array(
                    [
                        px * py * pz,
                        px * py * (1 - pz),
                        px * (1 - py) * pz,
                        px * (1 - py) * (1 - pz),
                        (1 - px) * py * pz,
                        (1 - px) * py * (1 - pz),
                        (1 - px) * (1 - py) * pz,
                        (1 - px) * (1 - py) * (1 - pz),
                    ]
                )
                idx = 0
                for di in range(2):
                    for dj in range(2):
                        for dk in range(2):
                            nf[2 * i + di, 2 * j + dj, 2 * k + dk] = base * w[idx]
                            idx += 1
    return nf


def stm_model(n_orders=5, p=0.5, sigma=1.0, rng=None):
    """Generate a 2+1D spatio-temporal STM-Model field with n_orders levels."""
    if rng is None:
        rng = np.random.default_rng()
    field = np.ones((1, 1, 1))
    for _ in range(n_orders):
        field = _next_step_2d(field, p, rng)
    if sigma > 0:
        field = gaussian_filter(field, sigma=sigma)
    return field


def task_iv_stm_demo():
    """
    STM-Model 2+1D demo: generate exogenous and endogenous fields and save
    the highest-intensity frame of each to 'stm_example.png'.
    """
    print("  Generating exogenous  STM-Model field (n=5, p=0.20)...")
    f_exo = stm_model(5, p=0.20, sigma=1.0, rng=np.random.default_rng(SEED + 10))
    print("  Generating endogenous STM-Model field (n=5, p=0.40)...")
    f_endo = stm_model(5, p=0.40, sigma=1.0, rng=np.random.default_rng(SEED + 11))

    def norm01(f):
        return (f - f.min()) / (f.max() - f.min() + 1e-12)

    fe, fn = norm01(f_exo), norm01(f_endo)
    best_exo = int(np.argmax(fe.max(axis=(0, 1))))
    best_endo = int(np.argmax(fn.max(axis=(0, 1))))

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    im1 = axes[0].imshow(
        fe[:, :, best_exo], cmap="inferno", origin="lower", vmin=0, vmax=1
    )
    axes[0].set_title(f"STM-Model -- Exogenous (p=0.20), frame t={best_exo}")
    plt.colorbar(im1, ax=axes[0])

    im2 = axes[1].imshow(
        fn[:, :, best_endo], cmap="inferno", origin="lower", vmin=0, vmax=1
    )
    axes[1].set_title(f"STM-Model -- Endogenous (p=0.40), frame t={best_endo}")
    plt.colorbar(im2, ax=axes[1])

    plt.tight_layout()
    plt.savefig("stm_example.png", dpi=150)
    plt.close()
    print("  stm_example.png saved.")


# ==============================================================================
#  Main entry point
# ==============================================================================


def main():
    print("=" * 66)
    print("  Hands-On 3 -- P-model and Spatio-Temporal Extension")
    print("  INPE/MCTI -- Computational Statistics")
    print("=" * 66)

    print("\n[Task i] Data generation and augmentation...")
    (ser_orig_endo, ser_orig_exo, ser_aug_endo, ser_aug_exo, p_oe, p_oo, p_ae, p_ao) = (
        task_i_augmentation()
    )
    print(
        f"  Original   -- Endogenous: {len(ser_orig_endo)}, "
        f"Exogenous: {len(ser_orig_exo)}"
    )
    print(
        f"  Augmented  -- Endogenous: {len(ser_aug_endo)}, "
        f"Exogenous: {len(ser_aug_exo)}"
    )
    print(
        f"  Total: {len(ser_orig_endo) + len(ser_orig_exo) + len(ser_aug_endo) + len(ser_aug_exo)} series"
    )

    print("\n[Task ii] Cullen-Frey diagram...")
    pdf_endo, pdf_exo = task_ii_cullen_frey(
        ser_orig_endo, ser_orig_exo, ser_aug_endo, ser_aug_exo
    )

    print("\n[Task iii] MLE fitting verification...")
    task_iii_fitting(ser_orig_endo, ser_orig_exo, ser_aug_endo, ser_aug_exo)

    print("\n[Task iv] STM-Model (2+1D) demo...")
    task_iv_stm_demo()

    print("\n" + "=" * 66)
    print("  Completed successfully.")
    print("=" * 66)


if __name__ == "__main__":
    main()
