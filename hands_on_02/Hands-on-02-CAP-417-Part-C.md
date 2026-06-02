# Hands-on 02 - CAP 417 - Part C

## Structure, Randomness, and the Cullen-Frey-Pearson Space

---

## Objective

In this hands-on activity, we will deepen the analysis of time series and explore how different types of noise influence statistical properties, with the following objectives:

- Investigate the effect of **shuffling** on time series
- Generate different types of noise (white, pink, and Brownian)
- Calculate higher-order statistics
- Represent results in the **Cullen-Frey-Pearson space**

---

## Deadline

**29/04/2026**

Submission via **Google Colab (shared link)**

---

## Theoretical Background (Summary)

While Brownian motion — modeled by the colored noise known as "red noise" — is an example of a process with temporal dependence, so-called white noise represents the absence of temporal correlation. "Colored" noises (pink, red) introduce **spectral structure** controlled by a parameter \(\beta\) (which will be covered in detail in the Spectral Analysis lecture).

As discussed in class, the **Cullen-Frey (Pearson) space** allows the characterization of distributions for time series using **Skewness and Kurtosis** in the parameter space: \(K \times S^2\).

---

## Part 2.1 — Shuffling

### Task

1. Generate a Brownian time series (\(N \geq 1000\))
2. Create a shuffled version (random shuffle of the points)
3. Calculate the statistical moments for:
   - Original series
   - Shuffled series

### Analysis

- Do the values change?
- How much do they change?
- What does this indicate about:
  - Temporal dependence
  - Distribution of values

### Theoretical Hypothesis to be Verified

> **Shuffling destroys the temporal structure, but does not necessarily alter the distribution.**

---

## Part 2.2 — Colored Noise Generation Algorithm

Create an algorithm for generating colored noises from the input: **spectral index value (\(\beta\))**.

### Task

Generate **100 realizations** for each noise type:

- White noise → \(\beta = 0\)
- Pink noise → \(\beta \approx 1\)
- Red noise (Brownian) → \(\beta \approx 2\)

---

## Part 2.3 — Cullen-Frey-Pearson Space

### Task

For all generated signals, plot:

- **x-axis** → (Skewness)²
- **y-axis** → Kurtosis

### Chart Specifications

- Each point characterizes how far each signal class deviates from the Gaussian distribution point (Skewness = 0 and Kurtosis = 3).
- Use different colors for:
  - White noise
  - Pink noise
  - Red noise
- *Tip: a dark background might work well here.*

---

## Part 2.5 (Optional)

Explore what AI agents produce when asked for:

**(i)** An advanced Cullen-Frey space plot that already includes pre-classified regions for different PDF models: log-normal, exponential, and another of your choice.

**(ii)** Ask the agents to include in the Cullen-Frey plot the region that would be produced by the **Generalized Extreme Value (GEV) distribution**, and how this could be obtained — noting that the GEV is parameterized by 3 parameters that include neither kurtosis nor skewness directly. Try to first build, in the conversation, a **lexicon on GEV**.

---

## Part 2.6 — Discussion

Answer the following questions:

1. Do the different noise types occupy distinct regions in this parameter space?
2. Is there overlap?
3. What does this indicate about the capacity of:
   - Skewness
   - Kurtosis
   
   ...to distinguish between processes?
4. Does shuffling alter the position in the Cullen-Frey space?
5. Present any conceptual and operational questions you may have.
6. Present any conceptual and operational questions you may have.

> **Remember: algorithms must always be generated with the help of two agents, and at the end a Benchmark must be presented. Always try to understand each step of both codes and note your questions or suggestions for improving the tool.**

---

## Evaluation Criteria

- Technical correctness
- Clarity of graphs
- Quality of analysis
- Interpretive capacity
- Benchmark presentation

---

*Prof. Reinaldo R. Rosa — 24/4/2026*
