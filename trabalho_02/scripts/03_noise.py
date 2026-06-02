"""
Script 03: Data Noise Analysis
Injects additive, multiplicative, and combined noise at varying intensities.
Verifies mean preservation and variance growth analytically and via Monte Carlo.
Outputs: figures/03_noise_analysis.svg
         sections/03_noise_stats.csv
"""

from pathlib import Path
import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import csv

HERE = Path(__file__).parent
FIGURES = HERE.parent / "figures"
SECTIONS = HERE.parent / "sections"
FIGURES.mkdir(exist_ok=True)
SECTIONS.mkdir(exist_ok=True)

rng = np.random.default_rng(42)
A_TRUE, B_TRUE = 1.5, -2.0
N_MC = 10_000
X_FIXED = np.linspace(-3, 3, 60)  # fixed x-values for analysis
SIGMAS = [0.1, 0.5, 1.0, 2.0]
NOISE_MODELS = ["Additive", "Multiplicative", "Combined"]


# ── Monte Carlo helper ────────────────────────────────────────────────────────
def mc_stats(y_draws):
    return y_draws.mean(axis=0).mean(), y_draws.var(axis=0).mean()


results = []

# Scatter plot: 3 models × 4 sigmas
fig, axes = plt.subplots(
    len(NOISE_MODELS),
    len(SIGMAS),
    figsize=(len(SIGMAS) * 3.5, len(NOISE_MODELS) * 2.8),
    sharex=True,
)
fig.suptitle(
    "Noise Analysis: $y = ax + b$ with different noise models and intensities",
    fontsize=12,
    y=1.01,
)

y_true = A_TRUE * X_FIXED + B_TRUE

for row, model in enumerate(NOISE_MODELS):
    for col, sigma in enumerate(SIGMAS):
        ax = axes[row, col]

        # draw N_MC realisations along the x-grid
        eps = rng.normal(0, sigma, (N_MC, len(X_FIXED)))
        eps2 = rng.normal(0, sigma, (N_MC, len(X_FIXED)))

        if model == "Additive":
            y_draws = y_true[None, :] + eps
            # analytical: E[y] = ax+b, Var[y] = sigma^2
            e_analytical = y_true.mean()
            v_analytical = sigma**2

        elif model == "Multiplicative":
            y_draws = y_true[None, :] * (1 + eps)
            # E[y] = ax+b (since E[eps]=0), Var[y] = (ax+b)^2 * sigma^2
            e_analytical = y_true.mean()
            v_analytical = np.mean(y_true**2) * sigma**2

        else:  # Combined
            y_draws = y_true[None, :] * (1 + eps) + eps2
            e_analytical = y_true.mean()
            v_analytical = np.mean(y_true**2) * sigma**2 + sigma**2

        e_mc, v_mc = mc_stats(y_draws)

        results.append(
            {
                "model": model,
                "sigma": sigma,
                "E_analytical": round(e_analytical, 4),
                "E_mc": round(e_mc, 4),
                "Var_analytical": round(v_analytical, 4),
                "Var_mc": round(v_mc, 4),
            }
        )

        # plot one sample realisation
        y_sample = y_draws[0]
        ax.scatter(X_FIXED, y_sample, s=8, alpha=0.5, color="#3498db", label="Sample")
        ax.plot(X_FIXED, y_true, "k-", linewidth=1.5, label="True line")
        ax.set_title(f"$\\sigma={sigma}$", fontsize=9)
        ax.grid(True, alpha=0.2)
        if col == 0:
            ax.set_ylabel(model, fontsize=9)
        if row == len(NOISE_MODELS) - 1:
            ax.set_xlabel("$x$", fontsize=9)

plt.tight_layout()
out = FIGURES / "03_noise_analysis.svg"
fig.savefig(out, format="svg", bbox_inches="tight")
print(f"Saved {out}")
plt.close()

# ── save CSV ──────────────────────────────────────────────────────────────────
csv_out = SECTIONS / "03_noise_stats.csv"
with open(csv_out, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=results[0].keys())
    w.writeheader()
    w.writerows(results)
print(f"Saved {csv_out}")

# print quick summary
print("\nNoise Statistics Summary:")
for r in results:
    print(
        f"  {r['model']:15s} σ={r['sigma']:4.1f}  "
        f"E[y]: analytic={r['E_analytical']:7.4f} MC={r['E_mc']:7.4f}  "
        f"Var[y]: analytic={r['Var_analytical']:8.4f} MC={r['Var_mc']:8.4f}"
    )
