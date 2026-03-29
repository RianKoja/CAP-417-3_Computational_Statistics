"""
Script 02: Parameter Estimation — Inverse Problem
Exhaustive grid search (L1 and L2) vs. analytical OLS.
Outputs: figures/02_error_surface_L1.svg
         figures/02_error_surface_L2.svg
         figures/02_fit_comparison.svg
         sections/02_recovery.csv
"""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import csv, time

HERE = Path(__file__).parent
FIGURES = HERE.parent / "figures"
SECTIONS = HERE.parent / "sections"
FIGURES.mkdir(exist_ok=True)
SECTIONS.mkdir(exist_ok=True)

# ── ground truth & data ───────────────────────────────────────────────────────
rng = np.random.default_rng(42)
A_TRUE, B_TRUE = 1.5, -2.0
N = 50
x = rng.uniform(-4, 4, N)
noise = rng.normal(0, 0.8, N)
y = A_TRUE * x + B_TRUE + noise

# ── grid search ───────────────────────────────────────────────────────────────
GRID = 300
a_range = np.linspace(-3, 5, GRID)
b_range = np.linspace(-6, 2, GRID)
AA, BB = np.meshgrid(a_range, b_range)  # (GRID, GRID)

t0 = time.perf_counter()
# residuals: (GRID, GRID, N)
resid = y[None, None, :] - (AA[:, :, None] * x[None, None, :] + BB[:, :, None])
L2 = np.sum(resid ** 2, axis=2)
L1 = np.sum(np.abs(resid), axis=2)
t_grid = time.perf_counter() - t0

# grid minima
idx_L2 = np.unravel_index(np.argmin(L2), L2.shape)
idx_L1 = np.unravel_index(np.argmin(L1), L1.shape)
a_grid_L2, b_grid_L2 = AA[idx_L2], BB[idx_L2]
a_grid_L1, b_grid_L1 = AA[idx_L1], BB[idx_L1]

# ── analytical OLS ────────────────────────────────────────────────────────────
t1 = time.perf_counter()
A_mat = np.column_stack([x, np.ones(N)])
a_ols, b_ols = np.linalg.lstsq(A_mat, y, rcond=None)[0]
t_ols = time.perf_counter() - t1

print(f"Ground truth:  a={A_TRUE}, b={B_TRUE}")
print(f"Grid L2:       a={a_grid_L2:.4f}, b={b_grid_L2:.4f}  (t={t_grid*1e3:.1f} ms)")
print(f"Grid L1:       a={a_grid_L1:.4f}, b={b_grid_L1:.4f}")
print(f"Analytical OLS:a={a_ols:.4f}, b={b_ols:.4f}  (t={t_ols*1e6:.1f} µs)")

# ── save recovery CSV ─────────────────────────────────────────────────────────
with open(SECTIONS / "02_recovery.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["Method", "a_hat", "b_hat", "err_a", "err_b", "time_ms"])
    w.writerow(["Ground truth", A_TRUE, B_TRUE, 0, 0, "—"])
    w.writerow(["Grid L2", f"{a_grid_L2:.4f}", f"{b_grid_L2:.4f}",
                f"{abs(a_grid_L2-A_TRUE):.4f}", f"{abs(b_grid_L2-B_TRUE):.4f}",
                f"{t_grid*1e3:.2f}"])
    w.writerow(["Grid L1", f"{a_grid_L1:.4f}", f"{b_grid_L1:.4f}",
                f"{abs(a_grid_L1-A_TRUE):.4f}", f"{abs(b_grid_L1-B_TRUE):.4f}", "—"])
    w.writerow(["Analytical OLS", f"{a_ols:.4f}", f"{b_ols:.4f}",
                f"{abs(a_ols-A_TRUE):.4f}", f"{abs(b_ols-B_TRUE):.4f}",
                f"{t_ols*1e3:.4f}"])
print(f"Saved sections/02_recovery.csv")

# ── helper: error surface plot ────────────────────────────────────────────────
def plot_surface(E, a_range, b_range, a_gt, b_gt, a_min, b_min, title, fname):
    fig, ax = plt.subplots(figsize=(6.5, 5))
    cf = ax.contourf(a_range, b_range, E, levels=40, cmap="viridis")
    plt.colorbar(cf, ax=ax, label="Error")
    ax.contour(a_range, b_range, E, levels=15, colors="white", linewidths=0.4, alpha=0.5)
    ax.plot(a_gt, b_gt, "w*", markersize=14, label=f"True $(a,b)$", zorder=5)
    ax.plot(a_min, b_min, "rx", markersize=10, markeredgewidth=2.5,
            label=f"Grid min $\\hat{{a}}={a_min:.2f},\\hat{{b}}={b_min:.2f}$", zorder=5)
    ax.set_xlabel("$a$", fontsize=12)
    ax.set_ylabel("$b$", fontsize=12)
    ax.set_title(title, fontsize=12)
    ax.legend(fontsize=9)
    fig.tight_layout()
    fig.savefig(fname, format="svg", bbox_inches="tight")
    print(f"Saved {fname}")
    plt.close()

plot_surface(L2, a_range, b_range, A_TRUE, B_TRUE, a_grid_L2, b_grid_L2,
             "L2 Error Surface (Sum of Squared Errors)",
             FIGURES / "02_error_surface_L2.svg")

plot_surface(L1, a_range, b_range, A_TRUE, B_TRUE, a_grid_L1, b_grid_L1,
             "L1 Error Surface (Sum of Absolute Errors)",
             FIGURES / "02_error_surface_L1.svg")

# ── fit comparison plot ───────────────────────────────────────────────────────
xp = np.linspace(x.min() - 0.5, x.max() + 0.5, 300)
fig, ax = plt.subplots(figsize=(7, 4.5))
ax.scatter(x, y, alpha=0.6, s=40, color="#555", label="Observations", zorder=3)
ax.plot(xp, A_TRUE * xp + B_TRUE, "k--", linewidth=2, label=f"True line ($a={A_TRUE}, b={B_TRUE}$)")
ax.plot(xp, a_ols * xp + b_ols, color="#e74c3c", linewidth=2,
        label=f"OLS fit ($\\hat{{a}}={a_ols:.3f}, \\hat{{b}}={b_ols:.3f}$)")
ax.plot(xp, a_grid_L2 * xp + b_grid_L2, color="#3498db", linewidth=1.8, linestyle="-.",
        label=f"Grid L2 ($\\hat{{a}}={a_grid_L2:.3f}, \\hat{{b}}={b_grid_L2:.3f}$)")
ax.set_xlabel("$x$", fontsize=12)
ax.set_ylabel("$y$", fontsize=12)
ax.set_title("Parameter Recovery: True vs. Estimated Lines", fontsize=12)
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3)
fig.tight_layout()
fig.savefig(FIGURES / "02_fit_comparison.svg", format="svg", bbox_inches="tight")
print(f"Saved {FIGURES / '02_fit_comparison.svg'}")
plt.close()
