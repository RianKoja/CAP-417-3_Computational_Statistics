# CLAUDE.md — Hands-on 03: Multimodality, KDE, and Cullen-Frey Space
## CAP 417 – Computational Statistics – Part C

---

## ⚠️ Critical Constraints

- **DO NOT navigate upward** in the folder structure. All operations are strictly confined to the directory where this file lives and its subdirectory `outputs/`.
- **Use `uv` as the package manager** for all dependency management. Do NOT use `pip`, `conda`, or any other package manager directly.
- **All output files must be saved in `./outputs/`**. Create this directory if it does not exist.
- **Only produce image (`.png`) and parquet (`.parquet`) files** in the outputs directory. No CSV, no HTML, no notebooks.
- The report will be generated later by importing files from `./outputs/` **without reading any source code**. Every figure and dataset must be self-contained and informative enough to stand alone.

---

## Environment Setup

```bash
uv init --no-workspace  # only if pyproject.toml does not exist
uv add numpy scipy matplotlib seaborn pandas pyarrow
```

All imports must be resolved through `uv run python` or an activated `uv` environment.

---

## Directory Structure

```
./
├── CLAUDE.md               ← this file
├── main.py                 ← single entry-point script
└── outputs/
    ├── (all .png files)
    └── (all .parquet files)
```

---

## Implementation Instructions

### General Coding Standards

- Use a **fixed random seed** (`numpy.random.default_rng(42)`) everywhere randomness is involved so results are fully reproducible.
- All figures must be saved at **300 DPI**, size **12×8 inches** (or proportional variants as specified below), with tight layout (`bbox_inches="tight"`).
- Use **Matplotlib** for all plots. Seaborn is allowed only for KDE overlays (`sns.kdeplot`).
- All axis labels, titles, and legends must be written in **English**.
- Every plot must have a descriptive title and labeled axes (with units where applicable).
- Use `plt.close("all")` after saving each figure to prevent memory leaks.
- Do not use `plt.show()` anywhere.

---

## Part 3.1 — Multimodal Series Generation

### Task

Implement a function `generate_mixture(n, modes, seed=42)` where:

- `n` (int): number of samples to generate
- `modes` (list of dicts): each dict defines one component with keys:
  - `"type"`: one of `"gaussian"`, `"laplace"`, `"skewnorm"`
  - `"loc"` (float): location parameter (mean or center)
  - `"scale"` (float): scale parameter (std or b)
  - `"weight"` (float): relative weight (will be normalized to sum to 1)
  - `"skew"` (float, only for `"skewnorm"`): skewness parameter `a` for `scipy.stats.skewnorm`
- Returns a 1D `numpy.ndarray` of samples drawn from the mixture.

### Mixture sampling logic

1. Normalize weights to sum to 1.
2. For each sample, draw the component index from a categorical distribution using the weights.
3. Draw the sample from the selected component distribution using `scipy.stats`.

### Signals to generate (n=5000 for all)

Generate the following named signals and store each as a column in a single Parquet file:

| Signal Name         | Description                                                                                  |
|---------------------|----------------------------------------------------------------------------------------------|
| `gaussian`          | Single Gaussian: `loc=0, scale=1, weight=1`                                                 |
| `bimodal_equal`     | Two equal-weight Gaussians: `(loc=-3, scale=1)` and `(loc=3, scale=1)`                      |
| `bimodal_unequal`   | Two unequal Gaussians: `(loc=-3, scale=1, w=0.7)` and `(loc=3, scale=0.8, w=0.3)`          |
| `bimodal_overlap`   | Two overlapping Gaussians: `(loc=-1, scale=1)` and `(loc=1, scale=1)`                       |
| `trimodal`          | Three Gaussians: `(loc=-5, scale=0.8, w=0.3)`, `(loc=0, scale=1, w=0.4)`, `(loc=5, scale=0.8, w=0.3)` |
| `asymmetric`        | Skew-normal: `loc=0, scale=2, skew=8`                                                       |
| `laplace_mix`       | Mix of Laplace and Gaussian: `(laplace, loc=0, scale=1, w=0.5)` + `(gaussian, loc=4, scale=0.5, w=0.5)` |
| `heavy_tail`        | Single Student-t with `df=2` (use `scipy.stats.t(df=2).rvs(n, random_state=42)`)           |
| `multimodal_4`      | Four Gaussians at `loc=-6,-2,2,6`, all `scale=0.7`, equal weights                          |
| `asymmetric_laplace`| Single Laplace: `loc=2, scale=1`                                                            |

### Output files

- **`outputs/signals.parquet`**: DataFrame with one column per signal name, 5000 rows. Include column `"index"` as integer index 0–4999.
- **`outputs/signals_stats.parquet`**: DataFrame with one row per signal and columns: `signal`, `mean`, `std`, `skewness`, `kurtosis` (excess kurtosis, i.e., Fisher definition). Compute using `scipy.stats.skew` and `scipy.stats.kurtosis(fisher=True)`.

---

## Part 3.2 — Histogram vs. KDE

### Task

For each of the 10 signals defined above, generate a comparison figure with **3 panels side by side** (figure size: 18×5 inches):

1. **Left panel — Histogram**: normalized histogram (density=True), 50 bins, color `steelblue`, alpha=0.7. Title: `"Histogram (50 bins)"`.
2. **Middle panel — KDE (bandwidth study)**: overlay KDE curves computed with `scipy.stats.gaussian_kde` for bandwidths `h = [0.1, 0.3, 0.5, 1.0, 2.0]`. Use a different color per bandwidth (use `matplotlib.cm.plasma` colormap, 5 evenly spaced colors). Also show the histogram (density=True, 50 bins, color `lightgray`, alpha=0.5) in the background. Label each KDE curve as `f"h={h}"`. Title: `"KDE — bandwidth effect"`.
3. **Right panel — Best KDE vs Histogram**: show the histogram (density=True, 50 bins, color `steelblue`, alpha=0.6) and on top the KDE using **Scott's rule** bandwidth (default `gaussian_kde` with no argument). Color: `crimson`, linewidth=2. Title: `"Histogram + KDE (Scott's rule)"`.

Each figure must have an overall `suptitle` with the signal name.

### Output files (one per signal)

- `outputs/kde_gaussian.png`
- `outputs/kde_bimodal_equal.png`
- `outputs/kde_bimodal_unequal.png`
- `outputs/kde_bimodal_overlap.png`
- `outputs/kde_trimodal.png`
- `outputs/kde_asymmetric.png`
- `outputs/kde_laplace_mix.png`
- `outputs/kde_heavy_tail.png`
- `outputs/kde_multimodal_4.png`
- `outputs/kde_asymmetric_laplace.png`

### Additional output — KDE bandwidth summary

Produce one additional figure `outputs/kde_bandwidth_summary.png` (figure size: 20×16 inches) with a grid of subplots, one per signal (2 columns × 5 rows). Each subplot shows only the KDE curves for the 5 bandwidths (no histogram), on the same x-range as the signal data. This is intended as a visual reference for the bandwidth effect across all signals simultaneously.

---

## Part 3.3 — Cullen-Frey-Pearson Space

### Theory

The Cullen-Frey-Pearson (CFP) diagram plots each sample/distribution as a point at:
- x = skewness² (squared skewness, β₁)
- y = excess kurtosis + 3 (kurtosis, β₂, using the **Pearson** convention: `scipy.stats.kurtosis(fisher=False)`)

Reference theoretical curves for common distributions must appear as background annotations (see below).

### Reference curves to draw

Draw the following **as background reference lines**, in light gray, with text labels:

1. **Normal distribution**: single point at `(0, 3)`. Mark as a large star marker.
2. **Exponential distribution**: single point at `(4, 9)`. Mark as a triangle.
3. **Uniform distribution**: single point at `(0, 1.8)`. Mark as a square.
4. **Lognormal curve**: parametric curve for varying `σ` (0.01 to 3): 
   - `β₁ = (exp(σ²)+2)² * (exp(σ²)-1)`
   - `β₂ = exp(4σ²) + 2*exp(3σ²) + 3*exp(2σ²) - 6`
   Draw as a continuous line.
5. **Beta distribution region**: shade (lightly) the region bounded by the beta distribution family using a parametric sweep over `(a, b)` pairs (a and b from 0.1 to 10). For each pair compute skewness and kurtosis using `scipy.stats.beta(a, b).stats(moments='sk')`. Plot as a scatter of semi-transparent gray dots.
6. **Gamma curve**: parametric curve varying shape `k` from 0.1 to 30:
   - `β₁ = (2/sqrt(k))²`
   - `β₂ = 3 + 6/k`
   Draw as a continuous dashed line.

### Monte Carlo sampling for uncertainty

For each of the 10 signals, perform **30 bootstrap realizations**:
- Each realization: draw 5000 samples **with replacement** from the original signal array.
- Compute `(skewness², kurtosis_pearson)` for each realization.
- Plot all 30 points per signal as small semi-transparent dots (alpha=0.3, marker size=20).
- Plot the mean of the 30 realizations as a large solid marker (marker size=120, alpha=1.0).

### Color and marker scheme (one per signal)

Use the following fixed color and marker map:

| Signal              | Color      | Marker |
|---------------------|------------|--------|
| `gaussian`          | `#2196F3`  | `o`    |
| `bimodal_equal`     | `#E91E63`  | `s`    |
| `bimodal_unequal`   | `#9C27B0`  | `D`    |
| `bimodal_overlap`   | `#FF5722`  | `^`    |
| `trimodal`          | `#4CAF50`  | `v`    |
| `asymmetric`        | `#FF9800`  | `<`    |
| `laplace_mix`       | `#009688`  | `>`    |
| `heavy_tail`        | `#795548`  | `p`    |
| `multimodal_4`      | `#607D8B`  | `h`    |
| `asymmetric_laplace`| `#F44336`  | `*`    |

### Output files

- **`outputs/cullen_frey.png`** (figure size: 14×10 inches): Full CFP diagram with all 10 signals (bootstrap scatter + mean markers) and all reference lines/regions. Include a legend for the signals only (references labeled directly on the plot). Set x-axis label to `"Skewness² (β₁)"` and y-axis label to `"Kurtosis (β₂, Pearson)"`. Add a horizontal dashed line at `y=3` (Gaussian kurtosis level) and a vertical dashed line at `x=0`.
- **`outputs/cullen_frey_stats.parquet`**: DataFrame with columns `signal`, `skewness_sq_mean`, `skewness_sq_std`, `kurtosis_pearson_mean`, `kurtosis_pearson_std` computed from the 30 bootstrap realizations.

---

## Part 3.4 — Conceptual Discussion Support Figures

These figures support the written discussion and must be interpretable without code.

### Figure 1 — Signal Gallery

`outputs/signal_gallery.png` (figure size: 20×16 inches, 2 columns × 5 rows):

Each subplot shows:
- Normalized histogram (density=True, 50 bins, color `steelblue`, alpha=0.6)
- KDE overlay (Scott's rule, color `crimson`, linewidth=2)
- Title: signal name
- Subtitle (using `ax.set_title(..., pad=...)` or `ax.text`): show `skewness={:.2f}, kurtosis={:.2f}` (using Fisher kurtosis)

### Figure 2 — KDE Multimodality Detection

`outputs/kde_multimodality.png` (figure size: 18×6 inches, 1 row × 3 columns):

Show only the following 3 signals: `bimodal_equal`, `trimodal`, `multimodal_4`.

For each, show:
- Histogram (density=True, 30 bins, `lightgray`, alpha=0.5)
- KDE with `h=0.3` (narrow, color `royalblue`, linewidth=2, label="h=0.3 (resolves modes)")
- KDE with `h=2.0` (wide, color `darkorange`, linewidth=2, linestyle="--", label="h=2.0 (over-smoothed)")
- KDE Scott's rule (color `crimson`, linewidth=1.5, linestyle=":", label="Scott's rule")

Add vertical dashed lines (light gray, alpha=0.5) at the true mode locations for each signal.

### Figure 3 — CFP Zoom: Multimodal region

`outputs/cullen_frey_zoom.png` (figure size: 10×8 inches):

Same as `cullen_frey.png` but zoom into `x ∈ [0, 15]`, `y ∈ [1.5, 12]`. Show only the 4 multimodal signals (`bimodal_equal`, `bimodal_unequal`, `trimodal`, `multimodal_4`) plus `gaussian` as reference. Annotate each mean point with the signal name using `ax.annotate`.

### Figure 4 — Overlap effect

`outputs/overlap_effect.png` (figure size: 18×5 inches, 1 row × 3 columns):

Show three bimodal Gaussians with increasing overlap:
- **Panel 1** — `bimodal_equal` (separation = 6σ): modes at -3 and +3, scale=1
- **Panel 2** — `bimodal_overlap` (separation = 2σ): modes at -1 and +1, scale=1
- **Panel 3** — generate on-the-fly a third case `bimodal_near` with modes at -0.5 and +0.5, scale=1 (near-complete overlap)

For each: show histogram + KDE (Scott's rule). Add annotation box in the corner with `skewness²={:.3f}, kurtosis={:.3f}` (Pearson).

---

## Full List of Output Files

The following files **must** exist in `./outputs/` after the script completes. No other files should be created.

### Parquet files (4 total)

| Filename                        | Description                                              |
|---------------------------------|----------------------------------------------------------|
| `signals.parquet`               | All 10 signals, 5000 rows each                           |
| `signals_stats.parquet`         | Summary stats per signal (mean, std, skewness, kurtosis) |
| `cullen_frey_stats.parquet`     | Bootstrap CFP stats per signal                           |

### PNG files (18 total)

| Filename                        | Description                                              |
|---------------------------------|----------------------------------------------------------|
| `kde_gaussian.png`              | KDE analysis — Gaussian signal                           |
| `kde_bimodal_equal.png`         | KDE analysis — equal bimodal                             |
| `kde_bimodal_unequal.png`       | KDE analysis — unequal bimodal                           |
| `kde_bimodal_overlap.png`       | KDE analysis — overlapping bimodal                       |
| `kde_trimodal.png`              | KDE analysis — trimodal                                  |
| `kde_asymmetric.png`            | KDE analysis — skew-normal                               |
| `kde_laplace_mix.png`           | KDE analysis — Laplace + Gaussian mix                    |
| `kde_heavy_tail.png`            | KDE analysis — heavy-tail Student-t                      |
| `kde_multimodal_4.png`          | KDE analysis — 4-mode Gaussian mixture                   |
| `kde_asymmetric_laplace.png`    | KDE analysis — asymmetric Laplace                        |
| `kde_bandwidth_summary.png`     | Bandwidth effect grid, all signals                       |
| `cullen_frey.png`               | Full Cullen-Frey-Pearson diagram                         |
| `cullen_frey_zoom.png`          | CFP diagram zoomed to multimodal region                  |
| `signal_gallery.png`            | Gallery of all 10 signals with stats                     |
| `kde_multimodality.png`         | KDE multimodality detection comparison                   |
| `overlap_effect.png`            | Bimodal overlap effect illustration                      |

**Total: 3 parquet + 16 PNG = 19 files**

---

## Execution

The entire project must be runnable as a single command:

```bash
uv run python main.py
```

The script must:
1. Create `./outputs/` if it does not exist.
2. Generate all signals.
3. Save all parquet files.
4. Generate and save all PNG files.
5. Print to stdout the list of files created with their sizes (e.g., `outputs/signals.parquet — 412 KB`).
6. Exit with code 0 on success.

There must be no interactive prompts, no GUI windows, and no dependency on Jupyter.

---

## Reproducibility Checklist

- [ ] Random seed fixed to `42` everywhere
- [ ] All figures saved at 300 DPI
- [ ] No `plt.show()` calls
- [ ] `uv run python main.py` runs end-to-end without errors
- [ ] All 19 output files present in `./outputs/`
- [ ] No files written outside `./outputs/`
- [ ] No upward directory traversal (`../` paths are forbidden)
