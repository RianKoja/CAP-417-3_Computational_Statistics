# AGENTS.md — Agent Task Instructions (Hands-On 3)

> **Scope:** This file applies **only to the folder that contains it.**
> Do NOT read, reference, or modify files in the parent directory or in any
> sibling directories (e.g. `../claude-code/` or `../gemini-cli/`).
> All required resources are already present in this folder.

***

## Context

You are completing **Hands-On 3** of a graduate course on Time Series Models.
The subject is the **p-model**, a canonical multifractal multiplicative-cascade
model that simulates extreme fluctuation patterns — both *endogenous* and
*exogenous* — introduced by Meneveau & Sreenivasan (1987) and implemented in
the reference script available in this folder.

The professor generated **10 series per class** (10 endogenous + 10 exogenous)
during the lecture using that script.  Your task builds on that baseline.

***

## Reference Code

The file `P_model_and_Spatio_Temporal_Multifractal_Cascade_Model.py` in this
folder is the reference implementation.  Its docstring describes the model and
the authors:

```
# P-model and Spatio-Temporal Multifractal Cascade Model (STM-Model 2+1D)
# Autores: Carlos Eduardo Falanes, Reinaldo Roberto Rosa
# Instituição: Instituto Nacional de Pesquisas Espaciais - INPE/MCTI
#
# O P-model, proposto por Meneveau e Sreenivasan (1987), é um modelo
# multifractal em cascata baseado na redistribuição recursiva de energia
# entre escalas. Esse processo multiplicativo gera estruturas com
# auto-similaridade e intermitência estatística, características comuns
# em sistemas turbulentos.
#
# A implementação original do P-model unidimensional, desenvolvida por
# R.R. Rosa, R. Sautter e N. Joshi, aplica um processo multiplicativo
# controlado pelo parâmetro p, responsável por introduzir intermitência
# e comportamento multifractal. A cada etapa da cascata, a energia é
# dividida recursivamente em duas partes assimétricas, produzindo uma
# estrutura hierárquica multifractal.
```

**Read the script fully before writing any code.** Use the functions,
constants, and patterns it defines (e.g. the cascade generation loop, the
`p` parameter range for endogenous vs. exogenous classes, any normalisation
steps) as the basis for all series generation.

***

## Environment & Package Manager

Use **`uv`** exclusively for environment and dependency management.
Do not use `pip`, `conda`, or `poetry`.

### Setup (run once before anything else)

```bash
uv init --python 3.11       # only if pyproject.toml does not already exist
uv add numpy scipy matplotlib statsmodels fitter
```

All subsequent execution must go through `uv run`:

```bash
uv run python hands_on_3.py
```

The `uv.lock` file must be committed alongside the script so the environment
is fully reproducible.  Do not delete or modify `.venv/` directly.

***

## Tasks

Implement all four tasks below in the **single Python script** described in the
"Deliverable" section. Each task must be encapsulated in its own clearly named
function, and the `main()` entry point must call them in order.

### Task i — Data Augmentation

Using an AI-driven data-augmentation strategy, generate **10 additional series
for each class** (10 endogenous + 10 exogenous), for a total of 20 new series.

Acceptable strategies (choose and justify at least one in a docstring or
comment block):

- **Parametric perturbation:** draw `p` values from a narrow distribution
  around the class-defining `p` range, regenerate cascades.
- **Gaussian noise injection:** add calibrated white noise to existing series
  while preserving multifractal structure (verify with a structure-function
  check).
- **Segment mixing / bootstrapping:** stochastic resampling of cascade levels.
- **VAE / normalising flow synthesis:** fit a generative model to each class
  and sample from it.

Document the random seed used (set via `numpy.random.default_rng(SEED)` at the
top of the script) so results are fully reproducible.

### Task ii — Cullen-Frey Classification

Collect **all 40 series** (20 original + 20 augmented).
For each series compute the empirical **skewness² (β₁)** and
**excess kurtosis (β₂)**.

1. Plot every series as a point in the **Cullen-Frey diagram** (β₁ on the
   x-axis, β₂ on the y-axis), coloured by class and by origin
   (original / augmented).
2. Overlay the theoretical loci of common distributions (Normal, Lognormal,
   Gamma, Weibull, Beta, etc.).
3. Identify the **statistically most plausible PDF family** for each class
   based on the cluster position in the diagram.

Save the figure as **`cullen_frey.png`** in this folder.

### Task iii — Fitting Verification

For each class:

1. Compute the **mean histogram** over the 20 series belonging to that class.
2. Fit the PDF family identified in Task ii (plus at least one alternative)
   using maximum-likelihood estimation.
3. Overlay the fitted curves on the histogram.
4. Report goodness-of-fit metrics: **KS statistic + p-value**, **AIC**, and
   **BIC** for each candidate distribution — print them to stdout in a
   readable table.
5. Discuss (in a comment block) whether the augmented series are statistically
   consistent with the originals.

Save the figure as **`fitting.png`** in this folder.

### Task iv — Spatio-Temporal Extension

Write a concise discussion (~300–500 words) in a top-level docstring or
comment block addressing:

- How the 1D p-model cascade is extended to a **2D+1 (spatio-temporal)**
  model (the STM-Model described in the reference script).
- What new parameters or structural choices are introduced.
- What classes of real-world phenomena can be modelled and what the
  limitations are.

Optionally, run a brief demo using the STM-Model code from the reference
script and save one example spatio-temporal frame as **`stm_example.png`**.

***

## Deliverable

| Property | Requirement |
|----------|-------------|
| **File name** | `hands_on_3.py` — fixed, do not rename |
| **Location** | This folder only — do not write files outside it |
| **Format** | Single Python script (`.py`) |
| **All code in one file** | Do not split into modules or packages; import only from the standard library, `uv`-managed dependencies, and the reference script in this folder |
| **Reproducibility** | Global `SEED` constant at the top; `uv.lock` committed |
| **Entry point** | `if __name__ == "__main__": main()` at the bottom |
| **Output files** | `cullen_frey.png`, `fitting.png`, and optionally `stm_example.png` — all saved in this folder |
| **Stdout** | Goodness-of-fit table printed to stdout when the script runs |
| **Language of comments/docstrings** | Portuguese (to match course language) |

Running `uv run python hands_on_3.py` from inside this folder must complete
without errors and produce all output files.

***

## Quality Checklist

Before finishing, verify:

- [ ] `uv run python hands_on_3.py` exits with code 0.
- [ ] `uv.lock` is present in this folder.
- [ ] 20 original series (10 endogenous + 10 exogenous) reproduced from the
      reference script.
- [ ] 20 augmented series generated, labelled, and seeded.
- [ ] `cullen_frey.png` saved — all 40 points visible, PDF loci overlaid.
- [ ] Best-fit PDF identified and justified for each class.
- [ ] `fitting.png` saved — fitted curves overlaid on mean histograms.
- [ ] KS, AIC, BIC table printed to stdout.
- [ ] Task iv discussion present as a comment/docstring in the script.
- [ ] No files written outside this folder.
- [ ] No references to `../claude-code/`, `../gemini-cli/`, or any parent path.
- [ ] Language of comments/docstrings in English.