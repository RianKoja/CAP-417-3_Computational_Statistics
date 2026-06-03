# Benchmark Report — Hands-on 02

This report compares the solutions provided by Claude Code and Gemini CLI for the Hands-on 02 assignment focusing on structure, randomness, and the Cullen-Frey-Pearson (CFP) space.

## 1. Algorithmic Comparison

| Aspect | Claude Code | Gemini CLI |
|--- |--- |--- |
| Brownian series generation | `cumsum` of Gaussian increments using `default_rng` | `cumsum` of Gaussian increments using `np.random.seed` |
| Shuffle method | `rng.permutation` | `np.random.permutation` |
| Colored noise generation | FFT-domain filtering using `rfft`/`irfft` | FFT-domain filtering using `fft`/`ifft` |
| Moment computation (library) | `scipy.stats.skew`, `stats.kurtosis` | `scipy.stats.skew`, `stats.kurtosis(fisher=False)` |
| CFP plot approach | Matplotlib `scatter` in dark background | Matplotlib `scatter` in dark background |

### Algorithmic Observations
- **Normalization:** Both agents correctly standardized the colored noise realizations to zero mean and unit variance.
- **Kurtosis Convention:** Both agents used the raw kurtosis (K=3 for Gaussian) for the CFP space, though Claude explicitly calculated it as `excess + 3` while Gemini used the `fisher=False` parameter.
- **Efficiency:** Claude used `rfft`, which is more efficient for real signals, whereas Gemini used the standard `fft`.

## 2. Numerical Results Comparison

### 2.1 Brownian Series Moments (Part 2.1)
The two agents produced different Brownian series due to different random number generator initializations. However, both agents successfully demonstrated that **shuffling preserves the statistical moments** (mean, variance, skewness, kurtosis) while destroying the temporal correlation.

| Agent | Original Mean | Shuffled Mean | Difference |
|--- |--- |--- |--- |
| Claude | -14.459521 | -14.459521 | 0.000000 |
| Gemini | -0.349653 | -0.349653 | 0.000000 |

### 2.2 Colored Noise Moments Comparison
Based on `benchmark/moments_comparison.csv` (averages over 100 realizations):

| Noise Type | Metric | Claude Mean | Gemini Mean | Abs Diff Mean |
|--- |--- |--- |--- |--- |
| White | Skewness | -0.0004 | 0.0075 | 0.0080 |
| White | Kurtosis | 2.9791 | 3.0178 | 0.0387 |
| Pink | Skewness | 0.0269 | -0.0125 | 0.0394 |
| Pink | Kurtosis | 2.9157 | 2.8877 | 0.0280 |
| Red | Skewness | -0.0211 | -0.0706 | 0.0495 |
| Red | Kurtosis | 2.3917 | 2.3577 | 0.0340 |

Numerical results are highly consistent, with differences in means typically less than 0.05.

### 2.3 Qualitative CFP Consistency
Both agents generated CFP scatter plots that show:
- **White Noise** clustered tightly around the Gaussian point (S²=0, K=3).
- **Pink Noise** showing slightly more spread but still centered near the Gaussian point.
- **Red Noise** showing significantly more spread and a downward shift in kurtosis (lower mean K), occupying a distinct region below the White/Pink clusters.

## 3. Benchmark Timing

The execution time for each script (generating 300 noise realizations and several plots) was recorded:

| Agent | Execution Time (s) |
|--- |--- |
| Claude Code | 15.67 |
| Gemini CLI | 18.25 |

Claude Code was approximately 14% faster than Gemini CLI, likely due to the use of `rfft` and more streamlined plotting calls.
