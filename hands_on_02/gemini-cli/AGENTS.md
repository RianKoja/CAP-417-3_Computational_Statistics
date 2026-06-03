# AGENTS.md — Scoped Agent Instructions

> **SCOPE CONSTRAINT (MANDATORY):** You operate exclusively within this directory.
> Do **NOT** read, traverse, or reference any files outside of this folder.
> Do **NOT** use `../`, absolute paths outside this directory, or any mechanism
> to access parent or sibling directories. Treat this folder as your entire filesystem.

---

## Assignment Context

This is **Hands-on 02 — CAP 417 — Part C**: *Structure, Randomness, and the Cullen-Frey-Pearson Space*.

You must implement the full assignment as a self-contained Python script (compatible with Google Colab).
All code must be correct, well-commented, and produce the outputs listed below.

---

## Task Breakdown

### Part 2.1 — Shuffle Analysis

1. Generate a Brownian (red noise) time series with **N ≥ 1000** points using cumulative sum of Gaussian increments.
2. Create a shuffled version using a random permutation of the same data points.
3. Compute the following statistical moments for **both** the original and shuffled series:
   - Mean
   - Variance (or standard deviation)
   - Skewness (third standardized moment)
   - Kurtosis (fourth standardized moment, excess or raw — state which)
4. Print a comparison table of these moments.
5. Plot both time series side-by-side and include their autocorrelation functions (ACF).
6. Answer inline (as comments or markdown cells) the following analysis questions:
   - Do the moment values change after shuffling?
   - What does this indicate about temporal dependence vs. marginal distribution?
   - Does shuffling preserve the distribution? (Verify the theoretical hypothesis.)

### Part 2.2 — Colored Noise Generation

Implement a general-purpose function `generate_colored_noise(N, beta, seed=None)` that:
- Takes series length `N`, spectral exponent `beta`, and optional random seed.
- Generates noise by shaping white noise in the **frequency domain**:
  1. Generate white noise.
  2. Compute FFT.
  3. Multiply each frequency component by `f^(-beta/2)` (handle DC component carefully).
  4. Apply inverse FFT and return the real part.
- Is valid for any `beta ≥ 0`.

Use this function to generate **100 independent realizations** for each of:

| Noise type  | Beta value |
|-------------|-----------|
| White noise | β = 0     |
| Pink noise  | β ≈ 1     |
| Red noise   | β ≈ 2     |

Each realization must have **N ≥ 1000** points.

### Part 2.3 — Cullen-Frey-Pearson Plot

For all 300 realizations (100 per noise type):
1. Compute **skewness (S)** and **kurtosis (K)** for each realization.
2. Plot in the Cullen-Frey-Pearson space:
   - **x-axis**: S² (squared skewness)
   - **y-axis**: K (kurtosis)
3. Use distinct colors per noise type:
   - White noise → one color
   - Pink noise → another color
   - Red noise → another color
4. Mark the **Gaussian reference point** (S²=0, K=3) explicitly with a distinct marker and label.
5. Use a **dark background** for the plot.
6. Add a legend, axis labels, and a descriptive title.

---

## Expected Output Files

Your script must produce, inside **this directory only**, the following files:

```
solution.py          ← Full Python script (also structured as a Colab-compatible notebook if possible)
figures/
  fig_2_1_series.png       ← Part 2.1: original vs shuffled time series
  fig_2_1_acf.png          ← Part 2.1: ACF comparison
  fig_2_1_moments.png      ← Part 2.1: moment comparison table as figure (optional)
  fig_2_2_examples.png     ← Part 2.2: example realizations of each noise type
  fig_2_3_cullen_frey.png  ← Part 2.3: Cullen-Frey-Pearson scatter plot
results/
  moments_table.csv        ← Part 2.1: original vs shuffled statistical moments
  noise_moments.csv        ← Parts 2.2/2.3: skewness and kurtosis per realization
```

---

## Code Quality Requirements

- Use only standard scientific Python libraries: `numpy`, `scipy`, `matplotlib`, `pandas`.
- No external dependencies beyond the standard Colab environment.
- Each section (2.1, 2.2, 2.3) must be clearly delimited with comments or markdown cells.
- Set a global random seed at the top of the script for full reproducibility.
- All plots must have: title, labeled axes, legend (where applicable), and readable font sizes.
- The script must run end-to-end without errors from a clean Python environment.
- Do not hardcode magic numbers — define constants at the top of the script.

---

## Do NOT

- Access any file or directory above this folder.
- Import data from external URLs or datasets.
- Use `os.chdir()` to change directories.
- Produce output files outside this directory.
