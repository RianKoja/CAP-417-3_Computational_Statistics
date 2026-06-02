# CAP 417 – Computational Statistics – Part C – Prof. Reinaldo

## Hands-on 03 — Multimodality, KDE, and the Cullen-Frey Space

### Objective

This hands-on investigates time series whose probability distribution functions (PDFs) exhibit: multimodality, skewness, heavy tails, and mixtures of generating processes.

The focus is to compare: generating time series that produce multimodal histograms, fitting PDFs with KDE (Kernel Density Estimation), and locating where the fluctuation pattern of such a time series falls in the Cullen-Frey-Pearson space.

The **benchmark between two agents** strategy is used again, as in previous hands-on assignments.

**Submission deadline: 11/5/2026** via shared Google Colab.

---

### Theoretical Context

In previous exercises, the work focused mainly on:

- White noise
- Brownian noise
- Approximately Gaussian distributions

This assignment explores more complex systems, where:

- A single simple distribution does not adequately describe the data.

Examples include:

- Mixture of regimes
- Systems with multiple states
- Asymmetric processes
- Distributions with heavy tails

---

## Part 3.1 — Generation of Multimodal Series

### Objective

Build algorithms capable of generating time series whose PDF is:

- Bimodal
- Multimodal
- Asymmetric (skewed)

### Minimum Requirements

The algorithm must allow control over the following parameters:

#### Number of Modes

- M = 1 → unimodal
- M = 2 → bimodal
- M > 2 → multimodal

#### Overlap Between Modes

Investigate:

- How to increase the intersection between modes
- How to reduce the intersection between modes

#### Different Weights Between Modes

- One dominant mode
- Secondary modes

#### Non-Gaussian Modes

Examples:

- Gaussian
- Skewed (asymmetric)
- Laplace
- Others

---

## Part 3.2 — Histogram vs. KDE

### Objective

Compare:

- Traditional histogram
- KDE

to model the PDF of the generated signals.

### Tasks

**Implement:**

- Histogram
- KDE

**Investigate:**

- Effect of bandwidth
- Over-smoothing
- Overfitting (underfitting)

### Expected Discussion

Answer the following questions:

1. Does the histogram adequately represent the PDF?
2. When does KDE improve the modeling?
3. How does bandwidth change the results?
4. Can KDE detect multimodality?

---

## Part 3.3 — Cullen-Frey-Pearson Space

### Objective

Project the signals into the space defined by:

- **x-axis** → Skewness²
- **y-axis** → Kurtosis

### Tasks

**Generate:**

- Multiple realizations of each signal type

**Plot:**

- Gaussian signals
- Multimodal signals
- Asymmetric (skewed) signals
- Heavy-tailed signals

---

## Part 3.4 — Conceptual Discussion

Answer the following questions:

1. Where do multimodal signals fall in the Cullen-Frey space?
2. Do multimodal mixtures occupy classical regions?
3. Can different distributions fall close to each other?
4. Does Cullen-Frey detect multimodality?
5. Do KDE and Cullen-Frey provide complementary information?

---

## Benchmark Between Two Agents

As in previous hands-on assignments, the two-agent benchmark strategy is applied.

### Expected Comparisons

| Aspect | Comparison |
|---|---|
| Generation strategy | Same or different? |
| KDE | How was it implemented? |
| Bandwidth | Same approach? |
| Cullen-Frey | Visual differences? |
| Code organization | Clarity |
| Robustness | Numerical stability |
