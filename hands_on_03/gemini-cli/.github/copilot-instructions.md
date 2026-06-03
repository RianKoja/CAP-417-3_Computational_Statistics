# AGENTS.md — Agent Task Instructions (Hands-On 3)

> **Scope:** This file applies **only to the folder that contains it.**
> Do NOT read, reference, or modify files in the parent directory or in any
> sibling directories (e.g. `../claude-code/` or `../gemini-cli/`).
> All required resources are already present in this folder.

---

## Context

You are completing **Hands-On 3** of a graduate course on Time Series Models.
The subject is the **p-model**, a canonical multifractal multiplicative-cascade
model that simulates extreme fluctuation patterns — both *endogenous* and
*exogenous* — introduced by Meneveau & Sreenivasan (1987) and implemented in
the reference script available in this folder.

The professor generated **10 series per class** (10 endogenous + 10 exogenous)
during the lecture using that script.  Your task builds on that baseline.

---

## Reference Code

The file `P_model_and_Spatio_Temporal_Multifractal_Cascade_Model.py` in this
folder is the reference implementation.  Its docstring describes the model and
the authors:

```
# P-model and Spatio-Temporal Multifractal Cascade Model (STM-Model 2+1D)
# Autores: Carlos Eduardo Falanes, Reinaldo Roberto Rosa
# Instituição: Instituto Nacional de Pesquisas Espaciais - INPE/MCTI

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

**Read the script fully before writing any code.**  Use the functions,
constants, and patterns it defines (e.g. the cascade generation loop, the
`p` parameter range for endogenous vs. exogenous classes, any normalisation
steps) as the basis for all series generation.

---

## Tasks

Complete all four tasks below **inside a single Jupyter notebook** (see
"Deliverable" section).  Each task maps to one clearly labelled notebook
section.

### Task i — Data Augmentation

Using an AI-driven data-augmentation strategy, generate **10 additional series
for each class** (10 endogenous + 10 exogenous), for a total of 20 new series.

Acceptable strategies (choose and justify at least one):

- **Parametric perturbation:** draw `p` values from a narrow distribution
  around the class-defining `p` range, regenerate cascades.
- **Gaussian noise injection:** add calibrated white noise to existing series
  while preserving multifractal structure (verify with a structure-function
  check).
- **Segment mixing / bootstrapping:** stochastic resampling of cascade levels.
- **VAE / normalising flow synthesis:** fit a generative model to each class
  and sample from it.

Justify your choice.  Document the random seed used so results are
reproducible.

### Task ii — Cullen-Frey Classification

Collect **all 40 series** (20 from the lecture + 20 from augmentation).
For each series compute the **skewness² (β₁)** and **excess kurtosis (β₂)**
of its empirical distribution.

1. Plot every series as a point in the **Cullen-Frey diagram** (β₁ on the
   x-axis, β₂ on the y-axis), coloured by class (endogenous / exogenous) and
   by origin (original / augmented).
2. Overlay the theoretical loci of common distributions (Normal, Lognormal,
   Gamma, Weibull, Beta, etc.).
3. Identify the **statistically most plausible PDF family** for each class
   based on the cluster position in the diagram.

### Task iii — Fitting Verification

For each class:

1. Compute the **mean histogram** over the 20 series belonging to that class.
2. Fit the PDF family identified in Task ii (plus at least one alternative)
   using maximum-likelihood estimation.
3. Overlay the fitted curves on the histogram.
4. Report goodness-of-fit metrics: **KS statistic + p-value**, **AIC**, and
   **BIC** for each candidate distribution.
5. Discuss whether the augmented series are statistically consistent with the
   originals (same distribution family, overlapping Cullen-Frey cluster).

### Task iv — Spatio-Temporal Extension (Discussion)

Write a concise discussion (≈ 300–500 words, with at least one supporting
figure or diagram) addressing:

- How the 1D p-model cascade is extended to a **2D+1 (spatio-temporal)**
  model (the STM-Model described in the reference script).
- What new parameters or structural choices are introduced in the extension.
- What classes of real-world phenomena can be modelled and what the
  limitations are.
- Optional: run a brief demo using the STM-Model code from the reference
  script and display an example spatio-temporal realisation.

---

## Deliverable

| Property | Requirement |
|----------|-------------|
| **File name** | See the table in the root `AGENTS.md` (one notebook per agent, named `hands_on_3_<agent>.ipynb`) |
| **Location** | This folder only — do not write files outside it |
| **Format** | Jupyter Notebook (`.ipynb`) |
| **Language** | Python 3 |
| **Code** | All code in a **single notebook file** — no external `.py` helper modules |
| **Self-contained** | The notebook must execute top-to-bottom with `jupyter nbconvert --to notebook --execute` |
| **Dependencies** | `numpy`, `scipy`, `matplotlib`, `statsmodels`; optionally `fitter`, `torch`/`tensorflow` for VAE |
| **Reproducibility** | Set and document a global random seed at the top of the notebook |
| **Sections** | One clearly titled section per task (i through iv) |
| **Language of narrative** | Portuguese (to match course language) |

> **Important:** Leave all code in the single notebook.  Do not split logic
> into separate `.py` files.  This makes it easy for the professor to review
> and compare the two agent outputs side-by-side.

---

## Quality Checklist

Before finishing, verify:

- [ ] 20 original series (10 end. + 10 exog.) are reproduced or loaded from
      the reference script output.
- [ ] 20 augmented series generated and clearly labelled.
- [ ] Cullen-Frey diagram includes all 40 series and the reference PDF loci.
- [ ] Best-fit PDF identified and justified for each class.
- [ ] Fitting verified with KS, AIC, BIC; results discussed.
- [ ] Task iv discussion is present with at least one figure.
- [ ] Notebook executes without errors from a clean kernel.
- [ ] Random seed is set and documented.
- [ ] No files written outside this folder.
