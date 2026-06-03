// ============================================================
//  Computational Statistics — Assignment 03
//  Instituto Nacional de Pesquisas Espaciais (INPE)
//  Author: Rian Koja
// ============================================================

#set page(
  paper: "a4",
  margin: (top: 2.5cm, bottom: 2.5cm, left: 2.5cm, right: 2.5cm),
  numbering: "1",
  number-align: center,
)
#set text(font: "Linux Libertine", size: 11pt, lang: "en")
#set heading(numbering: "1.a.")
#set par(justify: true, leading: 0.65em)

// --- FRONT MATTER ---
#align(center)[
  #v(1em)
  #text(size: 13pt)[Instituto Nacional de Pesquisas Espaciais (INPE)] \
  #text(size: 12pt)[Graduate Program in Applied Computing (CAP)] \
  #v(1.5em)
  #text(size: 22pt, weight: "bold")[Computational Statistics] \
  #v(0.4em)
  #text(size: 16pt)[Assignment 03 — Sampling, CLT and Model Selection] \
  #v(1.2em)
  #text(size: 13pt)[*Author:* Rian Koja] \
  #v(0.4em)
  #text(size: 12pt)[March 2026] \
  #v(2em)
]

#outline(indent: 2em, depth: 3)

#pagebreak()

// ============================================================
= Problem 1: Sampling Distribution and Bootstrap
// ============================================================

== Theory of Sampling Distribution

The *sampling distribution of the sample mean* $overline(X)$ describes how the average of $n$ independent and identically distributed (i.i.d.) draws from a population varies from sample to sample.  Given a population with mean $mu$ and variance $sigma^2$, two key properties hold for any $n$:

$ bb(E)[overline(X)] = mu, quad quad "Var"(overline(X)) = sigma^2 / n $

The *standard error* $"SE" = sigma / sqrt(n)$ measures how tightly the sample means cluster around $mu$ and decreases as $sqrt(n)$ grows.

=== Discrete Case

Let $X$ be a discrete random variable with PMF $p(x_i)$.  The sample mean $overline(X) = 1/n sum_(i=1)^n X_i$ is itself discrete, taking values on a finite or countable set.  Its distribution is obtained by convolving the PMF of $X$ with itself $n$ times and scaling by $1/n$:

$ P(overline(X) = z) = sum_((x_1, dots, x_n) in S_n(z)) product_(i=1)^n p(x_i), $

where $S_n(z)$ is the set of all $n$-tuples whose average equals $z$.  For $X tilde "Bernoulli"(p)$, the sum $sum X_i tilde "Binomial"(n,p)$, so

$ P(overline(X) = k/n) = binom(n, k) p^k (1-p)^(n-k), quad k = 0, 1, dots, n. $

As $n arrow.r infinity$, the CLT ensures that $sqrt(n)(overline(X) - p)$ converges to $cal(N)(0, p(1-p))$.

=== Continuous Case

For a continuous random variable with PDF $f_X$, the PDF of $overline(X)$ is obtained via $n$-fold convolution followed by scaling:

$ f_(overline(X))(t) = n dot (f_X^(*n))(n t). $

For example, if $X tilde "Exponential"(lambda)$, the sum $sum X_i tilde "Gamma"(n, lambda)$, so $overline(X) tilde "Gamma"(n, n lambda)$—a distribution that becomes increasingly symmetric and bell-shaped as $n$ grows.

=== Central Limit Theorem

If the population has mean $mu$ and *finite* variance $sigma^2$, then for any fixed $t$:

$ lim_(n arrow.r infinity) P( (overline(X) - mu) / (sigma/sqrt(n)) <= t ) = Phi(t), $

where $Phi$ is the standard Normal CDF.  Equivalently, for large $n$:

$ overline(X) #h(0.3em) approx^d #h(0.3em) cal(N)(mu, sigma^2/n). $

This result holds regardless of the original distribution shape, provided $sigma^2 < infinity$.

== Computational Example: Bernoulli vs Exponential

We simulated two populations of $1,000,000$ items:

- *Discrete:* $X tilde "Bernoulli"(p=0.3)$ — true $mu = 0.3$, $sigma = sqrt(0.21) approx 0.458$.
- *Continuous:* $X tilde "Exponential"(lambda=1)$ — true $mu = 1$, $sigma = 1$.

For each population, we compared estimating the true mean and true standard deviation under two different regimens that use the exact same quantity of data ($500$ observations drawn from the population). To see what happens to the standard deviation of the estimators themselves, we repeated each regimen 1,000 times:

1. *Batch/Segmented Procedure ($20 times 25$):* We draw 500 items from the actual population and segment them into 20 independent batches of $n=25$. For the mean, we take the mean of the 20 batch means. For the standard deviation, we calculate the variance of each of the 20 batches, average those 20 variances, and take the square root.
2. *Large Sample Procedure ($1 times 500$):* We draw 500 items straight from the population simultaneously and compute the mean and standard deviation of the single large pool.

By repeating the entire macro-experiment 1,000 times, we can see exactly what happens to the precision of the variance tracking. Note that for the sampling mean, averaging the means of 20 equally-sized batches is mathematically identical to calculating the mean of the pooled $500$ samples.

#figure(
  image("figures/problem1_sampling.svg", width: 95%),
  caption: [
    Histograms of 1,000 Mean estimates. Left: True Population distributions. Middle: 
    Overlay of the means of the $20 times 25$ strategy versus the $1 times 500$ pooled large 
    sample strategy. As expected, their distributions over 1,000 trials are perfectly identical.
  ],
) <sampling_dist>

#figure(
  image("figures/problem1_std_comparison.svg", width: 75%),
  caption: [
    Histograms of 1,000 Standard Deviation estimates. Both the "average of 20 subset variances"
    (red) and the "pooled variance of 500" (green) closely track the true population standard deviation.
  ],
) <std_comp>

*Observations.* The goal was to test whether getting the variance of 25 samples 20 times and averaging the variances works better or worse than taking the variance of 500 samples at once. 
First, @sampling_dist clearly shows that for the sample mean, segmenting the data mathematically makes absolutely no difference: $overline(x)_(20 times 25) equiv overline(x)_(500)$. 
However, @std_comp illustrates *what happens to the variance estimation*. The variance of a sample variance estimator generally scales as $2sigma^4 slash (n-1)$. Averaging 20 independent unbiased variance estimators of size 25 produces an unbiased estimator whose total variance is proportional to $1/20 dot 2/(25-1) = 2/480 = 1/240$. By contrast, pooling all 500 items to calculate a single variance produces an estimator with variance proportional to $2/(500-1) \approx 1/249.5$. 
Therefore, mathematically and visually, the estimators have nearly identical spreads ($1/240$ vs $1/249.5$). Getting the variance of 25 samples 20 times is *only very slightly worse* than taking the variance of 500 items directly, since sequential small batches ($24 times 20 = 480$ intrinsic degrees of freedom) are marginally less efficient than a single pooled batch ($499$ degrees of freedom).

== Bootstrap Inference from a Single Sample

If neither the true variance nor the true mean (nor the underlying distribution format) were known a priori, we would rely on the traditional Bootstrap resampling method to estimate our own error. To demonstrate this, we drew *exactly one* real sample of size $n=50$, and resampled it uniformly with replacement 1,000 times to infer the precision of the mean and standard deviation.

#figure(
  image("figures/problem1_bootstrap_inference.svg", width: 95%),
  caption: [
    Histograms generated via 1,000 bootstrap resamples of a *single* $n=50$ dataset. The distribution widths (Bootstrap SE) perfectly approximate the true variation (True SE) of our mean and standard deviation estimators.
  ],
) <boot_inference>

As shown in @boot_inference, even though we only possess 50 isolated data points, analyzing the variance across 1,000 bootstrap resamples bounds the True Standard Error without requiring a known underlying distribution format. The Bootstrap Standard Errors approximate the overall True SE—confirming that computation can substitute for unavailable true population structures when trying to estimate our confidence in finite descriptive statistics.

// ============================================================
= Problem 2: Central Limit Theorem and Confidence Intervals
// ============================================================

*Motivation problem.* A sample of $n=25$ adult males shows cholesterol level mean $overline(x)=186$ and standard deviation $s=12$.  The population is assumed to follow a Normal distribution.  Obtain the 95% confidence interval for the mean.

== CLT and the Distribution of the Sample Statistics

=== The Chi-Squared Distribution

Let $Z_1, Z_2, dots, Z_k$ be independent standard normal random variables, $Z_i tilde.op cal(N)(0,1)$.  By definition the random variable

$ Q = sum_(i=1)^k Z_i^2 $

follows the *chi-squared distribution with $k$ degrees of freedom*, $Q tilde.op chi^2(k)$.  We derive its PDF via the moment generating function (MGF).

*Step 1: MGF of $Z^2$.*  For $Z tilde.op cal(N)(0,1)$ and $t < 1/2$,

$
  M_(Z^2)(t) = bb(E)[e^(t Z^2)] = frac(1, sqrt(2pi)) integral_(-infinity)^(infinity) e^(t z^2) e^(-z^2 slash 2) d z = frac(1, sqrt(2pi)) integral_(-infinity)^(infinity) exp lr((-frac(z^2(1-2t), 2))) d z.
$

The integrand is proportional to a Gaussian with variance $(1-2t)^(-1)$, so the integral evaluates to $sqrt(2pi \/ (1-2t))$, giving

$ M_(Z^2)(t) = (1-2t)^(-1/2). $

*Step 2: MGF of $Q$.*  Because the $Z_i$ are independent,

$ M_Q(t) = product_(i=1)^k M_(Z_i^2)(t) = (1-2t)^(-k/2), quad t < 1/2. $

*Step 3: Identification.*  A Gamma distribution with shape $alpha$ and rate $beta$ has MGF $(1 - t/beta)^(-alpha)$.  Setting $alpha = k/2$ and $beta = 1/2$ yields $(1-2t)^(-k/2)$, which matches $M_Q$ exactly.  Since the MGF uniquely determines the distribution (on an open neighbourhood of $t=0$), $Q$ follows a $"Gamma"(k/2, 1/2)$ distribution with PDF

$
  f(q; k) = frac((1/2)^(k/2), Gamma(k/2)) q^(k/2-1) e^(-q/2) = frac(q^(k/2-1) e^(-q/2), 2^(k/2) Gamma(k/2)), quad q > 0.
$

A further corollary of the MGF is the *additive property*: independent $chi^2(k_1)$ and $chi^2(k_2)$ variables sum to a $chi^2(k_1+k_2)$ variable, since their MGFs multiply as $(1-2t)^(-(k_1+k_2)/2)$.  The distribution has mean $k$ and variance $2k$; it is right-skewed for small $k$ and approaches normality as $k arrow.r infinity$.

=== The Student's $t$-Distribution

Let $Z tilde.op cal(N)(0,1)$ and $V tilde.op chi^2(nu)$ be independent.  The ratio

$ T = frac(Z, sqrt(V slash nu)) $

follows the *Student's $t$-distribution with $nu$ degrees of freedom*, $T tilde.op t(nu)$.  We derive its PDF by conditioning on $V$ and marginalising.

*Conditional distribution.*  Given $V = v$, we have $T | V = v ~ cal(N)(0, nu/v)$, so

$ f_(T|V)(t | v) = sqrt(frac(v, 2pi nu)) exp lr((-frac(t^2 v, 2nu))). $

*Marginal PDF.*  Multiplying by the $chi^2(nu)$ density $f_V(v) = v^(nu/2-1) e^(-v/2) \/ (2^(nu/2) Gamma(nu/2))$ and integrating,

$
  f_T(t) &= integral_0^infinity f_(T|V)(t|v) f_V(v) d v \
  &= frac(1, sqrt(2pi nu) dot 2^(nu/2) Gamma(nu/2)) integral_0^infinity v^((nu+1)/2 - 1) exp lr((-frac(v, 2) lr((1 + frac(t^2, nu))))) d v.
$

*Evaluating the integral.*  Substitute $u = frac(v, 2)(1 + t^2 \/ nu)$, i.e. $v = 2u \/ (1 + t^2 \/ nu)$, $d v = 2 \/ (1 + t^2 \/ nu) d u$:

$
  integral_0^infinity v^((nu+1)/2-1) e^(-frac(v, 2)(1+t^2/nu)) d v = frac(2^((nu+1)/2), (1+t^2/nu)^((nu+1)/2)) integral_0^infinity u^((nu+1)/2-1) e^(-u) d u = frac(2^((nu+1)/2) Gamma((nu+1)/2), (1+t^2/nu)^((nu+1)/2)).
$

*Assembling the result.*  Substituting back, the factors $sqrt(2pi nu) dot 2^(nu/2) = sqrt(2) dot sqrt(pi nu) dot 2^(nu/2) = 2^((nu+1)/2) sqrt(pi nu)$ cancel the power of 2 in the numerator:

$ f_T(t) = frac(Gamma((nu+1)/2), sqrt(nu pi) Gamma(nu/2)) lr((1 + frac(t^2, nu)))^(-(nu+1)/2), quad t in bb(R). $

The distribution is symmetric about zero, heavier-tailed than the normal (the tails decay as $|t|^(-(nu+1))$ rather than exponentially), and $t(nu) arrow.r cal(N)(0,1)$ as $nu arrow.r infinity$.

=== Exact Sampling Distributions Under Normality

Assume $X_1, dots, X_n tilde.op^("i.i.d.") cal(N)(mu, sigma^2)$.  Define the sample mean and unbiased sample variance in the usual way:

$ overline(X) = frac(1, n) sum_(i=1)^n X_i, quad S^2 = frac(1, n-1) sum_(i=1)^n (X_i - overline(X))^2. $

*Distribution of $(n-1)S^2/sigma^2$.*  Each standardised deviation $(X_i - mu)/sigma$ is $cal(N)(0,1)$, so $sum_i (X_i - mu)^2 / sigma^2 tilde.op chi^2(n)$.  The algebraic identity

$ sum_(i=1)^n frac((X_i - mu)^2, sigma^2) = frac((n-1)S^2, sigma^2) + frac((overline(X) - mu)^2, sigma^2/n) $

decomposes this $chi^2(n)$ quantity into two independent terms (independence follows from the fact that $overline(X)$ and $S^2$ are independent for normal populations — a consequence of the normal distribution being the unique distribution for which the sample mean and sample variance are independent).  The second term is $chi^2(1)$, so by the additive property of the chi-squared distribution:

$ frac((n-1)S^2, sigma^2) tilde.op chi^2(n-1). $

*Distribution of the $t$-statistic.*  Because $overline(X) tilde.op cal(N)(mu, sigma^2/n)$, the standardised mean $Z = (overline(X) - mu)/(sigma/sqrt(n))$ is $cal(N)(0,1)$.  Writing $S$ in place of the unknown $sigma$ introduces $(n-1)S^2/sigma^2 tilde.op chi^2(n-1)$ into the denominator.  Specifically,

$ T = frac(overline(X) - mu, S/sqrt(n)) = frac(Z, sqrt([(n-1)S^2/sigma^2] \/ (n-1))). $

Since $Z$ and $(n-1)S^2/sigma^2$ are independent (by the result above), this ratio matches exactly the definition of a $t$-distributed variable with $nu = n-1$:

$ T = frac(overline(X) - mu, S / sqrt(n)) tilde.op t(n-1). $

This is an *exact* result for every $n >= 2$ when the population is normal.  For non-normal populations the CLT guarantees that $T$ is *approximately* $cal(N)(0,1)$ for large $n$, but the exact $t(n-1)$ result no longer holds in finite samples.  @clt_conv illustrates how quickly the sampling distribution of $overline(X)$ approaches normality as $n$ grows.

#figure(
  image("figures/problem2_clt.svg", width: 95%),
  caption: [
    CLT convergence for a Normal population.  Even though the population is already normal,
    the figure shows how the theoretical Normal approximation tightens as $n$ increases,
    and validates the simulation approach used throughout.
  ],
) <clt_conv>

== Confidence Interval for the Mean

Because $sigma$ is unknown we use the $t$-distribution with $"df" = n-1 = 24$ degrees of freedom:

$ "CI"_mu = overline(x) plus.minus t_(alpha/2, n-1) dot frac(s, sqrt(n)) $

For $alpha=0.05$: $t_(0.025, 24) approx 2.064$, $s/sqrt(n) = 12/5 = 2.4$.

$ "CI"_mu = 186 plus.minus 2.064 times 2.4 = [181.05, 190.95] $

== Confidence Interval for the Standard Deviation

The 95% CI for $sigma^2$ uses the $chi^2$ distribution:

$ "CI"_(sigma^2) = [ frac((n-1)s^2, chi^2_(1-alpha/2, n-1)), frac((n-1)s^2, chi^2_(alpha/2, n-1)) ] $

For $alpha=0.05$: $chi^2_(0.025,24) approx 12.40$ and $chi^2_(0.975,24) approx 39.36$.

$ "CI"_(sigma^2) = [ frac(24 times 144, 39.36), frac(24 times 144, 12.40) ] = [87.75, 278.71] $

$ "CI"_sigma = [sqrt(87.75), sqrt(278.71)] = [9.37, 16.69] $

#figure(
  image("figures/problem2_ci.svg", width: 95%),
  caption: [
    Left: $t(24)$ distribution with rejection regions at $alpha/2 = 0.025$ shaded in red.
    Right: 95% CIs from 100 independent simulated samples of size $n=25$.  Blue intervals
    contain the true mean; red intervals miss it.  The empirical coverage rate is close to
    the theoretical 95%.
  ],
) <ci_vis>

@ci_vis (right panel) confirms the coverage property: approximately 5% of simulated intervals do not contain the true mean, consistent with $alpha = 0.05$.

// ============================================================
= Problem 3: Model Confidence Set (MCS)
// ============================================================

== Theoretical Background

=== Setup and Notation

Let $cal(M)_0 = {1, dots, m_0}$ be a finite set of candidate models evaluated over $n$ periods.  Each model $i$ incurs a scalar loss $L_(i,t)$ at period $t$.  The *loss differential* is

$ d_(i j, t) = L_(i,t) - L_(j,t), $

and $mu_(i j) equiv bb(E)[d_(i j, t)]$ is assumed finite and time-invariant.  Model $i$ is preferred over $j$ when $mu_(i j) < 0$.

> *Definition 1 (Superior set).*  $cal(M)^* equiv {i in cal(M)_0 : mu_(i j) <= 0 "for all" j in cal(M)_0}$.

The MCS procedure aims to identify $cal(M)^*$ by testing, at each step, the null of *equal predictive ability* (EPA) over the current active set $cal(M)$:

$ H_(0, cal(M)) : mu_(i j) = 0 quad forall i, j in cal(M). $

=== The MCS Algorithm

The procedure requires an equivalence test $delta_cal(M)$ and an elimination rule $e_cal(M)$ @hansen2011:

+ Set $cal(M) = cal(M)_0$.
+ Test $H_(0, cal(M))$ using $delta_cal(M)$ at level $alpha$.
+ If accepted, set $hat(cal(M))^*_(1-alpha) = cal(M)$ and stop.
+ Otherwise apply $e_cal(M)$ to remove one object and return to step 2.

=== Test Statistics

Two statistics can serve as $delta_cal(M)$ @hansen2011.  Writing $overline(d)_(i dot) = m^(-1) sum_(j in cal(M)) overline(d)_(i j)$ for the average relative loss of model $i$, the *t-statistics*

$ t_(i dot) = overline(d)_(i dot) \/ sqrt(hat("var")(overline(d)_(i dot))) $

lead to two tests:

- *$T_"max"$ (semi-quadratic):* $T_"max" = max_(i in cal(M)) t_(i dot)$, with elimination rule $e_"max" = arg max_i t_(i dot)$.
- *$T_R$ (range):* $T_R = max_(i,j in cal(M)) |t_(i j)|$, with $e_R = arg max_i sup_j t_(i j)$.

Critical values are obtained via the *stationary bootstrap*, which resamples blocks of consecutive observations to preserve temporal dependence @politis1994.

=== Key Theorems

The following results hold under Assumption 1 of @hansen2011 (asymptotic level control, consistency, and coherency between test and elimination rule).

*Theorem 1 (MCS coverage and elimination consistency)* @hansen2011.

(i) $liminf_(n -> infinity) P(cal(M)^* subset.eq hat(cal(M))^*_(1-alpha)) >= 1 - alpha$.

(ii) $lim_(n -> infinity) P(i in hat(cal(M))^*_(1-alpha)) = 0$ for every $i in.not cal(M)^*$.

Part (i) is the analogue of a confidence interval covering the true parameter: the MCS contains every best model with probability at least $1 - alpha$.  Part (ii) says inferior models are asymptotically excluded with probability one.

*Corollary 1 (Singleton)* @hansen2011.  When $cal(M)^* = {i^*}$ is a singleton,

$ lim_(n -> infinity) P(cal(M)^* = hat(cal(M))^*_(1-alpha)) = 1. $

That is, with sufficient data, the MCS collapses exactly to the single best model.

*Theorem 2 (Finite-sample coherency)* @hansen2011.  If $P(delta_cal(M) = 1, e_cal(M) in cal(M)^*) <= alpha$, then $P(cal(M)^* subset.eq hat(cal(M))^*_(1-alpha)) >= 1 - alpha$ holds *exactly*, not just asymptotically.  The tests $T_"max"$ and $T_R$ paired with their natural elimination rules satisfy this coherency condition (Proposition 1 of @hansen2011).

*Theorem 3 (MCS p-values)* @hansen2011.  Let $hat(p)_(e_(cal(M)_j))$ denote the MCS p-value of the $j$-th eliminated model, defined as the running maximum of the sequence of per-step p-values:

$ hat(p)_(e_(cal(M)_j)) = max_(k <= j) P_(H_(0, cal(M)_k)). $

Then $i in hat(cal(M))^*_(1-alpha)$ if and only if $hat(p)_i >= alpha$.  The running-maximum construction ensures monotonicity: a model cannot have a smaller p-value than the one eliminated just before it, preventing the sequential procedure from accumulating spurious rejections.

=== Interpreting MCS Results

The MCS p-value $hat(p)_i$ reported for each model satisfies (by Theorem 3):

- $hat(p)_i >= alpha$: model $i$ *belongs to* the MCS at level $alpha$, i.e. it cannot be statistically distinguished from the best model(s).
- $hat(p)_i < alpha$: model $i$ is *excluded*, i.e. its inferiority is statistically significant at level $alpha$.
- $hat(p)_i = 1$: the model was *never eliminated*; the EPA test was accepted while it was still in the active set.
- The conventional choice is $alpha = 10%$: all models with $hat(p)_i >= 0.10$ form the MCS.

The MCS p-value is *not* the probability that a model is optimal — just as a classical p-value is not the probability that $H_0$ is true.  It reflects the random nature of $hat(cal(M))^*$: the set contains $cal(M)^*$ with probability $>= 1 - alpha$, not with certainty.  Less informative data leads to a wider MCS (many models survive); more informative data compresses it toward the single best model (Corollary 1).

== Where MCS Shines: Identifying a Clear Winner

We generated synthetic data from a quadratic relationship $y = x^2 + epsilon$ ($epsilon tilde cal(N)(0, 1.5^2)$, $x in [-4, 4]$) with $n_"train" = n_"test" = 200$.  Four polynomial models were trained on the training set and evaluated on the held-out test set using squared errors per observation:

#figure(
  image("figures/problem3_mcs_shines.svg", width: 92%),
  caption: [
    MCS applied to a quadratic ground truth.  Left: fitted curves on test data (solid lines
    indicate models in the MCS at $alpha=10%$; dashed lines indicate excluded models).
    Right: test RMSE and MCS p-values (green = included; red = excluded).
  ],
) <mcs_shines>

@mcs_shines confirms that when there is a structurally best model, MCS correctly identifies it:

- *Quadratic* (the true model) achieves the lowest RMSE and is included in the MCS ($hat(p) >= 0.10$).
- *Cubic* may also be included: the extra degree of freedom does not significantly worsen prediction on 200 test points, so the EPA test cannot reject equality with the quadratic.
- *Linear* is correctly excluded ($hat(p) < 0.10$): its systematic bias (underfitting) is large enough for the EPA test to detect.
- *Degree 8* is excluded: overfitting inflates its test-set variance, making it statistically inferior to the quadratic.

This is Corollary 1 in action: when the true model is structurally distinct, and we have enough data, the MCS converges to that single best model.

== Multi-Model Comparison: Hypothesis Testing with MCS

We evaluate four candidate estimators — Least Squares (LS), RANSAC, LightGBM (LGBM), and RANSAC+LightGBM (R+LGBM) — on nine synthetic datasets: three functional forms ($y=x$, $y=x^2$, $y=e^x$) each at three outlier contamination levels (0%, $approx$20%, $approx$50%).  For each dataset, the MCS is computed from squared-error losses at $alpha=10%$.  Each figure below shows, per outlier level: *(left)* the data with all four fitted curves (solid = included in MCS, dashed = excluded), and *(right)* the corresponding MCS p-value bar chart with the $alpha=0.10$ threshold line.

*Reading the tables.*  Within each row, values are colour-coded relative to each other (green = best, red = worst).  For MCS p-values the direction is reversed: green means $hat(p) >= 0.10$ (included), red means $hat(p) < 0.10$ (excluded).

=== Linear Relationship

#figure(
  image("figures/problem3_comparison_linear.svg", width: 100%),
  caption: [
    MCS comparison for linear data ($y = x$).  Each row is one outlier level.
    Left: data with fitted curves (solid = in MCS, dashed = excluded).
    Right: MCS p-values; dashed line marks $alpha = 0.10$.
  ],
) <mcs_linear_fig>

#include "generated/mcs_table_linear.typ"

On clean linear data, LS and RANSAC are statistically equivalent (both $hat(p) = 1$) and dominate.  As outliers increase, LightGBM gains an apparent advantage: its flexibility lets it partially fit the contaminated observations, lowering its MSE while LS and RANSAC are penalised.  At 50% contamination, LS is typically excluded ($hat(p) < 0.10$) while LGBM retains its p-value.

=== Quadratic Relationship

#figure(
  image("figures/problem3_comparison_quadratic.svg", width: 100%),
  caption: [
    MCS comparison for quadratic data ($y = x^2$).  Layout as in @mcs_linear_fig.
  ],
) <mcs_quadratic_fig>

#include "generated/mcs_table_quadratic.typ"

On clean quadratic data, LS (quadratic) and RANSAC are both in the MCS; R+LGBM may also enter because LightGBM can capture the curvature.  Outliers progressively shift the MCS toward LightGBM-based methods, consistent with the pattern observed for linear data.

=== Exponential Relationship

#figure(
  image("figures/problem3_comparison_exponential.svg", width: 100%),
  caption: [
    MCS comparison for exponential data ($y = e^x$).  Layout as in @mcs_linear_fig.
  ],
) <mcs_exponential_fig>

#include "generated/mcs_table_exponential.typ"

On clean exponential data, R+LGBM typically dominates because LGBM captures the non-linear shape while RANSAC discards any anomalous points.  LS (log-space linear model) and RANSAC on the log-transformed data are competitive but show higher RMSE when the exponential curvature is steep.

*Cross-cutting inference remark.*  In all three settings, the p-value bars make the hypothesis testing explicit: a bar above the $alpha = 0.10$ line means the EPA null $H_(0, cal(M))$ was *not* rejected while that model was still active — by Theorem 3, the model belongs to the 90% MCS.  A bar below the line means the model was eliminated when the EPA test rejected equality, and the running-maximum construction ensures monotonic p-values (Theorem 3).

== Where MCS Fails: Outlier Contamination

The comparison table already hints at a failure mode: on linearly-generated data with many outliers, LightGBM "wins" according to MSE even though the true relationship is $y = x$, which a simple linear model handles perfectly.  To isolate this failure, @mcs_fails reproduces a controlled version with three models (Linear LS, Quadratic LS, Degree 6 polynomial) on $n = 120$ points ($n_"in"=100$ inliers on $y=x$, $n_"out"=20$ circular outliers):

#figure(
  image("figures/problem3_mcs_fails.svg", width: 97%),
  caption: [
    MCS failure on linear data with circular outliers.  Left: fitted models with true inlier
    relationship $y = x$ (black dashed).  Middle: RMSE and MCS p-values on the full
    contaminated dataset — flexible models appear optimal.  Right: the same on clean inliers
    only — Linear LS correctly wins.
  ],
) <mcs_fails>

*Why does MCS fail here?*  Three compounding reasons:

+ *Non-robust loss.* MSE assigns equal weight to all residuals.  A circular outlier at distance $r$ from the true line contributes $r^2 approx 9$–$36$ to the loss, dwarfing inlier residuals ($approx 0.25$).  Flexible models partially interpolate the outlier cluster, lowering their apparent MSE.
+ *Bootstrap contamination.* The stationary bootstrap resamples the full dataset; resampled batches contain outliers in proportion to their frequency, biasing the variance estimate $hat("var")(overline(d)_(i j))$ and distorting the EPA test statistics.
+ *Breakdown point of zero.* The standard MCS has no robustness guarantee: Theorem 1 assumes the same stationary distribution holds throughout, but outliers create a mixture that violates this in practice.

When evaluated on clean inliers only (right panel of @mcs_fails), MCS correctly recovers Linear LS as the sole member of the confidence set — confirming that the procedure itself is sound, but the loss function is not.  This motivates the research direction of *outlier-robust* model confidence sets.

// ============================================================
= Conclusion
// ============================================================

This work covered three interconnected topics in computational statistics.

*Problem 1* demonstrated that the sampling distribution of the mean rapidly converges to a Normal distribution (CLT), regardless of whether the underlying variable is discrete (Bernoulli) or continuous (Exponential).  The standard error decreases as $sigma/sqrt(n)$; large-sample estimation is far more precise than bootstrap estimation with small $n$, though bootstrap remains useful when data collection is expensive.

*Problem 2* applied the CLT and exact sampling theory (t and chi-squared distributions) to construct 95% confidence intervals for the mean and standard deviation of cholesterol levels.  The coverage property was confirmed by simulation: approximately 5% of intervals miss the true mean, matching the nominal $alpha = 5%$.

*Problem 3* introduced the Model Confidence Set of Hansen, Lunde and Nason (2011), a principled sequential hypothesis testing procedure governed by three key theorems.  Theorem 1 guarantees that the MCS contains the true best model(s) with probability $>= 1 - alpha$ asymptotically, and eliminates all inferior models with probability tending to one.  Theorem 3 provides p-values that characterise inclusion: model $i$ belongs to the 90% MCS if and only if $hat(p)_i >= 0.10$.  A multi-model comparison across nine datasets (three functional forms × three outlier levels) showed that LightGBM consistently achieves high MCS p-values under contamination, while simpler methods are excluded as outliers increase.  However, when the loss function is non-robust (MSE), the procedure fails on contaminated data: outlier residuals dominate, flexible models appear falsely superior, and the true linear model is excluded.  On clean data, MCS correctly recovers the true model.  The remedy is a robust loss function or an outlier-aware resampling strategy.

// ============================================================
= References
// ============================================================

#bibliography("references.bib", style: "american-psychological-association")
