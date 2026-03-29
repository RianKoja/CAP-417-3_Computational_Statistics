This work will create a report in typst with dedicated documents for each part. This document shall embed plots created in python and numbers generated in python shall be written on a format readable by typst to import those numebrs as cosntants to be used in the typst document. No notebook usage.

The report shall be written in english.


## Part 1: Random number generation study
Use R, julia, python and rust to generate random numbers using the default generators and compare the results. We will always control the seeds and show them on the report.

We will use methods that allow getting numbers from thsoe generators using an api that looks just like python's standard `random` library. For example, in python we will use `random.random()` to get a random number in the [0,1] interval, then `julia_rng.random()` will use a wrapper to call the Julia RNG, and `rust_rng.random()` will use a wrapper to call the Rust RNG, and `r_rng.random()` will use a wrapper to call the R RNG.

The goal is to show the default generators in each language for numbers in the [0,1] interval.

We'll use plotly in the nb.ipynb to show the results, which shall contain:
- Histograms of the generated numbers
- Kernel density estimates of the generated numbers
- QQ-plots of the generated numbers
- Autocorrelation plots of the generated numbers
- Spectral density plots of the generated numbers
- Chi-squared tests of the generated numbers
- Kolmogorov-Smirnov tests of the generated numbers

We will not attempt to check for period of the generated numbers. Check the table below and use it for justification:

| Language                | Default RNG          | Period                                     | Source               |
| ----------------------- | -------------------- | ------------------------------------------ | -------------------- |
| Python (random module)  | Mersenne Twister     | 219937−12^{19937} - 1219937−1              | python​              |
| NumPy (default_rng)     | PCG64                | 21282^{128}2128                            | numpy​               |
| Julia (default_rng)     | MersenneTwister      | 219937−12^{19937} - 1219937−1              | discourse.julialang​ |
| R                       | Marsaglia-Multicarry | > 2602^{60}260                             | nku​                 |
| Rust (rand::thread_rng) | ChaCha12             | 22562^{256}2256 (expected for full stream) | stackoverflow​       |

We will present a summary table with a language comparison, showing methics we could test and the expected periods.

This will all be plotted and presented in the report. The figures for plots shall all use a 4x4 arrangement of subplots, one for each language.

Astral's uv is the packages manager. Cargo is installed. homebrew is available. Check if anythign else is needed.

## Part 2
With less ambition, we'll use integer numbers randomly generated in [1, 10] and:
- For a 5-numbers sequence: min, average, mode, median, max, range, sum,
variance, standard deviation
- For a 100-numbers sequence: min, average, mode, median, max, range, sum,
variance, standard deviation
- Distribution (controlling bins), and percentiles
- Average as a weighted sum

## Part 3: calculating pi 

use  The Coprime Number Trick (More Surprising!)

This one is genuinely magical: pick two random positive integers. The probability that they share **no common factors** (i.e., are coprime) is exactly \(\frac{6}{\pi^2}\).

So if you run \(N\) random pairs and find that a fraction \(p\) of them are coprime, you can solve for π:

\[\pi \approx \sqrt{\frac{6}{p}}\]

This works because of the deep connection between the Riemann zeta function and prime numbers — \(\zeta(2) = \frac{\pi^2}{6}\).  It's a completely non-geometric way to discover π lurking in number theory. [


## How They Compare

| Method | Inputs needed | Intuition | Convergence |
|---|---|---|---|
| Monte Carlo circle | 2 random floats per trial | Geometric area ratio | ~2.7/N variance  
| Coprime integers | 2 random integers per trial | Number theory / primes | ~1.59/N variance 
| Buffon's Needle | 1 random float + 1 angle | Geometric probability | Slower  

The coprime method actually has **slightly better variance** than the dartboard — meaning it converges a bit faster for the same number of trials.  However, both methods converge very slowly overall; you need billions of samples to get even 6 correct decimal places.  They are prized more for their elegance and surprise than their computational efficiency. 

Lets plot  the number of samples on the x-axis and the error and the  1.59/N deviation as a dashed line on the y-axis and use log scale for both axes.


# part4: the bootstrap properties with Lean 4
This project aims to show the properties of the bootstrap method using Lean 4.
The goal is to prove the distribution of the bootstrap mean and variance of the sample.

## What the Project Does

It formally encodes three algebraic facts about the bootstrap method in statistics:

1. **`bootstrap_mean_unbiased`** — the bootstrap sample mean is identical to the empirical mean by definition (proved by `rfl`, meaning both sides reduce to the same expression)
2. **`empiricalVariance_eq`** — unfolds the empirical variance into its raw sum form \( \frac{1}{n}\sum X_i^2 - \bar{X}^2 \)
3. **`bootstrap_variance_of_mean`** — the bootstrap variance of the mean statistic equals \( \hat{\sigma}^2 / n \), the plug-in analogue of the true \( \text{Var}(\bar{X}) = \sigma^2/n \)

No theorem uses `sorry`, meaning every proof is **fully closed** — Lean's kernel has verified each claim from first principles.

***

## How to Verify It Passes

```bash
lake build
```

If it prints `Build completed successfully.` with no errors, all proofs are accepted by Lean's type checker.

**To explicitly check for no `sorry`:**
Ensure this line is present anywhere in `Theorems.lean`:
```lean
#check @bootstrap_variance_of_mean  -- Lean prints the full type if accepted
```

***


# General notes
all code shall be as compact and concise as possible, minimize line count, but keep clarity as a priority.
Don't save samples in csv! Use functions to generate them on the fly. Cache results with joblib cache decorator for speed.