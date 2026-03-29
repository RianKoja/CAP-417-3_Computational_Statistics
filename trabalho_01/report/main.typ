#set page(
  paper: "a4",
  margin: (x: 2cm, y: 2.5cm),
)
#set text(size: 11pt, lang: "en")
#set par(justify: true)

#import "metrics.typ": *

= Part 1: Random Number Generation Study

== Introduction

A *pseudorandom number generator* (PRNG) is a deterministic algorithm that,
given an initial value called the *seed*, produces a sequence of numbers whose
statistical properties resemble those of a truly random sequence.
Because the algorithm is deterministic, the entire sequence is reproducible
whenever the same seed is used — a critical property for scientific
reproducibility.  This study uses *seed = 42* throughout.

A PRNG is characterised by its *period*: the length of the sequence before it
repeats.  Modern PRNGs achieve periods so large (often $> 2^(100)$) that
exhausting them in any practical computation is impossible.  A second key
requirement is *uniformity*: when the output is mapped to $[0, 1]$, values
should be indistinguishable from draws of the continuous uniform
distribution $U[0,1]$.

This study generates $N = "10,000"$ samples from the default PRNG of four
languages and evaluates quality using statistical tests and visual diagnostics.

== Default RNG Summary

#table(
  columns: (1fr, 1.5fr, 1.6fr, 1fr),
  inset: 6pt,
  align: horizon,
  [*Language*], [*Default RNG*], [*Period*], [*Source*],
  [Python], [Mersenne Twister], [$2^(19937) - 1$], [cpython],
  [Julia],  [MersenneTwister], [$2^(19937) - 1$], [julialang],
  [R],      [Marsaglia-Multicarry], [$> 2^(60)$], [nku.edu],
  [Rust],   [ChaCha12],            [$2^(256)$],   [stackoverflow],
)

The *Mersenne Twister* (MT19937) is a generalised feedback shift-register
generator with a period of $2^(19937)-1$ and good equidistribution in up to
623 dimensions.  It is the most widely deployed PRNG in scientific software,
though it is not cryptographically secure.

*Marsaglia-Multicarry* uses a multiply-with-carry recurrence.  Its period
exceeds $2^(60)$, which is adequate for the sample sizes used here.

*ChaCha12* originates from the ChaCha stream cipher.  Designed for
cryptographic use, it provides an astronomically large period of $2^(256)$
and passes all known statistical randomness tests.

== Goodness-of-Fit Tests

=== Chi-Squared Uniformity Test

The chi-squared test partitions $[0,1]$ into $k = 10$ equally spaced bins
and compares the observed count $O_i$ in each bin with the expected count
$E_i = N/k$ under a uniform distribution.  The test statistic is

$ chi^2 = sum_(i=1)^k (O_i - E_i)^2 / E_i $

Under the null hypothesis $H_0$ (the data are $U[0,1]$), this statistic
follows a $chi^2$ distribution with $k - 1 = 9$ degrees of freedom (one
degree is lost because the bin counts must sum to $N$).  The *p-value* is the
probability of observing a statistic at least as large as the one computed,
assuming $H_0$.  A p-value above the conventional threshold $alpha = 0.05$
means we do not have sufficient evidence to reject uniformity.

=== Kolmogorov-Smirnov (KS) Test

The KS test compares the empirical CDF
$hat(F)_n (x) = (1\/n) sum_(i=1)^n bb(1)[X_i <= x]$ against the theoretical
CDF $F(x) = x$ for $x in [0, 1]$.  The test statistic is the maximum absolute
discrepancy:

$ D_n = sup_(x in [0,1]) lr(|hat(F)_n (x) - F(x)|) $

The KS test does not require binning and is more sensitive than $chi^2$ to
deviations near the tails.  A high p-value again supports $H_0$.

=== Results

#table(
  columns: (1fr, 1fr, 1fr, 1fr, 1fr),
  inset: 8pt,
  align: horizon,
  [*Language*], [$chi^2$ *stat*], [$chi^2$ *p-value*], [*KS stat*], [*KS p-value*],
  [Python], [#python_chi2_stat], [#python_chi2_p], [#python_ks_stat], [#python_ks_p],
  [Julia],  [#julia_chi2_stat],  [#julia_chi2_p],  [#julia_ks_stat],  [#julia_ks_p],
  [R],      [#r_chi2_stat],      [#r_chi2_p],      [#r_ks_stat],      [#r_ks_p],
  [Rust],   [#rust_chi2_stat],   [#rust_chi2_p],   [#rust_ks_stat],   [#rust_ks_p],
)

All generators pass both tests at the $alpha = 0.05$ level — every p-value
exceeds 0.05, so uniformity is not rejected for any language.  Julia's KS
p-value (#julia_ks_p) is the smallest, but the corresponding statistic
(#julia_ks_stat) is tiny in absolute terms and well within the range of
normal sampling variation for $N = "10,000"$.

== Visual Diagnostics

@part1_matrix presents a $4 times 4$ diagnostic matrix.  Each *column*
corresponds to one language; each *row* to a different analysis tool.

- *Row 1 — Histogram + KDE*: Bar heights approximate the theoretical density
  of 1.  The kernel density estimate (red curve) should be flat across
  $[0, 1]$, confirming uniformity.

- *Row 2 — Q-Q Plot*: The $i$-th order statistic is plotted against the
  $i \/ (n+1)$ quantile of $U[0,1]$.  Alignment with the 45° diagonal
  indicates a distributional match; curvature signals a systematic mismatch.

- *Row 3 — Autocorrelation Function (ACF)*: The ACF at lag $ell$ measures
  the linear correlation between $X_t$ and $X_(t+ell)$.  Bars near zero for
  all lags indicate independence of successive outputs — a key requirement
  for a good PRNG.

- *Row 4 — Power Spectral Density (PSD)*: Estimated via Welch's method, the
  PSD shows how variance is distributed across frequencies.  A *flat
  (white-noise) spectrum* confirms no hidden periodicities.  Spikes would
  reveal cycles that could be exploited.

#figure(
  image("../outputs/plots/part1_matrix.png", width: 100%),
  caption: [
    Statistical diagnostics for each language's default PRNG ($N=10{,}000$,
    seed $=42$).  Columns: Python, Julia, R, Rust.  Rows: histogram + KDE,
    Q-Q plot against $U[0,1]$, ACF, and power spectral density.
  ],
) <part1_matrix>

All four generators show flat histograms, linear Q-Q plots, near-zero
autocorrelations, and flat power spectra — consistent with high-quality
uniform random number generation.

#pagebreak()

= Part 2: Descriptive Statistics on Integer Sequences

== Introduction

Descriptive statistics summarise the essential features of a data set with a
small number of measures.  We draw samples uniformly from the integer set
$\{1, 2, dots.c, 10\}$ and compute standard location and spread statistics.
Comparing a small sample ($n=5$) with a larger one ($n=100$) illustrates the
*law of large numbers*: as $n$ grows, sample statistics converge to their
population counterparts.  All samples use *seed = 42*.

For a discrete uniform distribution on $\{1, dots.c, M\}$, the exact
population parameters are

$ mu = (M+1)/2, quad sigma^2 = (M^2-1)/12 $

With $M = 10$: $mu = 5.5$ and $sigma^2 = 8.25$.

== Key Statistics Defined

Given a sample $x_1, dots.c, x_n$:

- *Arithmetic mean*: $overline(x) = (1\/n) sum_(i=1)^n x_i$ — the balance
  point of the empirical distribution; minimises the sum of squared
  deviations from any constant.

- *Median*: the middle value of the sorted sample (average of two middle
  values for even $n$).  Robust to extreme observations.

- *Mode*: the most frequently occurring value.  For small $n$ it may not
  reflect any genuine concentration.

- *Sample variance* (Bessel-corrected):
  $s^2 = (1\/(n-1)) sum_(i=1)^n (x_i - overline(x))^2$ — an unbiased
  estimator of the population variance $sigma^2$.  The factor $n-1$ (rather
  than $n$) corrects for the fact that the mean is estimated from the same
  data, effectively using one degree of freedom.

- *Standard deviation*: $s = sqrt(s^2)$ — expressed in the same units as
  the data, making it directly interpretable.

- *Range*: $max(bold(x)) - min(bold(x))$ — the simplest measure of spread;
  sensitive to extremes.

- *Sum*: $S = sum_(i=1)^n x_i = n overline(x)$.

== 5-Sample Sequence

With only 5 observations, all estimates are highly variable.  The standard
error of the mean is $s \/ sqrt(n) = s \/ sqrt(5) approx 0.45 s$, so the
sample mean can easily deviate by a full unit from the true $mu = 5.5$ by
chance alone.  The mode reflects whichever value happened to be drawn
most often — not a population property.

#table(
  columns: (1fr, 1fr),
  inset: 8pt,
  [*Metric*], [*Value*],
  [Min],              [#p2_5_min],
  [Mean ($overline(x)$)], [#p2_5_avg],
  [Mode],             [#p2_5_mode],
  [Median],           [#p2_5_median],
  [Max],              [#p2_5_max],
  [Range],            [#p2_5_range],
  [Sum],              [#p2_5_sum],
  [Variance ($s^2$)], [#p2_5_var],
  [Std Dev ($s$)],    [#p2_5_std],
)

== 100-Sample Sequence

With $n = 100$ samples the estimates stabilise considerably.  The standard
error of the mean drops to $s \/ 10$, so we expect the sample mean to land
very close to the theoretical $mu = 5.5$.

#table(
  columns: (1fr, 1fr),
  inset: 8pt,
  [*Metric*], [*Value*],
  [Min],                 [#p2_100_min],
  [Mean ($overline(x)$)],[#p2_100_avg],
  [Weighted mean],       [#p2_100_weighted_avg],
  [Mode],                [#p2_100_mode],
  [Median],              [#p2_100_median],
  [Max],                 [#p2_100_max],
  [Range],               [#p2_100_range],
  [Sum],                 [#p2_100_sum],
  [Variance ($s^2$)],    [#p2_100_var],
  [Std Dev ($s$)],       [#p2_100_std],
  [$Q_1$ — 25th pct.],   [#p2_100_p25],
  [$Q_2$ — 50th pct.],   [#p2_100_p50],
  [$Q_3$ — 75th pct.],   [#p2_100_p75],
)

=== Mean as a Weighted Sum

The arithmetic mean can be re-expressed as a weighted sum over the *distinct*
observed values $v_j$, using their relative frequencies as weights:

$ overline(x) = sum_j w_j v_j, quad w_j = n_j / n, quad sum_j w_j = 1 $

where $n_j$ is the count of occurrences of value $v_j$.  The weights
$\{w_j\}$ define the *empirical probability mass function* $hat(p)$, so this
identity is exactly $E_(hat(p))[X]$ — the expected value under the empirical
distribution.  It shows that the ordinary arithmetic mean is a special case
of the general expectation operator.  In the table above the plain mean
(#p2_100_avg) and the weighted mean (#p2_100_weighted_avg) are equal by
construction.

=== Percentiles and Quartiles

The *$p$-th percentile* $P_p$ is the value below which a fraction $p\/100$
of the observations fall.  The three *quartiles* $Q_1, Q_2, Q_3$ divide the
ranked sample into four equal parts:

$ Q_1 = P_(25), quad Q_2 = P_(50) = "Median", quad Q_3 = P_(75) $

The *interquartile range* $"IQR" = Q_3 - Q_1$ is a robust measure of
dispersion: unlike the range, it ignores the most extreme values and forms the
basis of box plots.  By definition, the middle 50% of the data lie inside
$[Q_1, Q_3]$.

== Distribution Plots

@part2_dist shows the empirical frequency distributions for both sample sizes
side by side.  The $n=5$ panel (left) illustrates how individual draws
dominate: any value appearing twice becomes the mode, and the histogram looks
nothing like the expected flat distribution.  The $n=100$ panel (right) is
visibly smoother, approaching the theoretical frequency of 10 counts per bin,
with mean, median, and quartiles annotated.

#figure(
  image("../outputs/plots/part2_distribution.png", width: 100%),
  caption: [
    Frequency distributions for $n=5$ (left) and $n=100$ (right), both with
    seed $=42$.  Red dashed: mean; green dotted: median; orange / purple
    dash-dot: $Q_1$ / $Q_3$ (right panel only).
  ],
) <part2_dist>

@part2_pct provides two complementary views of the $n=100$ sample.  The
*box plot* (left) compares the spread of both samples at a glance using a
five-number summary (min, $Q_1$, median, $Q_3$, max); the red line inside
the box marks the median.  The $n=5$ box is wide and asymmetric due to
sampling noise, while the $n=100$ box is compact and centred near 5.5.  The
*empirical CDF* (right) shows $hat(F)_(100)(x)$ as a staircase; dashed
vertical lines mark the quartiles and dotted horizontal lines mark the
corresponding probabilities (0.25, 0.50, 0.75), illustrating how percentiles
are read directly off the CDF.

#figure(
  image("../outputs/plots/part2_percentiles.png", width: 100%),
  caption: [
    Left: box plot comparison between $n=5$ and $n=100$.  Right: empirical
    CDF for $n=100$ with quartile markers.
  ],
) <part2_pct>

#pagebreak()

= Part 3: Estimating $pi$ via the Coprime Trick

== Mathematical Foundation

Two positive integers $a$ and $b$ are *coprime* if their greatest common
divisor equals one: $gcd(a, b) = 1$.  The probability that two positive
integers chosen uniformly at random are coprime is

$ P(gcd(a, b) = 1) = 6 / pi^2 approx 0.6079 $

This result follows from the *Riemann Zeta function*, defined for $s > 1$ as

$ zeta(s) = sum_(n=1)^infinity 1/n^s $

*Euler's product formula* factorises this over the prime numbers:

$ zeta(s) = product_(p "prime") 1/(1 - p^(-s)) $

The Basel problem (solved by Euler in 1735) establishes $zeta(2) = pi^2\/6$.
The probability that a uniformly random integer is *not* divisible by prime
$p$ is $(1 - 1\/p)$.  Divisibility by distinct primes is independent, so by
inclusion-exclusion over all primes:

$ P(gcd(a,b) = 1)
  = product_(p "prime") (1 - 1/p^2)
  = 1/zeta(2)
  = 6/pi^2 $

This identity connects a geometric constant ($pi$) to the arithmetic of prime
numbers through complex analysis — one of the deepest surprises in
mathematics.

== Estimation Procedure

We draw $N$ independent pairs $(a_i, b_i)$ uniformly from
$\{1, dots.c, 2^(31)-1\}$ (approximating a draw from the positive integers)
with *seed = 42*, and compute the running fraction of coprime pairs:

$ hat(p)_N = 1/N sum_(i=1)^N bb(1)[gcd(a_i, b_i) = 1] $

Inverting the coprimality probability gives the estimator

$ hat(pi)_N = sqrt(6 / hat(p)_N) $

By the *law of large numbers*, $hat(p)_N arrow.r 6\/pi^2$ as
$N arrow.r infinity$, so $hat(pi)_N arrow.r pi$.

== Convergence and Error Analysis

By the *Central Limit Theorem*, $hat(p)_N$ is approximately normal with
variance $"Var"(hat(p)_N) = p(1-p)\/N$ where $p = 6\/pi^2$.  Applying the
*delta method* to $f(p) = sqrt(6\/p)$, with derivative
$f'(p) = -sqrt(6)\/(2p^(3\/2))$:

$ "SD"(hat(pi)_N)
  approx |f'(p)| dot sqrt((p(1-p))/N)
  = sqrt(6) / (2 p^(3/2)) dot sqrt((p(1-p))/N)
  = sqrt((6(1 - 6\/pi^2)) / (4(6\/pi^2)^2 N))
  approx sqrt(1.59 / N) $

The *standard deviation* of the estimate is therefore $approx sqrt(1.59\/N)$,
converging as $O(N^(-1\/2))$ — the universal rate of Monte Carlo estimators.

#table(
  columns: (1fr, 1fr, 1fr, 1fr),
  inset: 7pt,
  align: horizon,
  [*Method*], [*Inputs per trial*], [*Intuition*], [*Std Dev*],
  [Coprime integers], [2 random integers], [Number theory / primes], [$approx sqrt(1.59\/N)$],
  [MC circle (dartboard)], [2 random floats], [Geometric area ratio], [$approx sqrt(2.7\/N)$],
  [Buffon's Needle], [1 float + 1 angle], [Geometric probability], [Slower],
)

The coprime trick has a *smaller* standard deviation than the dartboard method,
making it marginally more efficient per sample pair.  Both methods are prized
for their elegance rather than computational speed: achieving six correct
decimal places requires $O(10^(12))$ samples regardless of method.

== Results

Using $N = $ #pi_samples samples, the final estimate is
$hat(pi) = $ #pi_estimate (true value: $pi approx 3.14159265$).

#figure(
  image("../outputs/plots/pi_convergence.png", width: 85%),
  caption: [
    Log-log plot of the absolute estimation error $|hat(pi)_N - pi|$ as a
    function of sample size $N$.  The dashed line is the theoretical
    $sqrt(1.59\/N)$ standard-deviation envelope derived via the delta method.
  ],
) <part3_conv>

On a log-log scale a convergence rate of $O(N^(-1\/2))$ appears as a straight
line with slope $-1\/2$.  The actual error oscillates around the theoretical
envelope due to random fluctuations but follows the same long-run trend.
Large excursions at small $N$ are expected: with few samples, $hat(p)_N$
deviates substantially from its mean, causing large swings in $hat(pi)_N$.

#pagebreak()

= Part 4: Bootstrap Properties — Formal Verification with Lean 4

== Bootstrap Method: Background

The *bootstrap*, introduced by Efron (1979), is a resampling technique for
estimating the sampling distribution of any statistic without requiring
parametric assumptions.  Given an observed sample
$bold(X) = (X_1, dots.c, X_n)$ drawn from an unknown distribution $F$, the
*empirical distribution* $hat(F)_n$ places probability mass $1\/n$ on each
observed value.

A *bootstrap sample* $bold(X)^* = (X_1^*, dots.c, X_n^*)$ is drawn with
replacement from $hat(F)_n$.  Repeating this $B$ times approximates the
sampling distribution of any statistic $T(bold(X))$ without relying on
asymptotic theory.

The key algebraic properties we verify are:

1. *Unbiasedness of the bootstrap mean*:
  $ E^* [overline(X)^*] = overline(X) $
  Drawing $n$ values with equal probability $1\/n$ and averaging recovers
  the empirical mean by definition.

2. *Raw-score form of the empirical variance*:
  $ hat(sigma)^2 = 1/n sum_(i=1)^n X_i^2 - overline(X)^2 $
  This is the plug-in analogue of $"Var"(X) = E[X^2] - (E[X])^2$.

3. *Bootstrap variance of the mean*:
  $ "Var"^* (overline(X)^*) = hat(sigma)^2 / n $
  This mirrors the classical result $"Var"(overline(X)) = sigma^2 \/ n$,
  with the unknown $sigma^2$ replaced by the plug-in estimate $hat(sigma)^2$.
  It provides a closed-form bootstrap standard error for the mean.

== Formal Verification in Lean 4

We encoded and verified all three properties using *Lean 4* and the *Mathlib 4*
formal mathematics library.  In a proof assistant, every logical step is
checked by a type-checking kernel from first principles.  The absence of any
`sorry` (Lean's placeholder for an unproved step) guarantees machine-certified
completeness.

=== Verified Theorems

1. *`bootstrap_mean_unbiased`* — proved by `rfl` (definitional equality).
   Both sides reduce to the same expression under the definitions, requiring
   no additional reasoning.

2. *`empiricalVariance_eq`* — algebraically unfolds the variance definition
   to derive the raw-score form $(1\/n) sum X_i^2 - overline(X)^2$.

3. *`bootstrap_variance_of_mean`* — the most substantial result, relating the
   bootstrap variance of the mean to the plug-in variance.  Proved entirely
   by real-number algebra with no `sorry`.

=== Verification Status

```bash
cd lean4/BootstrapProperties
lake build
```

A successful build with no errors — and no `sorry` in the source — confirms
that all three theorems are fully certified by Lean's type-checker.

```lean
#check @bootstrap_variance_of_mean
```

This line in `Theorems.lean` causes Lean to print the full type of the theorem
if and only if it is accepted, providing an explicit machine-readable
certificate.
