# CAP417 – Part C – Hands-on 01 – 22/4/2026

## Objective

In this first hands-on session, the goal is to introduce fundamental concepts of stochastic processes and descriptive statistics through the practical implementation of algorithms.

You must:

- Generate a time series based on Brownian noise
- Visualize the data through a histogram
- Calculate the first four statistical moments

## Theoretical Background

Brownian motion, observed by Robert Brown and modeled by Albert Einstein, is a classic example of a non-linear stochastic process (see and practice simulations at https://labs.minutelabs.io/Brownian-Motion/).

Statistical moments describe fundamental properties of a distribution:

- **1st moment**: Mean
- **2nd moment**: Variance
- **3rd moment**: Skewness (Asymmetry)
- **4th moment**: Kurtosis

## Part 1 — Time Series Generation

Generate three sets of time series with N points (N = 100, 1000, 10000).

Use:
- Gaussian noise
- Cumulative sum (to obtain Brownian motion)

save the data in a parquet file named tseries_{N}.parquet in this folder.

## Part 2 — Visualization
For each series:
- Build a histogram of the generated series save if as "histogram_{N}.svg" in this folder.
- Qualitatively discuss the shape of the distribution in a markdown file named "histogram_{N}.md" in this folder.

## Part 3 — Statistical Moments

Calculate:

1. Mean
2. Variance
3. Skewness (Asymmetry)
4. Kurtosis (both Pearson and Fisher)

Save results in a parquet file named "moments_{N}.parquet" in this folder.

*This hands-on connects: probability theory, physics (diffusion), programming with agents, and statistical analysis of time series data.*

*…exactly the kind of interdisciplinary thinking of Carl Friedrich Gauss*

use python and uv as a package manager
All used code must be in this folder.