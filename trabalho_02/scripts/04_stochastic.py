"""
Script 04: Stochastic Optimization
Compares exhaustive grid search vs. random-restart stochastic search.
Shows that recovered parameters carry distributions.
Outputs: figures/04_timing.svg
         figures/04_param_histograms.svg
         sections/04_timing.csv
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

rng = np.random.default_rng(0)

A_TRUE, B_TRUE = 1.5, -2.0
N_DATA   = 50
N_TRIALS = 500
TOLERANCE = 0.5          # early-stop threshold on L2
GRID_SIZE = 200
SIGMAS    = [0.1, 0.5, 2.0]
SEARCH_BOUND = 5.0       # [−5, 5] for both a and b


def make_data(sigma, seed):
    rng_local = np.random.default_rng(seed)
    x = rng_local.uniform(-4, 4, N_DATA)
    y = A_TRUE * x + B_TRUE + rng_local.normal(0, sigma, N_DATA)
    return x, y


def l2_error(x, y, a, b):
    return np.sum((y - (a * x + b)) ** 2)


# ── exhaustive grid search (one run, time it) ─────────────────────────────────
def exhaustive_grid(x, y, g=GRID_SIZE):
    a_range = np.linspace(-SEARCH_BOUND, SEARCH_BOUND, g)
    b_range = np.linspace(-SEARCH_BOUND, SEARCH_BOUND, g)
    AA, BB = np.meshgrid(a_range, b_range)
    resid = y[None, None, :] - (AA[:, :, None] * x[None, None, :] + BB[:, :, None])
    L2 = np.sum(resid ** 2, axis=2)
    idx = np.unravel_index(np.argmin(L2), L2.shape)
    return AA[idx], BB[idx]


# ── stochastic search (one run) ───────────────────────────────────────────────
def stochastic_search(x, y, tol=TOLERANCE, max_iter=50_000, seed=None):
    rs = np.random.default_rng(seed)
    a = rs.uniform(-SEARCH_BOUND, SEARCH_BOUND)
    b = rs.uniform(-SEARCH_BOUND, SEARCH_BOUND)
    best_err = l2_error(x, y, a, b)
    iters = 0
    for i in range(max_iter):
        a_new = rs.uniform(-SEARCH_BOUND, SEARCH_BOUND)
        b_new = rs.uniform(-SEARCH_BOUND, SEARCH_BOUND)
        err = l2_error(x, y, a_new, b_new)
        if err < best_err:
            a, b, best_err = a_new, b_new, err
        iters = i + 1
        if best_err < tol:
            break
    return a, b, iters


timing_rows = []
param_data  = {}   # sigma -> {a_stoch, b_stoch}

for sigma in SIGMAS:
    print(f"\n--- sigma = {sigma} ---")
    x, y = make_data(sigma, seed=42)

    # ── time exhaustive (5 reps for stability) ────────────────────────────────
    grid_times = []
    for _ in range(5):
        t0 = time.perf_counter()
        exhaustive_grid(x, y)
        grid_times.append(time.perf_counter() - t0)
    t_grid_mean = np.mean(grid_times) * 1e3
    t_grid_std  = np.std(grid_times) * 1e3
    print(f"  Grid search:   {t_grid_mean:.1f} ± {t_grid_std:.1f} ms")

    # ── N_TRIALS stochastic runs ──────────────────────────────────────────────
    a_vals, b_vals, iters_vals, stoch_times = [], [], [], []
    for trial in range(N_TRIALS):
        t0 = time.perf_counter()
        a_hat, b_hat, iters = stochastic_search(x, y, seed=trial)
        stoch_times.append(time.perf_counter() - t0)
        a_vals.append(a_hat)
        b_vals.append(b_hat)
        iters_vals.append(iters)

    t_stoch_mean = np.mean(stoch_times) * 1e3
    t_stoch_std  = np.std(stoch_times) * 1e3
    print(f"  Stochastic:    {t_stoch_mean:.1f} ± {t_stoch_std:.1f} ms  |  "
          f"iters (mean) = {np.mean(iters_vals):.0f}  |  "
          f"â mean={np.mean(a_vals):.3f}, b̂ mean={np.mean(b_vals):.3f}")

    timing_rows.append({
        "sigma": sigma,
        "grid_mean_ms": round(t_grid_mean, 2),
        "grid_std_ms": round(t_grid_std, 2),
        "stoch_mean_ms": round(t_stoch_mean, 2),
        "stoch_std_ms": round(t_stoch_std, 2),
        "stoch_iters_mean": round(np.mean(iters_vals), 1),
    })
    param_data[sigma] = {"a": np.array(a_vals), "b": np.array(b_vals)}

# ── timing CSV ────────────────────────────────────────────────────────────────
with open(SECTIONS / "04_timing.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=timing_rows[0].keys())
    w.writeheader()
    w.writerows(timing_rows)
print("\nSaved sections/04_timing.csv")

# ── timing bar chart ─────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(6.5, 4))
x_pos = np.arange(len(SIGMAS))
width = 0.35
grid_means = [r["grid_mean_ms"] for r in timing_rows]
stoch_means = [r["stoch_mean_ms"] for r in timing_rows]
grid_stds = [r["grid_std_ms"] for r in timing_rows]
stoch_stds = [r["stoch_std_ms"] for r in timing_rows]

bars1 = ax.bar(x_pos - width/2, grid_means, width, yerr=grid_stds, capsize=4,
               label="Exhaustive Grid", color="#e74c3c", alpha=0.85)
bars2 = ax.bar(x_pos + width/2, stoch_means, width, yerr=stoch_stds, capsize=4,
               label="Stochastic Search", color="#3498db", alpha=0.85)
ax.set_xticks(x_pos)
ax.set_xticklabels([f"$\\sigma={s}$" for s in SIGMAS])
ax.set_ylabel("Time (ms)", fontsize=11)
ax.set_title("Execution Time: Grid vs. Stochastic Search", fontsize=11)
ax.legend()
ax.grid(True, alpha=0.3, axis="y")
fig.tight_layout()
fig.savefig(FIGURES / "04_timing.svg", format="svg", bbox_inches="tight")
print(f"Saved {FIGURES / '04_timing.svg'}")
plt.close()

# ── parameter histograms ──────────────────────────────────────────────────────
fig, axes = plt.subplots(2, len(SIGMAS), figsize=(len(SIGMAS) * 4, 6), sharey=False)
fig.suptitle(r"Distributions of recovered $\hat{a}$ and $\hat{b}$ across 500 stochastic runs",
             fontsize=12, y=1.01)

for col, sigma in enumerate(SIGMAS):
    a_arr = param_data[sigma]["a"]
    b_arr = param_data[sigma]["b"]

    # â
    ax = axes[0, col]
    ax.hist(a_arr, bins=40, color="#e74c3c", alpha=0.75, density=True)
    ax.axvline(A_TRUE, color="k", linewidth=2, linestyle="--", label=f"True $a={A_TRUE}$")
    ax.axvline(a_arr.mean(), color="#c0392b", linewidth=1.5, linestyle=":",
               label=f"Mean $\\hat{{a}}={a_arr.mean():.3f}$")
    ax.set_title(f"$\\hat{{a}}$, $\\sigma={sigma}$", fontsize=10)
    ax.legend(fontsize=7)
    ax.grid(True, alpha=0.25)

    # b̂
    ax = axes[1, col]
    ax.hist(b_arr, bins=40, color="#3498db", alpha=0.75, density=True)
    ax.axvline(B_TRUE, color="k", linewidth=2, linestyle="--", label=f"True $b={B_TRUE}$")
    ax.axvline(b_arr.mean(), color="#2980b9", linewidth=1.5, linestyle=":",
               label=f"Mean $\\hat{{b}}={b_arr.mean():.3f}$")
    ax.set_title(f"$\\hat{{b}}$, $\\sigma={sigma}$", fontsize=10)
    ax.legend(fontsize=7)
    ax.grid(True, alpha=0.25)

fig.tight_layout()
fig.savefig(FIGURES / "04_param_histograms.svg", format="svg", bbox_inches="tight")
print(f"Saved {FIGURES / '04_param_histograms.svg'}")
plt.close()
