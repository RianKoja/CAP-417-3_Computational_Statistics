## Objective

Implement a fully reproducible Python project that computes and analyzes Power Spectral Density (PSD), Detrended Fluctuation Analysis (DFA), and their spectral exponents for multiple colored noises (white, pink, red), and produces all results as files in a single `outputs` directory located alongside this `CLAUDE.md` file.

All requested items from the assignment must be satisfied **only by reading files from the `outputs` directory**, without inspecting the source code.

## Environment and Constraints

1. **Working directory**
   - Assume the current working directory is the directory containing this `CLAUDE.md` file.
   - Do **not** read from or write to directories outside this working directory.
   - Do **not** traverse upward in the folder hierarchy (no `..` in paths, no references outside this directory tree).

2. **Outputs directory**
   - Create a subdirectory named exactly `outputs` (lowercase) in the same directory as `CLAUDE.md`.
   - All generated artifacts (plots and data) **must** be stored inside this `outputs` directory.
   - The program should create `outputs` if it does not exist.

3. **Package management**
   - Use **`uv`** as the package manager and environment runner.
   - Assume a `pyproject.toml` will be managed via `uv`, but **do not** depend on any user-global Python environment.
   - Example commands (for human operators, not to be executed by the agent itself):
     - `uv init` to create the project (if not already created).
     - `uv add numpy scipy matplotlib pandas pyarrow`.

4. **Randomness and reproducibility**
   - Use a fixed random seed for all stochastic operations, e.g. `np.random.seed(417)`.
   - Ensure that **every run** of the main script with the same inputs yields **identical outputs**.

5. **Time series length and sampling**
   - Use the same length and sampling rate for all synthetic colored noises:
     - Number of samples: `N = 2**14` (16384 samples).
     - Sampling frequency: `fs = 1.0` (unit sampling; frequency axis in cycles per sample).

## High-level Structure

Implement the project as a single Python entry script, for example `main.py`, which can be invoked as:

```bash
uv run main.py
```

`main.py` must:

1. Generate white, pink, and red (Brownian) noise time series.
2. Compute their PSDs using a consistent method.
3. Compute their DFA fluctuation functions.
4. Estimate the spectral exponents `beta` (from PSD) and `alpha` (from DFA) via log-log least-squares fitting.
5. Validate (numerically) the theoretical relationship \(\beta = 2\alpha - 1\).
6. Produce the specified outputs listed in the section **Required output files**.
7. Store **all** outputs exclusively in the `outputs` directory.

## Detailed Requirements

### 1. Colored noise generation

Implement functions to generate:

- White noise (beta ≈ 0)
- Pink noise (beta ≈ 1)
- Red/Brownian noise (beta ≈ 2)

#### 1.1. General requirements

- Use NumPy arrays as the core representation.
- Each time series must be of length `N = 2**14`.
- Use the same random seed for all noise generations.

#### 1.2. White noise

- Generate by drawing samples from a standard normal distribution: `np.random.normal(0.0, 1.0, N)`.

#### 1.3. Pink noise (1/f)

- Use a frequency-domain construction:
  1. Generate white noise in the frequency domain.
  2. Scale magnitudes such that the amplitude spectrum decays as `1 / f^(beta/2)` with `beta = 1`.
  3. Enforce Hermitian symmetry so that the inverse FFT produces a real-valued time series.
  4. Use the discrete frequency grid defined by the FFT of length `N`.
  5. Set the zero-frequency component's scaling to 0 or to a finite value that avoids division by zero.

#### 1.4. Red/Brownian noise

Two acceptable approaches:

- **Integration approach**: cumulative sum of white noise, with optional normalization.
- **Frequency-domain approach**: same as pink noise, but with `beta = 2`.

Explicitly document in the code which approach is used, and ensure red noise has a much larger low-frequency power than white noise.

### 2. Power Spectral Density (PSD)

Implement a PSD computation function with the following requirements:

- Use `scipy.signal.welch` or an equivalent manual implementation.
- Use the same parameters for all signals:
  - Sampling frequency `fs = 1.0`.
  - Window type: `hann`.
  - Segment length: `nperseg = 1024`.
- Return frequency array `f` and PSD array `Pxx`.
- Use logarithmic (base 10) scaling only at the analysis/plotting stage, not for the raw PSD values.

### 3. Detrended Fluctuation Analysis (DFA)

Implement DFA for each time series as follows:

1. **Profile construction**
   - Given time series `x[n]`, subtract the mean and compute cumulative sum `y[k] = sum_{i=0}^{k} (x[i] - mean(x))`.

2. **Box sizes (scales)**
   - Define box sizes as:
     - `s_min = 16`
     - `s_max = N / 4` (integer)
     - Use logarithmically spaced scales (e.g., 20 scales) between `s_min` and `s_max`.

3. **Detrending**
   - For each scale `s`, divide `y` into non-overlapping windows of length `s`.
   - For each window, fit a first-order polynomial (linear trend) using least squares.
   - Subtract the local trend from the window profile.

4. **Fluctuation function**
   - For each detrended window, compute the mean squared deviation.
   - Average over all windows at scale `s` to obtain `F(s)^2`, then use `F(s) = sqrt(average)`.

5. **Output of DFA function**
   - Return arrays `(s, F)` where `s` are the scales and `F` are the corresponding fluctuation function values.

### 4. Log-log least-squares fitting

Implement a generic function to fit a power-law relationship `y = C * x^k` using least squares in log-log space.

1. Take inputs `(x, y)` where `x > 0` and `y > 0`.
2. Compute `log10(x)` and `log10(y)`.
3. Fit a straight line `log10(y) = a + k * log10(x)` using NumPy's `polyfit` of degree 1.
4. Return slope `k` and intercept `a`.

Apply this to:

- PSD in a selected frequency band (e.g., excluding the very lowest and highest frequencies).
- DFA fluctuation function `F(s)` versus `s`.

#### 4.1. Exponent extraction

- For PSD:
  - Use `beta = -k_psd`, where `k_psd` is the slope of `log10(Pxx)` versus `log10(f)` in the chosen frequency range.
- For DFA:
  - Use `alpha = k_dfa`, where `k_dfa` is the slope of `log10(F)` versus `log10(s)`.

### 5. Validation of theoretical relation

- For each noise type (white, pink, red), compute `beta` and `alpha`.
- Compute the difference `delta = beta - (2 * alpha - 1)`.
- Store numerical results for `beta`, `alpha`, and `delta` for each noise in a structured table.

### 6. Benchmarking Gemini vs Claude

Although the actual interaction with Gemini and Claude happens outside this codebase, this project must provide all the **numerical and graphical outputs** needed for a later benchmark.

Therefore, the outputs must include:

- PSD plots for each noise type.
- DFA plots for each noise type.
- Tabulated numerical values of `beta`, `alpha`, and `delta` for each noise.

## Required output files

All paths below are **relative to the `outputs` directory**. The project **must** create exactly these files (file names must match precisely), plus any additional intermediate files if needed. However, the following files are **mandatory** and will be used for the final report.

### 1. Parquet files (data)

1. `outputs/psd_white.parquet`
   - Columns: `frequency`, `psd`, `log10_frequency`, `log10_psd`.
   - Contains PSD data and log-transformed values for white noise.

2. `outputs/psd_pink.parquet`
   - Same schema as `psd_white.parquet`, but for pink noise.

3. `outputs/psd_red.parquet`
   - Same schema as `psd_white.parquet`, but for red noise.

4. `outputs/dfa_white.parquet`
   - Columns: `scale`, `F`, `log10_scale`, `log10_F`.
   - DFA fluctuation data for white noise.

5. `outputs/dfa_pink.parquet`
   - Same schema as `dfa_white.parquet`, but for pink noise.

6. `outputs/dfa_red.parquet`
   - Same schema as `dfa_white.parquet`, but for red noise.

7. `outputs/exponents.parquet`
   - Columns:
     - `noise_type` (string: `white`, `pink`, `red`)
     - `beta`
     - `alpha`
     - `delta_beta_2alpha_minus_1` (beta minus `(2 * alpha - 1)`)
   - Contains one row per noise type.

### 2. Image files (plots)

Use `matplotlib` (or equivalent) to produce publication-quality figures with clear labels, legends, and titles. Save all images as PNG files with at least 300 dpi resolution.

1. `outputs/psd_white.png`
   - Log-log plot of PSD vs frequency for white noise.
   - Include estimated `beta` in the title or as text inside the plot.

2. `outputs/psd_pink.png`
   - Log-log plot of PSD vs frequency for pink noise.
   - Include estimated `beta`.

3. `outputs/psd_red.png`
   - Log-log plot of PSD vs frequency for red noise.
   - Include estimated `beta`.

4. `outputs/dfa_white.png`
   - Log-log plot of DFA fluctuation function `F(s)` vs scale `s` for white noise.
   - Include estimated `alpha`.

5. `outputs/dfa_pink.png`
   - Log-log plot of DFA fluctuation function `F(s)` vs scale `s` for pink noise.
   - Include estimated `alpha`.

6. `outputs/dfa_red.png`
   - Log-log plot of DFA fluctuation function `F(s)` vs scale `s` for red noise.
   - Include estimated `alpha`.

7. `outputs/psd_dfa_relation.png`
   - Optional but recommended figure.
   - Scatter or bar plot illustrating `beta` versus `2*alpha - 1` for each noise type.
   - Clearly indicate the deviation `delta`.

### 3. Additional spectral characterizations (optional challenge)

If you implement additional optional analyses (blue noise, multifractal time series, experimental signals, turbulence, EEG, financial series), store their outputs using the following naming conventions:

- PSD Parquet: `psd_<label>.parquet`
- DFA Parquet: `dfa_<label>.parquet`
- PSD plot: `psd_<label>.png`
- DFA plot: `dfa_<label>.png`

where `<label>` is a lowercase string without spaces (e.g., `blue`, `eeg`, `finance`).

These optional files are **not required** for minimum compliance, but if present, they must obey the same schema as the core files.

## Execution Flow

1. Initialize random seed.
2. Create `outputs` directory if it does not exist.
3. Generate white, pink, and red noise time series.
4. For each time series:
   - Compute PSD (`f`, `Pxx`).
   - Compute DFA (`s`, `F`).
   - Fit log-log PSD to obtain `beta`.
   - Fit log-log DFA to obtain `alpha`.
5. Store PSD and DFA data into the corresponding Parquet files.
6. Store exponents and consistency checks into `exponents.parquet`.
7. Generate and save all plots as specified.

## Numerical Stability and Quality Notes

- Avoid taking logs of zero or negative values; restrict fitting to ranges where both `x` and `y` are strictly positive.
- Exclude the DC component (frequency = 0) from PSD log-log fitting.
- For DFA, ignore scales where the number of windows is less than a minimum (e.g., at least 4 windows per scale).
- Use double precision (default NumPy `float64`).

## Notes to the agent

- Do **not** look upwards in the folder structure; all code and outputs must remain within the current directory and its `outputs` subdirectory.
- Use **`uv`** as the package manager and runner for Python dependencies and execution.
- Design the project so that a separate reporting script or notebook can fully reconstruct all required interpretations and figures **only by reading Parquet and PNG files from the `outputs` directory**, without inspecting the implementation code.