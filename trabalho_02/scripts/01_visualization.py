"""
Script 01: Basic Data Visualization
Shows how parameters a and b of y = ax + b affect the line's shape.
Outputs: figures/01_param_grid.svg
"""

from pathlib import Path
import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

HERE = Path(__file__).parent
FIGURES = HERE.parent / "figures"
FIGURES.mkdir(exist_ok=True)

# ── parameter grid ────────────────────────────────────────────────────────────
A_VALUES = [-2.0, -0.5, 0.0, 0.5, 2.0, 10.0]
B_VALUES = [-5.0, 0.0, 5.0]

X = np.linspace(-3, 3, 200)

ncols = len(A_VALUES)
nrows = len(B_VALUES)

fig, axes = plt.subplots(
    nrows,
    ncols,
    figsize=(ncols * 3.2, nrows * 2.8),
    sharex=True,
    sharey=False,
)
fig.suptitle(
    r"$y = ax + b$ — effect of parameters $a$ (columns) and $b$ (rows)",
    fontsize=13,
    y=1.01,
)

for row, b in enumerate(B_VALUES):
    for col, a in enumerate(A_VALUES):
        ax = axes[row, col]
        y = a * X + b
        color = "#e74c3c" if a > 0 else ("#3498db" if a < 0 else "#2ecc71")
        ax.plot(X, y, color=color, linewidth=2)
        ax.axhline(0, color="gray", linewidth=0.5, linestyle="--")
        ax.axvline(0, color="gray", linewidth=0.5, linestyle="--")

        # mark y-intercept
        ax.plot(0, b, "ko", markersize=5, zorder=5)

        title = f"$a={a:g},\\ b={b:g}$"
        ax.set_title(title, fontsize=9)
        ax.set_ylim(min(y) - 2, max(y) + 2)
        ax.grid(True, alpha=0.25)
        if col == 0:
            ax.set_ylabel(f"$b = {b:g}$", fontsize=9)
        if row == nrows - 1:
            ax.set_xlabel("$x$", fontsize=9)

plt.tight_layout()
out = FIGURES / "01_param_grid.svg"
fig.savefig(out, format="svg", bbox_inches="tight")
print(f"Saved {out}")
plt.close()

# ── also save a summary CSV for the Typst table ───────────────────────────────
import csv

rows = []
for a in A_VALUES:
    for b in B_VALUES:
        slope_dir = (
            "positive" if a > 0 else ("negative" if a < 0 else "zero (horizontal)")
        )
        rows.append(
            {
                "a": a,
                "b": b,
                "slope": slope_dir,
                "y-intercept": b,
                "x-intercept": "n/a" if a == 0 else f"{-b / a:.2f}",
            }
        )

csv_out = HERE.parent / "sections" / "01_params.csv"
csv_out.parent.mkdir(exist_ok=True)
with open(csv_out, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)
print(f"Saved {csv_out}")
