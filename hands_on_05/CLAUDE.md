## Objective (Top-level Project)

You are the **top-level coordination agent** for the Hands-on 05 assignment (CAP 417 – PSD, DFA and Spectral Exponents in Colored Noises). [file:1]

Your task is to create a **single, standalone Jupyter notebook** in this top-level directory that:

1. Loads and compares the results produced by two sub-agents:
   - `claude-code` (using model opus-4.7)
   - `gemini-cli` (using model gemini-3.1-flash-lite-preview)
2. Critically evaluates their outputs for each exercise item in the assignment.
3. Presents all comparisons (numerical and graphical) in a clear, self-contained way.
4. Is sufficient, by itself, to earn a **full, perfect score** on the exercise list when submitted.

## Directory Layout and Constraints

This `CLAUDE.md` lives in the **top-level project directory**, which contains at least the following subdirectories:

- `claude-code/`
- `gemini-cli/`

### 1. No upward traversal

- Treat the current directory (where this `CLAUDE.md` resides) as the **project root**.
- Do **not** read, write, or traverse to any directory **above** this root.
- Do **not** use paths containing `..`.

### 2. Subfolder immutability

- You **must not** modify any file inside:
  - `claude-code/`
  - `gemini-cli/`
- These directories are considered **read-only** from your perspective.
- You may only **read** files from their `outputs` subdirectories.

Specifically, expect the following structure:

- `claude-code/outputs/`  (results from Claude Opus 4.7)
- `gemini-cli/outputs/`   (results from Gemini 3.1 Flash Lite)

### 3. Package management

- Use **`uv`** as the package manager and environment runner.
- Do **not** rely on any global Python installation.
- For human operators (not executed by you):
  - `uv init` (if needed) in the top-level directory.
  - `uv add numpy pandas pyarrow matplotlib seaborn jupyter`.

## Assignment Context (from Exercise List)

Based on the Hands-on 05 statement: [file:1]

- **5.1**: For a given input time series, compute
  - PSD (Power Spectral Density)
  - DFA (Detrended Fluctuation Analysis)
- **5.2**: Implement log-log least-squares fitting to estimate
  - Spectral exponent `beta` (from PSD)
  - Exponent `alpha` (from DFA)
  - Validate `beta` and `alpha` for colored noises: white, pink, red.
  - Use the theoretical relation \(\beta = 2\alpha - 1\).
- **5.3**: Compare results obtained using two agents (ChatGPT and Claude) with a benchmark on:
  - Code quality
  - Physical coherence
  - Numerical stability
  - Quality and clarity of graphs
  - Interpretation of results

In this project:

- `claude-code` corresponds to one agent (Claude Opus 4.7).
- `gemini-cli` corresponds to another agent (Gemini 3.1 Flash Lite).
- Your notebook must address all items 5.1, 5.2, and 5.3 using **only** their output files.

## Expected Inputs from Sub-agents

The sub-agents have been instructed to produce their results in their own `outputs` directories, using fixed file names.

You must assume the following files **exist** and are correctly formatted.

### 1. Files produced by `claude-code`

Inside `claude-code/outputs/`:

**Parquet data files**

- `psd_white.parquet`
- `psd_pink.parquet`
- `psd_red.parquet`
- `dfa_white.parquet`
- `dfa_pink.parquet`
- `dfa_red.parquet`
- `exponents.parquet`

**Image files**

- `psd_white.png`
- `psd_pink.png`
- `psd_red.png`
- `dfa_white.png`
- `dfa_pink.png`
- `dfa_red.png`
- `psd_dfa_relation.png` (optional but may exist)

### 2. Files produced by `gemini-cli`

Inside `gemini-cli/outputs/`:

**Parquet data files**

- `psd_white.parquet`
- `psd_pink.parquet`
- `psd_red.parquet`
- `dfa_white.parquet`
- `dfa_pink.parquet`
- `dfa_red.parquet`
- `exponents.parquet`

**Image files**

- `psd_white.png`
- `psd_pink.png`
- `psd_red.png`
- `dfa_white.png`
- `dfa_pink.png`
- `dfa_red.png`
- `psd_dfa_relation.png` (optional but may exist)

You must **not** generate or overwrite these files; they are inputs to your analysis.

## Required Output (Top-level Agent)

You must create exactly **one** primary artifact in the top-level directory:

- `HandsOn05_Benchmark.ipynb`

This Jupyter notebook must be **self-contained** and must:

1. Load all necessary data and images from:
   - `claude-code/outputs/`
   - `gemini-cli/outputs/`
2. Present all results needed to fully answer assignment items 5.1, 5.2, and 5.3.
3. Provide a critical comparison between the two agents.

No other new files are strictly required from you, but any temporary figures or tables are internal to the notebook.

## Notebook Structure and Content Requirements

The notebook `HandsOn05_Benchmark.ipynb` must follow this structure and include, at minimum, the sections below.

### 0. Notebook setup

Add a **code cell** that:

- Imports required libraries:
  - `from pathlib import Path`
  - `import numpy as np`
  - `import pandas as pd`
  - `import matplotlib.pyplot as plt`
  - `import matplotlib.image as mpimg`
  - `import seaborn as sns`
- Sets plotting style (e.g., `sns.set()`).
- Defines base paths:

```python
ROOT = Path('.').resolve()
CLAUDE_OUTPUTS = ROOT / 'claude-code' / 'outputs'
GEMINI_OUTPUTS = ROOT / 'gemini-cli' / 'outputs'
```

- Asserts existence of required directories and core files with clear error messages if missing.

### 1. Introduction and problem statement

Add a **Markdown section**:

- Summarize the physical motivation: systems often exhibit temporal memory, persistence, and multiscale organization; PSD reveals energy distribution across frequencies; DFA reveals organization of temporal memory across scales. [file:1]
- Restate assignment items 5.1, 5.2, 5.3.
- Explicitly note:
  - `claude-code` and `gemini-cli` are the two agents being benchmarked.
  - The notebook uses only their `outputs` directories.

### 2. Data loading (Parquet files)

Add a **code section** that:

1. Loads all Parquet files from `claude-code/outputs/`:

   ```python
psd_white_claude = pd.read_parquet(CLAUDE_OUTPUTS / 'psd_white.parquet')
psd_pink_claude = pd.read_parquet(CLAUDE_OUTPUTS / 'psd_pink.parquet')
psd_red_claude = pd.read_parquet(CLAUDE_OUTPUTS / 'psd_red.parquet')

dfa_white_claude = pd.read_parquet(CLAUDE_OUTPUTS / 'dfa_white.parquet')
dfa_pink_claude = pd.read_parquet(CLAUDE_OUTPUTS / 'dfa_pink.parquet')
dfa_red_claude = pd.read_parquet(CLAUDE_OUTPUTS / 'dfa_red.parquet')

exponents_claude = pd.read_parquet(CLAUDE_OUTPUTS / 'exponents.parquet')
   ```

2. Loads all Parquet files from `gemini-cli/outputs/` with analogous names.

3. Adds an `agent` column to each DataFrame with values:

   - `'claude-code'` for Claude outputs.
   - `'gemini-cli'` for Gemini outputs.

4. Creates combined DataFrames for each category (e.g., PSD white):

   ```python
psd_white = pd.concat([
    psd_white_claude.assign(agent='claude-code'),
    psd_white_gemini.assign(agent='gemini-cli')
], ignore_index=True)
   ```

Repeat for `psd_pink`, `psd_red`, `dfa_white`, `dfa_pink`, `dfa_red`, and `exponents`.

### 3. Schema and consistency checks

Add a section that:

- Prints or summarizes schemas (column names and dtypes) for each combined DataFrame.
- Checks that:

  - **PSD files** contain: `frequency`, `psd`, `log10_frequency`, `log10_psd`.
  - **DFA files** contain: `scale`, `F`, `log10_scale`, `log10_F`.
  - **Exponents file** contains: `noise_type`, `beta`, `alpha`, `delta_beta_2alpha_minus_1`.

- Produces a small DataFrame summarizing which columns are present/missing per agent and noise type.

Include a Markdown comment explaining any mismatches found.

### 4. Exercise 5.1 – PSD and DFA comparison

For each noise type (`white`, `pink`, `red`):

#### 4.1 PSD images – side-by-side comparison

Create a **code cell** that:

- Loads images:

  ```python
img_psd_claude = mpimg.imread(CLAUDE_OUTPUTS / f'psd_{noise}.png')
img_psd_gemini = mpimg.imread(GEMINI_OUTPUTS / f'psd_{noise}.png')
  ```

- Creates a figure with two subplots:

  - Left: Claude PSD.
  - Right: Gemini PSD.

- Sets titles including noise type and agent, removes axes for clarity, and ensures identical figure size.

Repeat for each noise type.

#### 4.2 DFA images – side-by-side comparison

Analogous to PSD, but for:

- `dfa_white.png`
- `dfa_pink.png`
- `dfa_red.png`

#### 4.3 PSD curves – overlay from Parquet

For each noise type:

- Use combined PSD DataFrame (e.g., `psd_white`).
- Plot `log10_frequency` vs `log10_psd` for both agents on the same axes.
- Use distinct colors and markers; add legend, labels, and title.
- Include a Markdown cell describing observed differences (e.g., slope, low-frequency behavior, numerical noise).

#### 4.4 DFA curves – overlay from Parquet

Similarly:

- Plot `log10_scale` vs `log10_F` for both agents.
- Comment on slope and scaling behavior.

These plots collectively demonstrate that Exercise 5.1 (PSD and DFA calculation for colored noises) has been fulfilled by both agents, and they allow visual inspection of numerical stability and consistency. [file:1]

### 5. Exercise 5.2 – Exponent estimation and theoretical relation

#### 5.1 Exponent table

- Use the combined `exponents` DataFrame.
- Display a table grouped by `noise_type` and `agent`, showing:

  - `beta`
  - `alpha`
  - `delta_beta_2alpha_minus_1`

#### 5.2 Agent-to-agent differences

- Create a derived DataFrame that, for each `noise_type`, computes:

  - `delta_beta = beta_claude - beta_gemini`
  - `delta_alpha = alpha_claude - alpha_gemini`
  - `delta_delta = delta_claude - delta_gemini`

- Display this table.

#### 5.3 Visualization of exponents

- Create bar plots (e.g., via seaborn) for each noise type:

  - Bar chart of `beta` for both agents.
  - Bar chart of `alpha` for both agents.
  - Optional: bar chart of `delta_beta_2alpha_minus_1` showing how well \(\beta = 2\alpha - 1\) holds.

#### 5.4 Relation plot (optional, combined)

- Optionally recreate a figure similar to `psd_dfa_relation.png`, but with both agents:

  - x-axis: `2*alpha - 1`
  - y-axis: `beta`
  - Points colored by agent and noise type.
  - Diagonal line `y = x` to indicate perfect agreement.

#### 5.5 Discussion

Add a Markdown section that:

- Compares each agent’s `beta` and `alpha` with theoretical expectations for white, pink, red noise. [file:1]
- Comments on which agent’s estimates are closer to theory for each noise type.
- Evaluates numerically how close each agent is to satisfying \(\beta = 2\alpha - 1\).

### 6. Exercise 5.3 – Critical benchmark between agents

Create a dedicated Markdown section with subsections for each benchmark dimension:

1. **Physical coherence**
   - Discuss whether PSD and DFA plots match expected power-law behavior for each noise.
   - Note any anomalies (e.g., flattened spectra, incorrect slopes).

2. **Numerical stability**
   - Comment on smoothness and variability in the curves.
   - Note presence/absence of NaNs, infs, or noisy tails.

3. **Quality and clarity of graphs**
   - Evaluate axis labels, units, legends, use of log scales.
   - Compare layout and readability of each agent’s figures.

4. **Consistency across PSD and DFA**
   - Evaluate how well each agent’s exponents satisfy \(\beta = 2\alpha - 1\).

5. **Overall performance**
   - Summarize which agent performed better, where, and why.
   - Use concrete evidence from tables and plots in the notebook.

Optionally, assign qualitative scores (e.g., “better”, “comparable”, “worse”) per dimension and agent.

### 7. Optional challenge results (if present)

If additional files corresponding to the optional challenge exist (e.g., blue noise, multifractals, experimental signals, turbulence, EEG, financial series): [file:1]

- Detect additional PSD/DFA Parquet and PNG files with labels other than `white`, `pink`, `red`.
- Briefly load and list them in a table, noting which agent produced which extras.
- Optionally, show one or two representative comparisons.

Make clear this section is **optional** and not required for full credit, but is considered as extra work.

### 8. Final conclusion

End the notebook with a Markdown section that:

- States clearly whether each exercise item (5.1, 5.2, 5.3) has been satisfied by the combined work of the agents and this benchmark.
- Summarizes the strengths and weaknesses of each agent.
- States a concise final judgment (e.g., “Claude-code offers more physically coherent exponents; Gemini-cli provides slightly clearer DFA plots”, adapted to actual findings).

## Execution Notes

- The notebook should be executable via:

```bash
uv run jupyter nbconvert --to notebook --execute HandsOn05_Benchmark.ipynb
```

or by launching Jupyter (through `uv`) and executing all cells interactively.

- Do **not** write any new files into `claude-code/` or `gemini-cli/`; all reading is from their `outputs` directories only.
- Any additional files created (if absolutely necessary) must reside in the top-level directory or be embedded within the notebook.

## Notes to the Agent

- Do **not** look upwards in the folder structure; all necessary inputs are contained within:
  - Current directory (top-level project root),
  - `claude-code/`,
  - `gemini-cli/`.
- Never modify the contents of `claude-code/` and `gemini-cli/`; treat them as read-only.
- Use **`uv`** as the package manager and runner for all Python code.
- Ensure that `HandsOn05_Benchmark.ipynb` is fully self-contained and, when opened, shows all relevant figures, tables, and discussions needed for a perfect score on the exercise list.