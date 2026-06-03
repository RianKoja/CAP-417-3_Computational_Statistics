"""Hands-on 03 — Multimodality, KDE, and Cullen-Frey-Pearson space.

Runs end-to-end: generates 10 synthetic signals, KDE diagnostic figures,
the Cullen-Frey-Pearson diagram (with bootstrap), and the support figures
listed in CLAUDE.md. All artefacts are written to ./outputs/.
"""

from __future__ import annotations

import os
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns  # noqa: F401  (allowed dependency per spec)
from scipy import stats

SEED = 42
N_SAMPLES = 5000
N_BOOTSTRAP = 30
OUTPUT_DIR = Path("outputs")

SIGNAL_ORDER = [
    "gaussian",
    "bimodal_equal",
    "bimodal_unequal",
    "bimodal_overlap",
    "trimodal",
    "asymmetric",
    "laplace_mix",
    "heavy_tail",
    "multimodal_4",
    "asymmetric_laplace",
]

SIGNAL_SPECS: dict[str, list[dict]] = {
    "gaussian": [{"type": "gaussian", "loc": 0.0, "scale": 1.0, "weight": 1.0}],
    "bimodal_equal": [
        {"type": "gaussian", "loc": -3.0, "scale": 1.0, "weight": 0.5},
        {"type": "gaussian", "loc": 3.0, "scale": 1.0, "weight": 0.5},
    ],
    "bimodal_unequal": [
        {"type": "gaussian", "loc": -3.0, "scale": 1.0, "weight": 0.7},
        {"type": "gaussian", "loc": 3.0, "scale": 0.8, "weight": 0.3},
    ],
    "bimodal_overlap": [
        {"type": "gaussian", "loc": -1.0, "scale": 1.0, "weight": 0.5},
        {"type": "gaussian", "loc": 1.0, "scale": 1.0, "weight": 0.5},
    ],
    "trimodal": [
        {"type": "gaussian", "loc": -5.0, "scale": 0.8, "weight": 0.3},
        {"type": "gaussian", "loc": 0.0, "scale": 1.0, "weight": 0.4},
        {"type": "gaussian", "loc": 5.0, "scale": 0.8, "weight": 0.3},
    ],
    "asymmetric": [
        {"type": "skewnorm", "loc": 0.0, "scale": 2.0, "skew": 8.0, "weight": 1.0},
    ],
    "laplace_mix": [
        {"type": "laplace", "loc": 0.0, "scale": 1.0, "weight": 0.5},
        {"type": "gaussian", "loc": 4.0, "scale": 0.5, "weight": 0.5},
    ],
    "multimodal_4": [
        {"type": "gaussian", "loc": -6.0, "scale": 0.7, "weight": 0.25},
        {"type": "gaussian", "loc": -2.0, "scale": 0.7, "weight": 0.25},
        {"type": "gaussian", "loc": 2.0, "scale": 0.7, "weight": 0.25},
        {"type": "gaussian", "loc": 6.0, "scale": 0.7, "weight": 0.25},
    ],
    "asymmetric_laplace": [
        {"type": "laplace", "loc": 2.0, "scale": 1.0, "weight": 1.0},
    ],
}

SIGNAL_STYLE: dict[str, tuple[str, str]] = {
    "gaussian": ("#2196F3", "o"),
    "bimodal_equal": ("#E91E63", "s"),
    "bimodal_unequal": ("#9C27B0", "D"),
    "bimodal_overlap": ("#FF5722", "^"),
    "trimodal": ("#4CAF50", "v"),
    "asymmetric": ("#FF9800", "<"),
    "laplace_mix": ("#009688", ">"),
    "heavy_tail": ("#795548", "p"),
    "multimodal_4": ("#607D8B", "h"),
    "asymmetric_laplace": ("#F44336", "*"),
}

TRUE_MODES: dict[str, list[float]] = {
    "bimodal_equal": [-3.0, 3.0],
    "trimodal": [-5.0, 0.0, 5.0],
    "multimodal_4": [-6.0, -2.0, 2.0, 6.0],
}


# ---------------------------------------------------------------------------
# Part 3.1 — Mixture generation
# ---------------------------------------------------------------------------


def generate_mixture(n: int, modes: list[dict], seed: int = SEED) -> np.ndarray:
    """Sample ``n`` points from an arbitrary mixture of named components."""
    rng = np.random.default_rng(seed)
    weights = np.array([m["weight"] for m in modes], dtype=float)
    weights = weights / weights.sum()

    component_idx = rng.choice(len(modes), size=n, p=weights)
    samples = np.empty(n, dtype=float)

    for i, mode in enumerate(modes):
        mask = component_idx == i
        k = int(mask.sum())
        if k == 0:
            continue
        sub_seed = int(rng.integers(0, 2**31 - 1))
        kind = mode["type"]
        loc = mode["loc"]
        scale = mode["scale"]
        if kind == "gaussian":
            samples[mask] = stats.norm(loc=loc, scale=scale).rvs(k, random_state=sub_seed)
        elif kind == "laplace":
            samples[mask] = stats.laplace(loc=loc, scale=scale).rvs(k, random_state=sub_seed)
        elif kind == "skewnorm":
            samples[mask] = stats.skewnorm(
                a=mode["skew"], loc=loc, scale=scale
            ).rvs(k, random_state=sub_seed)
        else:
            raise ValueError(f"Unknown component type: {kind!r}")
    return samples


def generate_all_signals() -> dict[str, np.ndarray]:
    signals: dict[str, np.ndarray] = {}
    for name in SIGNAL_ORDER:
        if name == "heavy_tail":
            signals[name] = stats.t(df=2).rvs(N_SAMPLES, random_state=SEED)
        else:
            signals[name] = generate_mixture(N_SAMPLES, SIGNAL_SPECS[name], seed=SEED)
    return signals


def save_signals(signals: dict[str, np.ndarray]) -> Path:
    df = pd.DataFrame({"index": np.arange(N_SAMPLES, dtype=np.int64)})
    for name in SIGNAL_ORDER:
        df[name] = signals[name]
    path = OUTPUT_DIR / "signals.parquet"
    df.to_parquet(path, index=False)
    return path


def save_signal_stats(signals: dict[str, np.ndarray]) -> Path:
    rows = []
    for name in SIGNAL_ORDER:
        x = signals[name]
        rows.append(
            {
                "signal": name,
                "mean": float(np.mean(x)),
                "std": float(np.std(x, ddof=1)),
                "skewness": float(stats.skew(x)),
                "kurtosis": float(stats.kurtosis(x, fisher=True)),
            }
        )
    df = pd.DataFrame(rows)
    path = OUTPUT_DIR / "signals_stats.parquet"
    df.to_parquet(path, index=False)
    return path


# ---------------------------------------------------------------------------
# Part 3.2 — Histogram vs KDE
# ---------------------------------------------------------------------------

BANDWIDTHS = [0.1, 0.3, 0.5, 1.0, 2.0]


def _kde_eval(x: np.ndarray, grid: np.ndarray, bw: float | str | None) -> np.ndarray:
    if bw is None:
        kde = stats.gaussian_kde(x)
    else:
        kde = stats.gaussian_kde(x, bw_method=bw)
    return kde(grid)


def _data_grid(x: np.ndarray, pad: float = 0.05, num: int = 512) -> np.ndarray:
    lo, hi = float(np.min(x)), float(np.max(x))
    span = hi - lo
    return np.linspace(lo - pad * span, hi + pad * span, num)


def plot_kde_figure(name: str, x: np.ndarray) -> Path:
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    grid = _data_grid(x)

    axes[0].hist(x, bins=50, density=True, color="steelblue", alpha=0.7)
    axes[0].set_title("Histogram (50 bins)")
    axes[0].set_xlabel("Value")
    axes[0].set_ylabel("Density")

    axes[1].hist(x, bins=50, density=True, color="lightgray", alpha=0.5)
    colors = cm.plasma(np.linspace(0.05, 0.95, len(BANDWIDTHS)))
    for h, c in zip(BANDWIDTHS, colors):
        axes[1].plot(grid, _kde_eval(x, grid, h), color=c, linewidth=2, label=f"h={h}")
    axes[1].set_title("KDE — bandwidth effect")
    axes[1].set_xlabel("Value")
    axes[1].set_ylabel("Density")
    axes[1].legend(loc="best", fontsize=9)

    axes[2].hist(x, bins=50, density=True, color="steelblue", alpha=0.6)
    axes[2].plot(grid, _kde_eval(x, grid, None), color="crimson", linewidth=2, label="Scott")
    axes[2].set_title("Histogram + KDE (Scott's rule)")
    axes[2].set_xlabel("Value")
    axes[2].set_ylabel("Density")
    axes[2].legend(loc="best", fontsize=9)

    fig.suptitle(f"Signal: {name}", fontsize=14, fontweight="bold")
    fig.tight_layout()
    path = OUTPUT_DIR / f"kde_{name}.png"
    fig.savefig(path, dpi=300, bbox_inches="tight")
    plt.close("all")
    return path


def plot_kde_bandwidth_summary(signals: dict[str, np.ndarray]) -> Path:
    fig, axes = plt.subplots(5, 2, figsize=(20, 16))
    axes_flat = axes.flatten()
    colors = cm.plasma(np.linspace(0.05, 0.95, len(BANDWIDTHS)))
    for ax, name in zip(axes_flat, SIGNAL_ORDER):
        x = signals[name]
        grid = _data_grid(x)
        for h, c in zip(BANDWIDTHS, colors):
            ax.plot(grid, _kde_eval(x, grid, h), color=c, linewidth=1.8, label=f"h={h}")
        ax.set_title(name)
        ax.set_xlabel("Value")
        ax.set_ylabel("Density")
        ax.legend(loc="best", fontsize=8)
    fig.suptitle("KDE bandwidth effect across all signals", fontsize=16, fontweight="bold")
    fig.tight_layout()
    path = OUTPUT_DIR / "kde_bandwidth_summary.png"
    fig.savefig(path, dpi=300, bbox_inches="tight")
    plt.close("all")
    return path


# ---------------------------------------------------------------------------
# Part 3.3 — Cullen-Frey-Pearson space
# ---------------------------------------------------------------------------


def _bootstrap_cfp(x: np.ndarray, n_boot: int = N_BOOTSTRAP, seed: int = SEED) -> np.ndarray:
    """Return an (n_boot, 2) array of (skew², kurt_pearson) per resample."""
    rng = np.random.default_rng(seed)
    n = x.size
    out = np.empty((n_boot, 2), dtype=float)
    for i in range(n_boot):
        sample = rng.choice(x, size=n, replace=True)
        sk = stats.skew(sample)
        ku = stats.kurtosis(sample, fisher=False)
        out[i, 0] = sk * sk
        out[i, 1] = ku
    return out


def _draw_cfp_references(ax: plt.Axes, xlim: tuple[float, float] | None = None,
                          ylim: tuple[float, float] | None = None) -> None:
    """Draw Cullen-Frey reference distributions. All artefacts are clipped to
    the axes view so they cooperate with ``bbox_inches='tight'``."""
    sigma = np.linspace(0.01, 3.0, 400)
    s2 = np.exp(sigma**2)
    b1_ln = (s2 + 2.0) ** 2 * (s2 - 1.0)
    b2_ln = np.exp(4 * sigma**2) + 2 * np.exp(3 * sigma**2) + 3 * np.exp(2 * sigma**2) - 6
    (ln_line,) = ax.plot(b1_ln, b2_ln, color="gray", linewidth=1.5, alpha=0.7,
                         label="_nolegend_")
    ln_line.set_clip_on(True)

    k = np.linspace(0.1, 30.0, 400)
    b1_g = (2.0 / np.sqrt(k)) ** 2
    b2_g = 3.0 + 6.0 / k
    (g_line,) = ax.plot(b1_g, b2_g, color="gray", linewidth=1.5, linestyle="--",
                        alpha=0.7, label="_nolegend_")
    g_line.set_clip_on(True)

    a_grid = np.linspace(0.1, 10.0, 30)
    b_grid = np.linspace(0.1, 10.0, 30)
    beta_x, beta_y = [], []
    for a in a_grid:
        for b in b_grid:
            sk, ku_excess = stats.beta(a, b).stats(moments="sk")
            beta_x.append(float(sk) ** 2)
            beta_y.append(float(ku_excess) + 3.0)
    beta_scatter = ax.scatter(beta_x, beta_y, color="gray", alpha=0.15, s=10,
                              label="_nolegend_")
    beta_scatter.set_clip_on(True)

    ax.scatter([0], [3], marker="*", color="gray", s=260, edgecolor="black",
               linewidth=0.8, zorder=4, label="_nolegend_")
    ax.scatter([4], [9], marker="^", color="gray", s=140, edgecolor="black",
               linewidth=0.8, zorder=4, label="_nolegend_")
    ax.scatter([0], [1.8], marker="s", color="gray", s=120, edgecolor="black",
               linewidth=0.8, zorder=4, label="_nolegend_")

    # Annotations — use clip_on=True so they never expand the saved bbox.
    annotations = [
        ("Normal", 0.4, 3.15),
        ("Exponential", 4.2, 9.1),
        ("Uniform", 0.4, 1.7),
        ("Beta region", 0.15, 5.5),
    ]
    # Place curve labels at points that lie inside the visible window when
    # possible.
    if xlim is None:
        xlim_eff = ax.get_xlim()
    else:
        xlim_eff = xlim
    if ylim is None:
        ylim_eff = ax.get_ylim()
    else:
        ylim_eff = ylim

    def _pick_inside(xs: np.ndarray, ys: np.ndarray) -> tuple[float, float] | None:
        mask = (
            (xs >= xlim_eff[0]) & (xs <= xlim_eff[1])
            & (ys >= ylim_eff[0]) & (ys <= ylim_eff[1])
        )
        idx = np.where(mask)[0]
        if idx.size == 0:
            return None
        mid = idx[len(idx) // 2]
        return float(xs[mid]), float(ys[mid])

    ln_anchor = _pick_inside(b1_ln, b2_ln)
    if ln_anchor is not None:
        annotations.append(("Lognormal", ln_anchor[0], ln_anchor[1]))
    g_anchor = _pick_inside(b1_g, b2_g)
    if g_anchor is not None:
        annotations.append(("Gamma", g_anchor[0], g_anchor[1] + 0.1))

    for txt, tx, ty in annotations:
        t = ax.text(tx, ty, txt, color="dimgray", fontsize=10)
        t.set_clip_on(True)


def compute_cfp_stats(
    signals: dict[str, np.ndarray]
) -> tuple[dict[str, np.ndarray], pd.DataFrame]:
    boot_data: dict[str, np.ndarray] = {}
    rows = []
    for i, name in enumerate(SIGNAL_ORDER):
        boots = _bootstrap_cfp(signals[name], seed=SEED + i)
        boot_data[name] = boots
        rows.append(
            {
                "signal": name,
                "skewness_sq_mean": float(boots[:, 0].mean()),
                "skewness_sq_std": float(boots[:, 0].std(ddof=1)),
                "kurtosis_pearson_mean": float(boots[:, 1].mean()),
                "kurtosis_pearson_std": float(boots[:, 1].std(ddof=1)),
            }
        )
    df = pd.DataFrame(rows)
    df.to_parquet(OUTPUT_DIR / "cullen_frey_stats.parquet", index=False)
    return boot_data, df


def plot_cullen_frey(boot_data: dict[str, np.ndarray]) -> Path:
    fig, ax = plt.subplots(figsize=(14, 10))
    # Determine a view that fits all signal bootstrap means + a margin, but
    # caps the heavy-tailed signal kurtosis so the reference curves remain
    # readable.
    all_x = np.concatenate([boot_data[n][:, 0] for n in SIGNAL_ORDER])
    all_y = np.concatenate([boot_data[n][:, 1] for n in SIGNAL_ORDER])
    x_hi = float(min(max(all_x.max() * 1.15, 5.0), 25.0))
    y_hi = float(min(max(all_y.max() * 1.10, 12.0), 40.0))
    xlim = (-0.5, x_hi)
    ylim = (1.0, y_hi)
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    _draw_cfp_references(ax, xlim=xlim, ylim=ylim)

    for name in SIGNAL_ORDER:
        color, marker = SIGNAL_STYLE[name]
        pts = boot_data[name]
        ax.scatter(pts[:, 0], pts[:, 1], s=20, alpha=0.3, color=color, marker=marker)
        ax.scatter(
            pts[:, 0].mean(),
            pts[:, 1].mean(),
            s=120,
            alpha=1.0,
            color=color,
            marker=marker,
            edgecolor="black",
            linewidth=0.8,
            label=name,
            zorder=5,
        )

    ax.axhline(3, color="black", linestyle="--", linewidth=0.8, alpha=0.5)
    ax.axvline(0, color="black", linestyle="--", linewidth=0.8, alpha=0.5)
    ax.set_xlabel("Skewness² (β₁)")
    ax.set_ylabel("Kurtosis (β₂, Pearson)")
    ax.set_title("Cullen-Frey-Pearson diagram (30 bootstrap realisations per signal)")
    ax.legend(loc="upper right", fontsize=9, framealpha=0.9)
    ax.grid(True, alpha=0.2)
    fig.tight_layout()
    path = OUTPUT_DIR / "cullen_frey.png"
    fig.savefig(path, dpi=300, bbox_inches="tight")
    plt.close("all")
    return path


# ---------------------------------------------------------------------------
# Part 3.4 — Discussion support figures
# ---------------------------------------------------------------------------


def plot_signal_gallery(signals: dict[str, np.ndarray]) -> Path:
    fig, axes = plt.subplots(5, 2, figsize=(20, 16))
    axes_flat = axes.flatten()
    for ax, name in zip(axes_flat, SIGNAL_ORDER):
        x = signals[name]
        grid = _data_grid(x)
        ax.hist(x, bins=50, density=True, color="steelblue", alpha=0.6)
        ax.plot(grid, _kde_eval(x, grid, None), color="crimson", linewidth=2)
        sk = stats.skew(x)
        ku = stats.kurtosis(x, fisher=True)
        ax.set_title(f"{name}\nskewness={sk:.2f}, kurtosis={ku:.2f}", fontsize=11)
        ax.set_xlabel("Value")
        ax.set_ylabel("Density")
    fig.suptitle("Signal gallery (histogram + KDE Scott's rule)",
                 fontsize=16, fontweight="bold")
    fig.tight_layout()
    path = OUTPUT_DIR / "signal_gallery.png"
    fig.savefig(path, dpi=300, bbox_inches="tight")
    plt.close("all")
    return path


def plot_kde_multimodality(signals: dict[str, np.ndarray]) -> Path:
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    targets = ["bimodal_equal", "trimodal", "multimodal_4"]
    for ax, name in zip(axes, targets):
        x = signals[name]
        grid = _data_grid(x)
        ax.hist(x, bins=30, density=True, color="lightgray", alpha=0.5)
        ax.plot(grid, _kde_eval(x, grid, 0.3), color="royalblue", linewidth=2,
                label="h=0.3 (resolves modes)")
        ax.plot(grid, _kde_eval(x, grid, 2.0), color="darkorange", linewidth=2,
                linestyle="--", label="h=2.0 (over-smoothed)")
        ax.plot(grid, _kde_eval(x, grid, None), color="crimson", linewidth=1.5,
                linestyle=":", label="Scott's rule")
        for m in TRUE_MODES[name]:
            ax.axvline(m, color="gray", linestyle="--", alpha=0.5)
        ax.set_title(name)
        ax.set_xlabel("Value")
        ax.set_ylabel("Density")
        ax.legend(loc="best", fontsize=9)
    fig.suptitle("KDE — multimodality detection", fontsize=14, fontweight="bold")
    fig.tight_layout()
    path = OUTPUT_DIR / "kde_multimodality.png"
    fig.savefig(path, dpi=300, bbox_inches="tight")
    plt.close("all")
    return path


def plot_cullen_frey_zoom(boot_data: dict[str, np.ndarray]) -> Path:
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.set_xlim(0, 15)
    ax.set_ylim(1.5, 12)
    _draw_cfp_references(ax, xlim=(0, 15), ylim=(1.5, 12))
    targets = ["gaussian", "bimodal_equal", "bimodal_unequal", "trimodal", "multimodal_4"]
    for name in targets:
        color, marker = SIGNAL_STYLE[name]
        pts = boot_data[name]
        mx, my = pts[:, 0].mean(), pts[:, 1].mean()
        ax.scatter(pts[:, 0], pts[:, 1], s=20, alpha=0.3, color=color, marker=marker)
        ax.scatter(mx, my, s=140, alpha=1.0, color=color, marker=marker,
                   edgecolor="black", linewidth=0.8, label=name, zorder=5)
        ax.annotate(name, (mx, my), xytext=(mx + 0.2, my + 0.15),
                    fontsize=10, color=color, fontweight="bold")
    ax.axhline(3, color="black", linestyle="--", linewidth=0.8, alpha=0.5)
    ax.axvline(0, color="black", linestyle="--", linewidth=0.8, alpha=0.5)
    ax.set_xlim(0, 15)
    ax.set_ylim(1.5, 12)
    ax.set_xlabel("Skewness² (β₁)")
    ax.set_ylabel("Kurtosis (β₂, Pearson)")
    ax.set_title("Cullen-Frey-Pearson — multimodal zoom")
    ax.legend(loc="upper right", fontsize=9, framealpha=0.9)
    ax.grid(True, alpha=0.2)
    fig.tight_layout()
    path = OUTPUT_DIR / "cullen_frey_zoom.png"
    fig.savefig(path, dpi=300, bbox_inches="tight")
    plt.close("all")
    return path


def plot_overlap_effect(signals: dict[str, np.ndarray]) -> Path:
    bimodal_near = generate_mixture(
        N_SAMPLES,
        [
            {"type": "gaussian", "loc": -0.5, "scale": 1.0, "weight": 0.5},
            {"type": "gaussian", "loc": 0.5, "scale": 1.0, "weight": 0.5},
        ],
        seed=SEED,
    )

    cases = [
        ("bimodal_equal (sep = 6σ)", signals["bimodal_equal"]),
        ("bimodal_overlap (sep = 2σ)", signals["bimodal_overlap"]),
        ("bimodal_near (sep = 1σ)", bimodal_near),
    ]

    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    for ax, (title, x) in zip(axes, cases):
        grid = _data_grid(x)
        ax.hist(x, bins=50, density=True, color="steelblue", alpha=0.6)
        ax.plot(grid, _kde_eval(x, grid, None), color="crimson", linewidth=2)
        sk2 = stats.skew(x) ** 2
        ku = stats.kurtosis(x, fisher=False)
        ax.set_title(title)
        ax.set_xlabel("Value")
        ax.set_ylabel("Density")
        ax.text(
            0.02,
            0.95,
            f"skewness²={sk2:.3f}\nkurtosis={ku:.3f}",
            transform=ax.transAxes,
            fontsize=10,
            verticalalignment="top",
            bbox=dict(boxstyle="round,pad=0.4", facecolor="white", alpha=0.85,
                      edgecolor="gray"),
        )
    fig.suptitle("Effect of overlap on bimodal mixtures", fontsize=14, fontweight="bold")
    fig.tight_layout()
    path = OUTPUT_DIR / "overlap_effect.png"
    fig.savefig(path, dpi=300, bbox_inches="tight")
    plt.close("all")
    return path


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def _human_size(n: int) -> str:
    size = float(n)
    for unit in ("B", "KB", "MB", "GB"):
        if size < 1024:
            return f"{size:.0f} {unit}" if unit == "B" else f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} TB"


def main() -> int:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    signals = generate_all_signals()
    created: list[Path] = []

    created.append(save_signals(signals))
    created.append(save_signal_stats(signals))

    for name in SIGNAL_ORDER:
        created.append(plot_kde_figure(name, signals[name]))
    created.append(plot_kde_bandwidth_summary(signals))

    boot_data, _ = compute_cfp_stats(signals)
    created.append(OUTPUT_DIR / "cullen_frey_stats.parquet")
    created.append(plot_cullen_frey(boot_data))

    created.append(plot_signal_gallery(signals))
    created.append(plot_kde_multimodality(signals))
    created.append(plot_cullen_frey_zoom(boot_data))
    created.append(plot_overlap_effect(signals))

    seen: set[Path] = set()
    ordered: list[Path] = []
    for p in created:
        if p not in seen:
            seen.add(p)
            ordered.append(p)

    print("Files created:")
    for p in ordered:
        size = _human_size(os.path.getsize(p))
        print(f"  {p.as_posix()} — {size}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
