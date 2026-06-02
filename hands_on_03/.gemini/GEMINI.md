# AGENTS.md — Root Project Instructions

> **Scope:** This file applies to the entire project tree.
> The authoritative task files for each AI agent are located in the subfolders
> `claude-code/` and `gemini-cli/`. **Do NOT modify any files inside those
> two directories.** They must be preserved exactly as left by their respective
> agent so that results can be compared side-by-side.

---

## Context

This project is the deliverable for **Hands-On 3** of the course on Time Series
Models, supervised by the professor who assigned the activity.  The reference
implementation (`P_model_and_Spatio_Temporal_Multifractal_Cascade_Model.py`)
was handed out during class and adapted from the class notebook by
**Carlos Eduardo Falanes and Reinaldo Roberto Rosa (INPE/MCTI)**.

The overall assignment has four parts:

| # | Task |
|---|------|
| i | Data Augmentation — generate 10 additional series per class (endogenous / exogenous) using AI-driven strategies |
| ii | Classify all 40 series in the Cullen-Frey space; identify the best-fit PDF for each class |
| iii | Verify the quality of the fitting on the mean histograms of each class |
| iv | Discuss the extension of the p-model to spatio-temporal (2D+1) series simulation |

---

## Repository Layout

```
.
├── AGENTS.md                         ← this file (root)
├── P_model_and_Spatio_Temporal_Multifractal_Cascade_Model.py   ← reference script
├── hands_on_3_rian.ipynb       ← deliverable
├── claude-code/
│   ├── AGENTS.md                     ← instructions for the Claude Code agent
│   ├── P_model_and_Spatio_Temporal_Multifractal_Cascade_Model.py   ← reference script (copy)
│   └── hands_on_3_claude.ipynb       ← deliverable produced by Claude Code
└── gemini-cli/
    ├── AGENTS.md                     ← instructions for the Gemini CLI agent
    ├── P_model_and_Spatio_Temporal_Multifractal_Cascade_Model.py   ← reference script (copy)
    └── hands_on_3_gemini.ipynb       ← deliverable produced by Gemini CLI
```

---

## Deliverable to be submitted to the professor

A **Jupyter notebook** (`.ipynb`) produced by the top-level agent, named as `hands_on_3_rian.ipynb`.
The notebook must be self-contained and reproducible: running
`jupyter nbconvert --to notebook --execute <notebook>` must succeed with no
external dependencies beyond the standard scientific Python stack
(`numpy`, `scipy`, `matplotlib`, `statsmodels`, `fitter` or equivalent).

---

## Rules for this root-level context

- **Do not touch `claude-code/` or `gemini-cli/`.**  Both subdirectories are
  reserved for their respective agents.
- Any exploratory or scratch work you do at the root level must go into
  a `scratch/` directory and must not interfere with the agent subfolders.
- The notebook at top elvel must be fully contained, but shall not reimplement code or work from the subfolders.
- The notebook shall fully satisfy the professor to get a top grade, see hand_on_03.md for original instructions.
- The work and code shall be done in english.



