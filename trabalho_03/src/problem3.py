"""
Problem 3 (Optional): Model Confidence Set (MCS)

Part A — Where MCS shines: True quadratic relationship.
          Four polynomial models; right panel shows MCS p-values as bars with α line.

Part B — Full comparison: 9 datasets (linear/quadratic/exponential × no/some/many
          outliers) × 4 models. Generates one comparison figure per data type (3 rows
          × 2 cols: data+fits | p-value bars) and three separate typst tables.

Part C — Where MCS fails: linear data with circular outliers.
"""

from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.linear_model import LinearRegression, RANSACRegressor
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.metrics import mean_absolute_error
from arch.bootstrap import MCS
import lightgbm as lgb
import warnings

warnings.filterwarnings("ignore")

SEED = 42
ALPHA = 0.10

FIGURES_DIR = Path(__file__).parent.parent / "figures"
FIGURES_DIR.mkdir(exist_ok=True)
GENERATED_DIR = Path(__file__).parent.parent / "generated"
GENERATED_DIR.mkdir(exist_ok=True)

# Model display names and colours (consistent throughout)
MODEL_NAMES = ["LS", "RANSAC", "LGBM", "R+LGBM"]
MODEL_COLORS = ["#4C72B0", "#55A868", "#DD8452", "#C44E52"]


# ─────────────────────────────────────────────────────────────────────────────
# Shared helpers
# ─────────────────────────────────────────────────────────────────────────────


def run_mcs(losses_df: pd.DataFrame, size: float = ALPHA, seed: int = SEED) -> dict:
    try:
        mcs = MCS(losses_df, size=size, seed=seed)
        mcs.compute()
        return mcs.pvalues["Pvalue"].to_dict()
    except Exception as exc:
        print(f"  MCS warning: {exc}")
        best = losses_df.mean().idxmin()
        return {col: (1.0 if col == best else 0.0) for col in losses_df.columns}


def make_poly(degree):
    return make_pipeline(PolynomialFeatures(degree), LinearRegression())


def _predict(x_plot, model, is_log_space: bool):
    """Safe prediction; returns nan-filled array on failure."""
    X = x_plot.reshape(-1, 1)
    try:
        if is_log_space:
            m = model[0] if isinstance(model, tuple) else model
            return np.exp(m.predict(X))
        return model.predict(X)
    except Exception:
        return np.full(len(x_plot), np.nan)


def _pvalue_barplot(ax, names, pvalues, alpha=ALPHA):
    """Bar chart of MCS p-values with a horizontal α threshold line."""
    pvs = [pvalues.get(n, 0.0) for n in names]
    bar_colors = ["#55A868" if p >= alpha else "#C44E52" for p in pvs]
    xs = np.arange(len(names))
    ax.bar(xs, pvs, color=bar_colors, edgecolor="white", width=0.6)
    ax.axhline(alpha, color="black", lw=1.4, ls="--", label=f"α = {alpha}")
    ax.set_xticks(xs)
    ax.set_xticklabels([n.replace(" ", "\n") for n in names], fontsize=8)
    ax.set_ylim(0, 1.12)
    ax.set_ylabel("MCS p-value")
    ax.legend(fontsize=8)
    for x, p in zip(xs, pvs):
        ax.text(x, p + 0.03, f"{p:.2f}", ha="center", va="bottom", fontsize=8)


# ─────────────────────────────────────────────────────────────────────────────
# Part A — MCS shines
# ─────────────────────────────────────────────────────────────────────────────


def part_a_mcs_shines():
    """
    True model y = x².  Large test set (n=500) gives the MCS enough power to
    separate the four polynomial candidates.  Noise chosen so that degree 2 wins
    clearly, degree 12 is excluded by overfitting, and linear by underfitting.
    """
    rng = np.random.default_rng(7)  # seed chosen for clean separation
    n_tr, n_te, noise = 200, 500, 1.5

    x_tr = rng.uniform(-4, 4, n_tr)
    y_tr = x_tr**2 + rng.normal(0, noise, n_tr)
    x_te = rng.uniform(-4, 4, n_te)
    y_te = x_te**2 + rng.normal(0, noise, n_te)

    poly_models = {
        "Linear (deg 1)": make_poly(1),
        "Quadratic (deg 2)": make_poly(2),
        "Cubic (deg 3)": make_poly(3),
        "Degree 12": make_poly(12),
    }
    losses = {}
    for name, m in poly_models.items():
        m.fit(x_tr.reshape(-1, 1), y_tr)
        losses[name] = (y_te - m.predict(x_te.reshape(-1, 1))) ** 2

    pvalues = run_mcs(pd.DataFrame(losses))
    print("Part A — MCS p-values:")
    for name, pv in pvalues.items():
        rmse = np.sqrt(losses[name].mean())
        print(f"  {name:22s}  RMSE={rmse:.3f}  p={pv:.3f}")

    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    fig.suptitle(
        "MCS Shines: True Quadratic Relationship\n"
        f"(train n={n_tr}, test n={n_te}, noise σ={noise})",
        fontsize=12,
        fontweight="bold",
    )

    # Left — fitted curves on test data
    ax = axes[0]
    x_plot = np.linspace(-4, 4, 300).reshape(-1, 1)
    ax.scatter(
        x_tr,
        y_tr,
        s=12,
        alpha=0.25,
        color="#4878CF",
        marker="o",
        label=f"Train (n={n_tr})",
        zorder=1,
    )
    ax.scatter(
        x_te,
        y_te,
        s=12,
        alpha=0.35,
        color="#D65F5F",
        marker="^",
        label=f"Test (n={n_te})",
        zorder=1,
    )
    ax.plot(x_plot, x_plot**2, "k--", lw=1.5, label="True y = x²", zorder=2)
    colors = ["#C44E52", "#55A868", "#DD8452", "#9467BD"]
    for (name, m), color in zip(poly_models.items(), colors):
        pv = pvalues.get(name, 0.0)
        ax.plot(
            x_plot,
            m.predict(x_plot),
            color=color,
            lw=2.5 if pv >= ALPHA else 1.2,
            ls="-" if pv >= ALPHA else "--",
            label=f"{name}  (p={pv:.2f})",
            zorder=3,
        )
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title("Fitted curves\n(solid line = in MCS, dashed = excluded)")
    ax.legend(fontsize=8, loc="upper center")
    ax.set_ylim(-5, 25)

    # Right — MCS p-value bar chart
    ax = axes[1]
    _pvalue_barplot(ax, list(poly_models.keys()), pvalues)
    ax.set_title(f"MCS p-values  (green ≥ α={ALPHA}, red < α)")

    fig.tight_layout()
    out = FIGURES_DIR / "problem3_mcs_shines.svg"
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved {out}")


# ─────────────────────────────────────────────────────────────────────────────
# Data generation
# ─────────────────────────────────────────────────────────────────────────────


def _gen_linear(n_pts, n_out, noise=0.1, seed=42):
    rng = np.random.default_rng(seed)
    xi = rng.uniform(-5, 5, n_pts)
    yi = xi + rng.normal(0, noise, n_pts)
    if n_out > 0:
        ang = rng.uniform(0, 2 * np.pi, n_out)
        r = rng.uniform(3, 6, n_out)
        xo = r * np.cos(ang)
        yo = r * np.sin(ang)
        return (
            np.r_[xi, xo],
            np.r_[yi, yo],
            np.r_[np.zeros(n_pts, bool), np.ones(n_out, bool)],
        )
    return xi, yi, np.zeros(n_pts, bool)


def _gen_quadratic(n_pts, n_out, noise=0.5, seed=42):
    rng = np.random.default_rng(seed)
    xi = rng.uniform(-3, 3, n_pts)
    yi = xi**2 + rng.normal(0, noise, n_pts)
    if n_out > 0:
        xo = rng.uniform(-3, 3, n_out)
        yo = rng.uniform(-5, 15, n_out)
        return (
            np.r_[xi, xo],
            np.r_[yi, yo],
            np.r_[np.zeros(n_pts, bool), np.ones(n_out, bool)],
        )
    return xi, yi, np.zeros(n_pts, bool)


def _gen_exponential(n_pts, n_out, noise=0.3, seed=42):
    rng = np.random.default_rng(seed)
    xi = rng.uniform(-1, 2, n_pts)
    yi = np.exp(xi) + rng.normal(0, noise, n_pts)
    if n_out > 0:
        xo = rng.uniform(-1, 2, n_out)
        yo = rng.uniform(-2, 10, n_out)
        return (
            np.r_[xi, xo],
            np.r_[yi, yo],
            np.r_[np.zeros(n_pts, bool), np.ones(n_out, bool)],
        )
    return xi, yi, np.zeros(n_pts, bool)


# ─────────────────────────────────────────────────────────────────────────────
# Model fitting
# ─────────────────────────────────────────────────────────────────────────────


def _fit_ls(x, y, kind):
    X = x.reshape(-1, 1)
    if kind == "linear":
        m = LinearRegression()
        m.fit(X, y)
        return m
    if kind == "quadratic":
        m = make_poly(2)
        m.fit(X, y)
        return m
    mask = y > 0
    if mask.sum() < 2:
        return None
    m = LinearRegression()
    m.fit(X[mask], np.log(y[mask]))
    return (m, mask)


def _fit_ransac(x, y, kind, seed=42):
    X = x.reshape(-1, 1)
    if kind == "linear":
        m = RANSACRegressor(random_state=seed, min_samples=2)
        m.fit(X, y)
        return m
    if kind == "quadratic":
        m = RANSACRegressor(estimator=make_poly(2), random_state=seed, min_samples=3)
        m.fit(X, y)
        return m
    mask = y > 0
    if mask.sum() < 2:
        return None
    try:
        m = RANSACRegressor(random_state=seed, min_samples=2)
        m.fit(X[mask], np.log(y[mask]))
        return (m, mask)
    except Exception:
        return None


def _fit_lgbm(x, y, seed=42):
    m = lgb.LGBMRegressor(
        random_state=seed, n_estimators=100, learning_rate=0.1, max_depth=3, verbose=-1
    )
    m.fit(x.reshape(-1, 1), y)
    return m


def _fit_lgbm_ransac(x, y, seed=42):
    base = lgb.LGBMRegressor(
        random_state=seed,
        n_estimators=50,
        learning_rate=0.1,
        max_depth=3,
        min_child_samples=1,
        verbose=-1,
    )
    m = RANSACRegressor(
        estimator=base, random_state=seed, min_samples=0.5, max_trials=100
    )
    m.fit(x.reshape(-1, 1), y)
    return m


# ─────────────────────────────────────────────────────────────────────────────
# Evaluation
# ─────────────────────────────────────────────────────────────────────────────


def _evaluate(x, y, model, is_log_space: bool):
    try:
        mask = model[1] if (is_log_space and isinstance(model, tuple)) else (y > 0)
        if is_log_space:
            m = model[0] if isinstance(model, tuple) else model
            y_pred = np.exp(m.predict(x[mask].reshape(-1, 1)))
            resid = y[mask] - y_pred
            y_eval = y[mask]
        else:
            y_pred = model.predict(x.reshape(-1, 1))
            resid = y - y_pred
            y_eval = y
        sq = resid**2
        return {
            "rmse": float(np.sqrt(sq.mean())),
            "mae": float(mean_absolute_error(y_eval, y_pred)),
            "losses": sq,
        }
    except Exception:
        return {"rmse": np.inf, "mae": np.inf, "losses": None}


# ─────────────────────────────────────────────────────────────────────────────
# Comparison figure  (3 rows × 2 cols)
# ─────────────────────────────────────────────────────────────────────────────

_OUTLIER_LABELS = ["No outliers (0%)", "Some outliers (~20%)", "Many outliers (~50%)"]
_TRUE_FN = {
    "linear": (lambda x: x, "y = x"),
    "quadratic": (lambda x: x**2, "y = x²"),
    "exponential": (lambda x: np.exp(x), "y = eˣ"),
}
_X_RANGE = {
    "linear": (-6.5, 6.5),
    "quadratic": (-3.5, 3.5),
    "exponential": (-1.3, 2.3),
}


def _plot_comparison_figure(
    type_name, kind, datasets, models_list, pvals_list, out_path
):
    """
    datasets      : list of 3 (x, y, is_outlier)
    models_list   : list of 3  {col_name: fitted_model}   col_names = MODEL_NAMES
    pvals_list    : list of 3  {col_name: p_value}
    """
    is_log = kind == "exponential"
    true_fn, true_label = _TRUE_FN[kind]
    x0, x1 = _X_RANGE[kind]
    x_plot = np.linspace(x0, x1, 400)

    fig, axes = plt.subplots(3, 2, figsize=(14, 13))
    fig.suptitle(
        f"{type_name} Data — Model Fits and MCS p-values",
        fontsize=13,
        fontweight="bold",
    )

    for row, (label, (x, y, outlier), models, pvals) in enumerate(
        zip(_OUTLIER_LABELS, datasets, models_list, pvals_list)
    ):
        # ── Left: data + fitted curves ────────────────────────────────────────
        ax = axes[row, 0]
        inl = ~outlier
        outtl = outlier
        ax.scatter(
            x[inl], y[inl], s=18, alpha=0.5, color="#4878CF", label="Inliers", zorder=3
        )
        if outtl.any():
            ax.scatter(
                x[outtl],
                y[outtl],
                s=25,
                alpha=0.6,
                color="#D65F5F",
                marker="x",
                linewidths=1.5,
                label="Outliers",
                zorder=3,
            )
        ax.plot(
            x_plot, true_fn(x_plot), "k--", lw=1.4, label=f"True {true_label}", zorder=2
        )

        for name, color in zip(MODEL_NAMES, MODEL_COLORS):
            m = models.get(name)
            if m is None:
                continue
            pv = pvals.get(name, 0.0)
            y_fit = _predict(x_plot, m, is_log)
            ax.plot(
                x_plot,
                y_fit,
                color=color,
                lw=2.2,
                ls="-" if pv >= ALPHA else "--",
                label=f"{name} (p={pv:.2f})",
                zorder=4,
            )

        ax.set_title(label, fontsize=10)
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.legend(fontsize=7, loc="best")
        # clip y-axis to reasonable range
        y_med = np.nanmedian(y)
        y_std = np.nanstd(y)
        ax.set_ylim(y_med - 4 * y_std, y_med + 4 * y_std)

        # ── Right: MCS p-value bars ───────────────────────────────────────────
        ax = axes[row, 1]
        _pvalue_barplot(ax, MODEL_NAMES, pvals)
        ax.set_title(f"{label} — MCS p-values (α={ALPHA})", fontsize=10)

    fig.tight_layout()
    fig.savefig(out_path, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved {out_path}")


# ─────────────────────────────────────────────────────────────────────────────
# Typst table helpers
# ─────────────────────────────────────────────────────────────────────────────


def _row_colors(values, inverse=False):
    valid = [v for v in values if np.isfinite(v)]
    if len(valid) < 2:
        return [(200, 200, 200)] * len(values)
    mn, mx = min(valid), max(valid)
    out = []
    for v in values:
        if not np.isfinite(v):
            out.append((220, 220, 220))
            continue
        norm = (v - mn) / (mx - mn) if mx > mn else 0.5
        if inverse:
            norm = 1.0 - norm
        if norm < 0.5:
            out.append((int(norm * 2 * 255), 255, 0))
        else:
            out.append((255, int((1 - (norm - 0.5) * 2) * 255), 0))
    return out


def _cell(value, rgb):
    r, g, b = rgb
    if not np.isfinite(value):
        return f"table.cell(fill: rgb({r},{g},{b}))[-]"
    return f"table.cell(fill: rgb({r},{g},{b}))[{value:.3f}]"


def _write_typst_table(metrics_data, out_path, caption):
    """Write a 3-row typst table (one outlier level per row)."""
    row_labels = ["No outliers", "~20% outliers", "~50% outliers"]
    lines = [
        "// Auto-generated by src/problem3.py — do not edit manually",
        "",
        "#figure(",
        "  text(size: 8.5pt)[",
        "  #table(",
        "    columns: 13,",
        "    inset: (x: 4pt, y: 4pt),",
        "    align: center,",
        "    stroke: 0.4pt + gray,",
        "    table.cell(rowspan: 2, align: left + horizon)[*Outlier level*],",
        "    table.cell(colspan: 4)[*RMSE*],",
        "    table.cell(colspan: 4)[*MAE*],",
        "    table.cell(colspan: 4)[*MCS p-value*],",
        "    [LS], [RANSAC], [LGBM], [R+LGBM],",
        "    [LS], [RANSAC], [LGBM], [R+LGBM],",
        "    [LS], [RANSAC], [LGBM], [R+LGBM],",
    ]

    for label, d in zip(row_labels, metrics_data):
        rv = [d["ls_rmse"], d["ransac_rmse"], d["lgbm_rmse"], d["lgbm_ransac_rmse"]]
        mv = [d["ls_mae"], d["ransac_mae"], d["lgbm_mae"], d["lgbm_ransac_mae"]]
        pv = [d["ls_mcs"], d["ransac_mcs"], d["lgbm_mcs"], d["lgbm_ransac_mcs"]]
        rc = _row_colors(rv)
        mc = _row_colors(mv)
        pc = _row_colors(pv, inverse=True)
        row = (
            f"    table.cell(align: left)[{label}],"
            + "".join(f" {_cell(v, c)}," for v, c in zip(rv, rc))
            + "".join(f" {_cell(v, c)}," for v, c in zip(mv, mc))
            + "".join(f" {_cell(v, c)}," for v, c in zip(pv, pc))
        )
        lines.append(row)

    lines += [
        "  )],",
        f"  caption: [{caption}],",
        f") <tab_mcs_{out_path.stem.split('_')[-1]}>",
    ]
    out_path.write_text("\n".join(lines) + "\n")
    print(f"Typst table saved to {out_path}")


# ─────────────────────────────────────────────────────────────────────────────
# Part B — Full comparison
# ─────────────────────────────────────────────────────────────────────────────


def part_b_full_comparison():
    print("\nPart B — Full comparison (9 datasets × 4 models)...")

    type_specs = [
        ("Linear", "linear", _gen_linear, [(100, 0, 0), (80, 20, 1), (50, 50, 2)]),
        (
            "Quadratic",
            "quadratic",
            _gen_quadratic,
            [(100, 0, 3), (80, 20, 4), (50, 50, 5)],
        ),
        (
            "Exponential",
            "exponential",
            _gen_exponential,
            [(100, 0, 6), (80, 20, 7), (50, 50, 8)],
        ),
    ]

    for type_name, kind, gen_fn, outlier_specs in type_specs:
        print(f"  {type_name}...")
        is_log = kind == "exponential"

        datasets, models_list, pvals_list, metrics_data = [], [], [], []

        for n_pts, n_out, off in outlier_specs:
            s = SEED + off
            x, y, flag = gen_fn(n_pts, n_out, seed=s)
            datasets.append((x, y, flag))

            ls_m = _fit_ls(x, y, kind)
            ransac_m = _fit_ransac(x, y, kind, seed=s)
            lgbm_m = _fit_lgbm(x, y, seed=s)
            lgbm_r_m = _fit_lgbm_ransac(x, y, seed=s)

            ls_ev = _evaluate(x, y, ls_m, is_log)
            ransac_ev = _evaluate(x, y, ransac_m, is_log)
            lgbm_ev = _evaluate(x, y, lgbm_m, False)
            lgbm_r_ev = _evaluate(x, y, lgbm_r_m, False)

            evs = [ls_ev, ransac_ev, lgbm_ev, lgbm_r_ev]
            col_n = ["LS", "RANSAC", "LightGBM", "R+LightGBM"]
            pvals_raw = {k: 0.0 for k in col_n}
            if all(e["losses"] is not None for e in evs):
                mn = min(len(e["losses"]) for e in evs)
                ldf = pd.DataFrame({n: e["losses"][:mn] for n, e in zip(col_n, evs)})
                pvals_raw = run_mcs(ldf, seed=s)

            # model dict keyed by display name
            models_list.append(
                {
                    "LS": ls_m,
                    "RANSAC": ransac_m,
                    "LGBM": lgbm_m,
                    "R+LGBM": lgbm_r_m,
                }
            )
            pvals_list.append(
                {
                    "LS": pvals_raw.get("LS", 0.0),
                    "RANSAC": pvals_raw.get("RANSAC", 0.0),
                    "LGBM": pvals_raw.get("LightGBM", 0.0),
                    "R+LGBM": pvals_raw.get("R+LightGBM", 0.0),
                }
            )
            metrics_data.append(
                {
                    "ls_rmse": ls_ev["rmse"],
                    "ransac_rmse": ransac_ev["rmse"],
                    "lgbm_rmse": lgbm_ev["rmse"],
                    "lgbm_ransac_rmse": lgbm_r_ev["rmse"],
                    "ls_mae": ls_ev["mae"],
                    "ransac_mae": ransac_ev["mae"],
                    "lgbm_mae": lgbm_ev["mae"],
                    "lgbm_ransac_mae": lgbm_r_ev["mae"],
                    "ls_mcs": pvals_raw.get("LS", 0.0),
                    "ransac_mcs": pvals_raw.get("RANSAC", 0.0),
                    "lgbm_mcs": pvals_raw.get("LightGBM", 0.0),
                    "lgbm_ransac_mcs": pvals_raw.get("R+LightGBM", 0.0),
                }
            )

        # Figure
        fig_out = FIGURES_DIR / f"problem3_comparison_{kind}.svg"
        _plot_comparison_figure(
            type_name, kind, datasets, models_list, pvals_list, fig_out
        )

        # Typst table
        cap = (
            f"*{type_name} data* — RMSE, MAE and MCS p-values for four fitting methods "
            f"at three outlier levels. Green = best, red = worst; for p-values green "
            f"means included in the 90\\% MCS ($hat(p) >= 0.10$). "
            f"LS: Least Squares, LGBM: LightGBM, R+LGBM: RANSAC+LightGBM."
        )
        _write_typst_table(
            metrics_data,
            GENERATED_DIR / f"mcs_table_{kind}.typ",
            cap,
        )


# ─────────────────────────────────────────────────────────────────────────────
# Part C — MCS fails (outlier contamination)
# ─────────────────────────────────────────────────────────────────────────────


def part_c_mcs_fails():
    rng = np.random.default_rng(SEED)
    n_in, n_out = 100, 20

    x_in = rng.uniform(-5, 5, n_in)
    y_in = x_in + rng.normal(0, 0.5, n_in)
    ang = rng.uniform(0, 2 * np.pi, n_out)
    r = rng.uniform(3, 6, n_out)
    x_out = r * np.cos(ang)
    y_out = r * np.sin(ang)
    x_all = np.r_[x_in, x_out]
    y_all = np.r_[y_in, y_out]

    models = {
        "Linear LS": make_poly(1),
        "Quadratic LS": make_poly(2),
        "Flexible (deg 6)": make_poly(6),
    }
    for m in models.values():
        m.fit(x_all.reshape(-1, 1), y_all)

    l_all = {
        n: (y_all - m.predict(x_all.reshape(-1, 1))) ** 2 for n, m in models.items()
    }
    l_clean = {
        n: (y_in - m.predict(x_in.reshape(-1, 1))) ** 2 for n, m in models.items()
    }
    pv_all = run_mcs(pd.DataFrame(l_all))
    pv_clean = run_mcs(pd.DataFrame(l_clean))

    print("\nPart C — contaminated data:")
    for name in models:
        print(
            f"  {name:22s}  RMSE={np.sqrt(l_all[name].mean()):.3f}"
            f"  p={pv_all.get(name, 0.0):.3f}"
        )
    print("Part C — clean inliers only:")
    for name in models:
        print(
            f"  {name:22s}  RMSE={np.sqrt(l_clean[name].mean()):.3f}"
            f"  p={pv_clean.get(name, 0.0):.3f}"
        )

    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    fig.suptitle(
        "MCS Fails: Linear Data with Outliers\n"
        "True relationship y = x; outliers are a circular cloud",
        fontsize=12,
        fontweight="bold",
    )
    x_plot = np.linspace(-6, 6, 300).reshape(-1, 1)
    colors = ["#4C72B0", "#DD8452", "#C44E52"]

    ax = axes[0]
    ax.scatter(
        x_in, y_in, s=20, alpha=0.5, color="steelblue", label="Inliers", zorder=3
    )
    ax.scatter(
        x_out,
        y_out,
        s=30,
        alpha=0.6,
        color="tomato",
        marker="x",
        label="Outliers",
        zorder=3,
    )
    ax.plot(x_plot, x_plot, "k--", lw=1.5, label="True y = x")
    for (name, m), c in zip(models.items(), colors):
        ax.plot(x_plot, m.predict(x_plot), color=c, lw=2, label=name)
    ax.set_xlim(-7, 7)
    ax.set_ylim(-8, 8)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title("Data and Fitted Models")
    ax.legend(fontsize=7)

    for ax, pvals, title in [
        (axes[1], pv_all, "Contaminated data\n(true best = Linear LS)"),
        (axes[2], pv_clean, "Clean inliers only\n(Linear LS should win)"),
    ]:
        _pvalue_barplot(ax, list(models.keys()), pvals)
        ax.set_title(title)

    fig.tight_layout()
    out = FIGURES_DIR / "problem3_mcs_fails.svg"
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved {out}")


# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=== Problem 3 — Model Confidence Set ===")
    part_a_mcs_shines()
    part_b_full_comparison()
    part_c_mcs_fails()
    print("\nDone.")
