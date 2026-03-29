# Implementation Plan: Trabalho 02 — Estatística Computacional
**Author:** Rian Koja

## Overview

Deliver a **Typst PDF** covering all five sections of the assignment. Python scripts generate every figure and table; Typst assembles them into the document. The layout mirrors `references/or_mcs`: `make all` rebuilds everything end-to-end.

---

## Project Structure

```
trabalho_02/
├── main.typ                   # Typst master (author: Rian Koja, date: auto)
├── sections/
│   ├── 01_visualization.typ
│   ├── 02_estimation.typ
│   ├── 03_noise.typ
│   ├── 04_stochastic.typ
│   └── 05_real_data.typ
├── scripts/
│   ├── 01_visualization.py
│   ├── 02_estimation.py
│   ├── 03_noise.py
│   ├── 04_stochastic.py
│   └── 05_real_data.py
├── figures/                   # auto-generated SVGs from scripts
│   └── or_mcs -> ../references/or_mcs/helpers/  # symlink — figures reused as-is
├── pyproject.toml             # uv env
└── Makefile
```

> The `figures/or_mcs/` symlink lets Typst import the already-generated files
> `demo_results_linear.svg`, `demo_results_quadratic.svg`, `demo_results_exponential.svg`
> without copying or regenerating them.

---

## Section-by-Section Plan

### 1. Basic Data Visualization
**Open-ended goal:** show visually and intuitively how a line's shape changes with `a` and `b`.

**Script `01_visualization.py` → `figures/01_param_grid.svg`:**
- Matrix of `(a, b)` pairs: `a ∈ {-2, -0.5, 0, 0.5, 2, 10}`, `b ∈ {-5, 0, 5}`.
- Each cell plots `y = ax + b` over the same x-range with parameter annotation.
- Colour-code positive vs. negative slope; mark y-intercept.

**Typst section `01_visualization.typ`:**
- Compact table of (a, b, slope direction, y-intercept).
- `01_param_grid.svg`.
- 1–2 paragraphs explaining what each parameter controls.

---

### 2. Parameter Estimation (Inverse Problem)
**Open-ended goal:** implement exhaustive grid search and analytical OLS; compare both on the error surface.

**Script `02_estimation.py` → `figures/02_error_surface_L1.svg`, `02_error_surface_L2.svg`, `02_fit_comparison.svg`:**
- Ground truth `a₀ = 1.5`, `b₀ = -2.0`; 50 noisy observations.
- Grid search over `a ∈ [-3, 3]`, `b ∈ [-6, 2]` (200×200).
- L1 and L2 error surfaces as filled contours; mark grid minimum and OLS minimum.
- Analytical OLS via `(AᵀA)⁻¹Aᵀy`; overlay both fits on the scatter.

**Typst section `02_estimation.typ`:**
- Typeset L1 and L2 objective functions.
- OLS analytical derivation (normal equations).
- Two contour figures with commentary (L2 smooth/unique minimum vs. L1 non-smooth).
- Recovery table: `(â, b̂)` grid vs. analytical vs. ground truth.

---

### 3. Data Noise Analysis + OR-MCS Reproduction
**Open-ended goal:** characterise how noise affects mean and variance, then evaluate model selection under contamination — directly connecting noise theory to the OR-MCS question.

**Reused OR-MCS assets (no regeneration needed):**

| Asset | Source | How included in Typst |
|---|---|---|
| `demo_results_linear.svg` | `references/or_mcs/helpers/` (already generated) | `#image("figures/or_mcs/demo_results_linear.svg")` |
| `demo_results_quadratic.svg` | idem | idem |
| `demo_results_exponential.svg` | idem | idem |

**Script `03_noise.py` → `figures/03_noise_analysis.svg` + CSV table:**
- Same synthetic linear data as section 2.
- Three noise models at intensities `σ ∈ {0.1, 0.5, 1.0, 2.0}`:
  - **Additive:** `ŷ = ax + b + ε`, `ε ~ N(0, σ²)` → `E[ŷ] = ax+b`, `Var[ŷ] = σ²`
  - **Multiplicative:** `ŷ = (ax+b)(1+ε)` → `E[ŷ] = ax+b`, `Var[ŷ] = (ax+b)²σ²`
  - **Combined:** `ŷ = (ax+b)(1+ε₁) + ε₂`
- Compute analytical and Monte Carlo (10 000 draws) mean/variance for each; output CSV.
- Plot scatter grid (noise type × intensity).

**Typst section `03_noise.typ`:**
- Math derivations of E[ŷ] and Var[ŷ] for each model.
- `03_noise_analysis.svg` + statistics table.
- **Subsection "Model Selection under Noise (OR-MCS reproduction)":**
  - Explain the OR-MCS demo: 9 datasets (linear/quadratic/exponential × no/some/many outliers); LS, RANSAC, LightGBM, RANSAC+LightGBM; evaluated with MCS at 10% confidence.
  - Include the three SVGs (`demo_results_linear.svg`, etc.) as captioned figures.
  - Manually-typeset table reproducing key MCS p-values from `results_table.tex`.
  - Critical discussion: why does naive MCS prefer LightGBM (overfitting) under heavy outliers? How does this motivate OR-MCS?

---

### 4. Stochastic Optimization
**Open-ended goal:** compare exhaustive vs. stochastic search in time and convergence; show that recovered parameters carry uncertainty (i.e., have distributions).

**Script `04_stochastic.py` → `figures/04_timing.svg`, `figures/04_param_histograms.svg`:**
- **Stochastic search:** sample `(a, b) ~ Uniform[-5,5]²`; keep if L2 improves; halt if error < tolerance `τ = 0.01`.
- 500 independent trials; record wall-clock time, iterations, final `(â, b̂)`.
- Compare against exhaustive 200×200 grid via `time.perf_counter`.
- Repeat for `σ ∈ {0.1, 0.5, 2.0}` to show widening histograms.
- Plot: 6-panel histogram of `â` and `b̂` per noise level; timing bar chart.

**Typst section `04_stochastic.typ`:**
- Pseudocode block for the stochastic search.
- Timing table (mean ± std, iterations).
- Histogram figure → **yes**, `â` and `b̂` have distributions, centred on truth, widening with σ.
- Discussion: stochastic is faster but noisier; grid is deterministic but scales as O(N²).

---

### 5. Real Data — GARCH Fit for Financial Stocks
**Open-ended goal:** bring a real dataset, apply linear regression, discuss critically whether linearity holds — and go beyond by fitting GARCH when it doesn't.

**This section reproduces the GARCH exercise from `references/list2_rian_errata.pdf`.**

**Script `05_real_data.py` → `figures/05_*.svg` suite:**
- Download daily closing prices for 3–4 tickers (e.g. `PETR4.SA`, `VALE3.SA`, `^BVSP`, `SPY`) with `yfinance` over 5 years.
- Compute log-returns `rₜ = log(Pₜ / Pₜ₋₁)`.
- **Linear regression:** fit `rₜ` on `rₜ₋₁`; plot scatter + fit line; compute R² → confirm near-zero (returns are unpredictable linearly).
- **GARCH(1,1)** fit with `arch` library (`arch_model(returns, vol='Garch', p=1, q=1)`):
  - Estimate `ω, α, β`; extract conditional volatility σₜ.
  - Plot: (a) return series + σₜ, (b) standardised-residual Q-Q plot, (c) ACF of r²ₜ before/after GARCH.
- **Model comparison table:** AIC/BIC for GARCH(1,1), GARCH(2,1), GARCH(1,2) across all tickers.

**Typst section `05_real_data.typ`:**
- Dataset description (tickers, period, source: Yahoo Finance via `yfinance`).
- GARCH(1,1) definition: $r_t = \sigma_t \varepsilon_t$, $\sigma_t^2 = \omega + \alpha r_{t-1}^2 + \beta \sigma_{t-1}^2$.
- All figures.
- AIC/BIC table.
- Critical discussion: **linear regression is not appropriate** for returns (R² ≈ 0, fat tails, volatility clustering); GARCH captures second-moment dynamics; model selection via AIC/BIC shows GARCH(1,1) is typically sufficient.

---

## Tooling

| Tool | Purpose |
|---|---|
| `uv` + `pyproject.toml` | Python env (mirrors `or_mcs`) |
| `numpy`, `scipy`, `matplotlib` | Sections 1–4 |
| `pandas`, `yfinance` | Section 5 data download |
| `arch` | GARCH fitting (already used in `or_mcs` env) |
| `typst` | PDF compilation |
| `Makefile` | `make figures` → scripts 01–05; `make pdf` → typst; `make all` → both |

---

## Key Design Choices

1. **OR-MCS SVGs included as-is** — imported via symlink `figures/or_mcs/ → references/or_mcs/helpers/`; no regeneration, no copying.
2. **GARCH code adapted from `list2_rian_errata.pdf`** — same `arch`-based idiom; new contribution is the multi-ticker comparison table and the critical linearity discussion.
3. **Math in Typst, numbers from Python** — derivations typeset; scripts emit only figures and CSV.
4. **Author in `main.typ`:** `#set document(author: "Rian Koja", title: "...")`.
5. **Single `make all`** rebuilds everything.

---

## Build Order

```
1. uv init && uv add numpy scipy matplotlib pandas yfinance arch
2. Write Makefile (figures + pdf targets)
3. Implement scripts 01 → 05 (run each after writing)
4. Write Typst sections in parallel
5. Assemble main.typ, compile, review PDF
```
