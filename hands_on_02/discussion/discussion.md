# Theoretical Discussion

This document answers the theoretical questions from Part 2.6 of the assignment, based on the numerical results obtained from both Claude Code and Gemini CLI implementations.

## 1. Do the different noise types occupy distinct regions in the Cullen-Frey-Pearson space?

Yes, they do, although the degree of separation varies.
- **White Noise ($\beta=0$):** Occupies a very tight region centered at $(S^2 \approx 0, K \approx 3)$, which is the theoretical point for a Gaussian distribution.
- **Pink Noise ($\beta=1$):** Occupies a similar region to White noise but with slightly higher spread. It remains largely centered around the Gaussian point.
- **Red Noise ($\beta=2$):** Occupies a **distinctly different region**. Both agents found that Red noise realizations tend to have a lower raw kurtosis (mean $K \approx 2.35 \text{--} 2.40$) compared to White and Pink noise. The spread is also significantly larger for Red noise.

**Quantitative Support (Mean $\pm$ Std):**
| Noise Type | Skewness ($S$) | Kurtosis ($K$) |
|---|---|---|
| White | $0.00 \pm 0.08$ | $2.98 \pm 0.12$ |
| Pink | $0.03 \pm 0.14$ | $2.92 \pm 0.20$ |
| Red | $-0.02 \pm 0.44$ | $2.39 \pm 0.56$ |

## 2. Is there overlap between classes?

There is significant overlap between **White and Pink noise**. Because both are generated from Gaussian white noise and the spectral shaping for Pink noise ($\beta=1$) is relatively mild, their marginal distributions remain very close to Gaussian for $N=1000$.

There is **minimal overlap between Red noise and the others** in terms of the "center of mass" of the clusters, but because Red noise has high variance in its moment estimates (due to strong temporal correlation reducing the "effective" number of independent samples), some individual Red noise realizations can overlap with the White/Pink clusters.

## 3. Capacity of Skewness and Kurtosis to distinguish processes

Skewness and Kurtosis are **marginal statistics**; they characterize the distribution of values but ignore their temporal order.
- They are effective at distinguishing processes that have inherently different marginal distributions (e.g., Gaussian vs. Log-normal).
- They have **limited power** to distinguish processes that differ only in their correlation structure (like different colored noises) if those processes all result in nearly Gaussian marginals.
- The shift observed in Red noise ($K < 3$) is likely an artifact of the strong autocorrelation and the finite sample size ($N=1000$), where the series does not "explore" the full Gaussian distribution, leading to biased moment estimates.

## 4. Does shuffling alter the position in the Cullen-Frey space?

**No.** Both agents demonstrated that the mean, variance, skewness, and kurtosis remain identical (within floating-point precision) after shuffling.

**Theoretical Explanation:**
The Cullen-Frey-Pearson space is defined by $S^2$ and $K$. These statistics are calculated using the set of values in the time series, regardless of their order:
$$S = \frac{E[(X-\mu)^3]}{\sigma^3}, \quad K = \frac{E[(X-\mu)^4]}{\sigma^4}$$
Since shuffling is a random permutation that preserves the exact set of values (the marginal distribution), all order-independent moments are preserved. Thus, a series and its shuffled version map to the **exact same point** in the CFP space, even though their temporal structures (and ACFs) are completely different.

## 5. Conceptual Observations

- **Consistency:** Both agents produced remarkably consistent results despite using different FFT implementations (`rfft` vs `fft`) and different random number generators. This reinforces the robustness of the frequency-domain noise generation method.
- **Red Noise Bias:** The observation that Red noise (Brownian motion) realizations consistently show $K < 3$ for $N=1000$ is a classic example of how strong autocorrelation increases the variance and bias of statistical estimators.
- **Agent Choice:** Claude's use of `rfft` and the modern `Generator` API makes it slightly more aligned with current best practices in the Python scientific ecosystem, although Gemini's solution was equally correct in its results.
