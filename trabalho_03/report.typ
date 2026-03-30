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

The *sampling distribution of the sample mean* $bar(X)$ describes how the average of $n$ independent and identically distributed (i.i.d.) draws from a population varies from sample to sample.  Given a population with mean $mu$ and variance $sigma^2$, two key properties hold for any $n$:

$ bb(E)[bar(X)] = mu, quad quad "Var"(bar(X)) = sigma^2 / n $

The *standard error* $"SE" = sigma / sqrt(n)$ measures how tightly the sample means cluster around $mu$ and decreases as $sqrt(n)$ grows.

=== Discrete Case

Let $X$ be a discrete random variable with PMF $p(x_i)$.  The sample mean $bar(X) = 1/n sum_(i=1)^n X_i$ is itself discrete, taking values on a finite or countable set.  Its distribution is obtained by convolving the PMF of $X$ with itself $n$ times and scaling by $1/n$:

$ P(bar(X) = z) = sum_((x_1, dots, x_n) in S_n(z)) product_(i=1)^n p(x_i), $

where $S_n(z)$ is the set of all $n$-tuples whose average equals $z$.  For $X tilde "Bernoulli"(p)$, the sum $sum X_i tilde "Binomial"(n,p)$, so

$ P(bar(X) = k/n) = binom(n, k) p^k (1-p)^(n-k), quad k = 0, 1, dots, n. $

As $n arrow.r infinity$, the CLT ensures that $sqrt(n)(bar(X) - p)$ converges to $cal(N)(0, p(1-p))$.

=== Continuous Case

For a continuous random variable with PDF $f_X$, the PDF of $bar(X)$ is obtained via $n$-fold convolution followed by scaling:

$ f_(bar(X))(t) = n dot (f_X^(*n))(n t). $

For example, if $X tilde "Exponential"(lambda)$, the sum $sum X_i tilde "Gamma"(n, lambda)$, so $bar(X) tilde "Gamma"(n, n lambda)$—a distribution that becomes increasingly symmetric and bell-shaped as $n$ grows.

=== Central Limit Theorem

If the population has mean $mu$ and *finite* variance $sigma^2$, then for any fixed $t$:

$ lim_(n arrow.r infinity) P( (bar(X) - mu) / (sigma/sqrt(n)) <= t ) = Phi(t), $

where $Phi$ is the standard Normal CDF.  Equivalently, for large $n$:

$ bar(X) #h(0.3em) approx^d #h(0.3em) cal(N)(mu, sigma^2/n). $

This result holds regardless of the original distribution shape, provided $sigma^2 < infinity$.

== Computational Example: Bernoulli vs Exponential

We simulated two populations of $1,000,000$ items:

- *Discrete:* $X tilde "Bernoulli"(p=0.3)$ — true $mu = 0.3$, $sigma = sqrt(0.21) approx 0.458$.
- *Continuous:* $X tilde "Exponential"(lambda=1)$ — true $mu = 1$, $sigma = 1$.

For each population we estimated the mean two ways, repeated 2,000 times:

1. *Bootstrap (small sample):* draw $n=30$ values with replacement, compute the mean.
2. *Large sample:* draw $n=1000$ values without replacement, compute the mean.

#figure(
  image("figures/problem1_sampling.svg", width: 95%),
  caption: [
    Sampling distributions of the mean for Bernoulli(0.3) and Exponential(1) populations.
    Each row shows the true distribution (left), bootstrap means with $n=30$ (middle), and
    large-sample means with $n=1000$ (right).  The dashed curve is the theoretical Normal
    $cal(N)(mu, sigma^2/n)$.
  ],
) <sampling_dist>

#figure(
  image("figures/problem1_std_comparison.svg", width: 75%),
  caption: [
    Empirical standard deviation of the sample mean (blue bars) vs.\ the
    theoretical $sigma/sqrt(n)$ (orange bars) for bootstrap ($n=30$) and
    large-sample ($n=1000$) approaches.
  ],
) <std_comp>

*Observations.*  @sampling_dist shows that, for both distributions, the histogram of sample means closely follows the theoretical Normal curve.  At $n=30$ the Exponential case retains a slight positive skew, which disappears almost entirely at $n=1000$.  @std_comp confirms that the empirical standard errors match $sigma/sqrt(n)$: the large-sample estimator reduces the standard error by a factor of $sqrt(1000/30) approx 5.77$ relative to the bootstrap estimator, at the cost of requiring more data per estimate.

// ============================================================
= Problem 2: Central Limit Theorem and Confidence Intervals
// ============================================================

*Motivation problem.* A sample of $n=25$ adult males shows cholesterol level mean $bar(x)=186$ and standard deviation $s=12$.  The population is assumed to follow a Normal distribution.  Obtain the 95% confidence interval for the mean.

== CLT and the Distribution of the Sample Statistics

=== The Chi-Squared Distribution

Let $Z_1, Z_2, dots, Z_k$ be independent standard normal random variables, $Z_i tilde.op cal(N)(0,1)$.  By definition the random variable

$ Q = sum_(i=1)^k Z_i^2 $

follows the *chi-squared distribution with $k$ degrees of freedom*, $Q tilde.op chi^2(k)$.  We derive its PDF via the moment generating function (MGF).

*Step 1: MGF of $Z^2$.*  For $Z tilde.op cal(N)(0,1)$ and $t < 1/2$,

$ M_(Z^2)(t) = bb(E)[e^(t Z^2)] = frac(1, sqrt(2pi)) integral_(-infinity)^(infinity) e^(t z^2) e^(-z^2 slash 2) d z = frac(1, sqrt(2pi)) integral_(-infinity)^(infinity) exp lr((-frac(z^2(1-2t), 2))) d z. $

The integrand is proportional to a Gaussian with variance $(1-2t)^(-1)$, so the integral evaluates to $sqrt(2pi \/ (1-2t))$, giving

$ M_(Z^2)(t) = (1-2t)^(-1/2). $

*Step 2: MGF of $Q$.*  Because the $Z_i$ are independent,

$ M_Q(t) = product_(i=1)^k M_(Z_i^2)(t) = (1-2t)^(-k/2), quad t < 1/2. $

*Step 3: Identification.*  A Gamma distribution with shape $alpha$ and rate $beta$ has MGF $(1 - t/beta)^(-alpha)$.  Setting $alpha = k/2$ and $beta = 1/2$ yields $(1-2t)^(-k/2)$, which matches $M_Q$ exactly.  Since the MGF uniquely determines the distribution (on an open neighbourhood of $t=0$), $Q$ follows a $"Gamma"(k/2, 1/2)$ distribution with PDF

$ f(q; k) = frac((1/2)^(k/2), Gamma(k/2)) q^(k/2-1) e^(-q/2) = frac(q^(k/2-1) e^(-q/2), 2^(k/2) Gamma(k/2)), quad q > 0. $

A further corollary of the MGF is the *additive property*: independent $chi^2(k_1)$ and $chi^2(k_2)$ variables sum to a $chi^2(k_1+k_2)$ variable, since their MGFs multiply as $(1-2t)^(-(k_1+k_2)/2)$.  The distribution has mean $k$ and variance $2k$; it is right-skewed for small $k$ and approaches normality as $k arrow.r infinity$.

=== The Student's $t$-Distribution

Let $Z tilde.op cal(N)(0,1)$ and $V tilde.op chi^2(nu)$ be independent.  The ratio

$ T = frac(Z, sqrt(V slash nu)) $

follows the *Student's $t$-distribution with $nu$ degrees of freedom*, $T tilde.op t(nu)$.  We derive its PDF by conditioning on $V$ and marginalising.

*Conditional distribution.*  Given $V = v$, we have $T | V = v ~ cal(N)(0, nu/v)$, so

$ f_(T|V)(t | v) = sqrt(frac(v, 2pi nu)) exp lr((-frac(t^2 v, 2nu))). $

*Marginal PDF.*  Multiplying by the $chi^2(nu)$ density $f_V(v) = v^(nu/2-1) e^(-v/2) \/ (2^(nu/2) Gamma(nu/2))$ and integrating,

$ f_T(t) &= integral_0^infinity f_(T|V)(t|v) f_V(v) d v \
  &= frac(1, sqrt(2pi nu) dot 2^(nu/2) Gamma(nu/2)) integral_0^infinity v^((nu+1)/2 - 1) exp lr((-frac(v, 2) lr((1 + frac(t^2, nu))))) d v. $

*Evaluating the integral.*  Substitute $u = frac(v, 2)(1 + t^2 \/ nu)$, i.e. $v = 2u \/ (1 + t^2 \/ nu)$, $d v = 2 \/ (1 + t^2 \/ nu) d u$:

$ integral_0^infinity v^((nu+1)/2-1) e^(-frac(v,2)(1+t^2/nu)) d v = frac(2^((nu+1)/2), (1+t^2/nu)^((nu+1)/2)) integral_0^infinity u^((nu+1)/2-1) e^(-u) d u = frac(2^((nu+1)/2) Gamma((nu+1)/2), (1+t^2/nu)^((nu+1)/2)). $

*Assembling the result.*  Substituting back, the factors $sqrt(2pi nu) dot 2^(nu/2) = sqrt(2) dot sqrt(pi nu) dot 2^(nu/2) = 2^((nu+1)/2) sqrt(pi nu)$ cancel the power of 2 in the numerator:

$ f_T(t) = frac(Gamma((nu+1)/2), sqrt(nu pi) Gamma(nu/2)) lr((1 + frac(t^2, nu)))^(-(nu+1)/2), quad t in bb(R). $

The distribution is symmetric about zero, heavier-tailed than the normal (the tails decay as $|t|^(-(nu+1))$ rather than exponentially), and $t(nu) arrow.r cal(N)(0,1)$ as $nu arrow.r infinity$.

=== Exact Sampling Distributions Under Normality

Assume $X_1, dots, X_n tilde.op^("i.i.d.") cal(N)(mu, sigma^2)$.  Define the sample mean and unbiased sample variance in the usual way:

$ bar(X) = frac(1,n) sum_(i=1)^n X_i, quad S^2 = frac(1, n-1) sum_(i=1)^n (X_i - bar(X))^2. $

*Distribution of $(n-1)S^2/sigma^2$.*  Each standardised deviation $(X_i - mu)/sigma$ is $cal(N)(0,1)$, so $sum_i (X_i - mu)^2 / sigma^2 tilde.op chi^2(n)$.  The algebraic identity

$ sum_(i=1)^n frac((X_i - mu)^2, sigma^2) = frac((n-1)S^2, sigma^2) + frac((bar(X) - mu)^2, sigma^2/n) $

decomposes this $chi^2(n)$ quantity into two independent terms (independence follows from the fact that $bar(X)$ and $S^2$ are independent for normal populations — a consequence of the normal distribution being the unique distribution for which the sample mean and sample variance are independent).  The second term is $chi^2(1)$, so by the additive property of the chi-squared distribution:

$ frac((n-1)S^2, sigma^2) tilde.op chi^2(n-1). $

*Distribution of the $t$-statistic.*  Because $bar(X) tilde.op cal(N)(mu, sigma^2/n)$, the standardised mean $Z = (bar(X) - mu)/(sigma/sqrt(n))$ is $cal(N)(0,1)$.  Writing $S$ in place of the unknown $sigma$ introduces $(n-1)S^2/sigma^2 tilde.op chi^2(n-1)$ into the denominator.  Specifically,

$ T = frac(bar(X) - mu, S/sqrt(n)) = frac(Z, sqrt([(n-1)S^2/sigma^2] \/ (n-1))). $

Since $Z$ and $(n-1)S^2/sigma^2$ are independent (by the result above), this ratio matches exactly the definition of a $t$-distributed variable with $nu = n-1$:

$ T = frac(bar(X) - mu, S / sqrt(n)) tilde.op t(n-1). $

This is an *exact* result for every $n >= 2$ when the population is normal.  For non-normal populations the CLT guarantees that $T$ is *approximately* $cal(N)(0,1)$ for large $n$, but the exact $t(n-1)$ result no longer holds in finite samples.  @clt_conv illustrates how quickly the sampling distribution of $bar(X)$ approaches normality as $n$ grows.

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

$ "CI"_mu = bar(x) plus.minus t_(alpha/2,, n-1) dot frac(s, sqrt(n)) $

For $alpha=0.05$: $t_(0.025, 24) approx 2.064$, $s/sqrt(n) = 12/5 = 2.4$.

$ "CI"_mu = 186 plus.minus 2.064 times 2.4 = [181.05,, 190.95] $

== Confidence Interval for the Standard Deviation

The 95% CI for $sigma^2$ uses the $chi^2$ distribution:

$ "CI"_(sigma^2) = [ frac((n-1)s^2, chi^2_(1-alpha/2,, n-1)),, frac((n-1)s^2, chi^2_(alpha/2,, n-1)) ] $

For $alpha=0.05$: $chi^2_(0.025,24) approx 12.40$ and $chi^2_(0.975,24) approx 39.36$.

$ "CI"_(sigma^2) = [ frac(24 times 144, 39.36),, frac(24 times 144, 12.40) ] = [87.75,, 278.71] $

$ "CI"_sigma = [sqrt(87.75),, sqrt(278.71)] = [9.37,, 16.69] $

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

Let $cal(M)_0 = {1, dots, m_0}$ be a set of candidate models evaluated on observations $t = 1, dots, T$.  Each model $i$ incurs a scalar loss $L_(i,t)$ (e.g.\ squared error) at time $t$.  The *loss differential* between models $i$ and $j$ is

$ d_(i j, t) = L_(i,t) - L_(j,t). $

We say model $i$ is *superior to* model $j$ if $bb(E)[d_(i j, t)] < 0$, i.e.\ it has strictly lower expected loss.

=== Equal Predictive Ability (EPA) Hypothesis

The null hypothesis of *Equal Predictive Ability* over a set $cal(M)$ is

$ H_(0, cal(M)) : bb(E)[d_(i j, t)] = 0 quad forall i, j in cal(M). $

Hansen, Lunde & Nason (2011) use a sequence of EPA tests to build the MCS: at each step the set $cal(M)$ is tested; if $H_0$ is rejected, the model with the worst relative performance is removed.  Removal continues until the remaining models cannot be statistically distinguished.

=== Test Statistics

Two test statistics are proposed @hansen2011:

- *Range statistic* $T_R$: based on the maximum standardised average loss differential across all pairs,
  $ T_R = max_(i,j in cal(M)) frac(bar(d)_(i j), sqrt(hat("Var")(bar(d)_(i j)))). $

- *Semi-quadratic statistic* $T_(S Q)$: sum of standardised squared mean differentials per model,
  $ T_(S Q) = sum_(i in cal(M)) frac(bar(d)_(i dot)^2, hat("Var")(bar(d)_(i dot))), $
  where $bar(d)_(i dot) = (m)^(-1) sum_(j in cal(M)) bar(d)_(i j)$ is the average loss differential of model $i$ against all others.

P-values are obtained via the *stationary bootstrap* @politis1994, which resamples blocks of consecutive observations to respect temporal dependence.

=== Model Elimination Rule

Given a significance level $alpha$, the model eliminated at each step is

$ e^* (cal(M)) = arg max_(i in cal(M)) bar(d)_(i dot) / sqrt(hat("Var")(bar(d)_(i dot))). $

The procedure terminates when $H_(0, cal(M))$ cannot be rejected, yielding the *Model Confidence Set* $hat(cal(M))^*_alpha$.

=== Key Theorems

*Theorem 1 (Consistency)* @hansen2011.  Under standard regularity conditions (stationarity, weak dependence, finite fourth moments):

$ lim_(T arrow.r infinity) P(cal(M)^* subset.eq hat(cal(M))^*_alpha) >= 1 - alpha, $

where $cal(M)^* = {i in cal(M)_0 : bb(E)[d_(i j, t)] <= 0 quad forall j in cal(M)_0}$ is the true superior set.  That is, the MCS contains the best model(s) with probability at least $1-alpha$ in large samples.

*Theorem 2 (Elimination consistency)* @hansen2011.  Models that are strictly inferior (positive expected loss differential against $cal(M)^*$) are excluded from $hat(cal(M))^*_alpha$ with probability approaching one as $T arrow.r infinity$.

=== Interpreting MCS Results

The MCS p-value $p_i$ reported for each model has the following interpretation:

- $p_i >= alpha$: model $i$ *belongs to* the MCS at level $alpha$; it cannot be statistically distinguished from the best.
- $p_i < alpha$: model $i$ is *excluded* from the MCS; its inferiority relative to the best model is statistically significant.
- A p-value of exactly 1 means the model was *never eliminated* during the sequential procedure.
- The conventional choice is $alpha = 10%$: all models with $p_i >= 0.10$ form the MCS.

The MCS does *not* guarantee that the included model is the global optimum—it only guarantees that no sufficient statistical evidence exists to call it inferior.

== Where MCS Shines: Identifying a Clear Winner

We generated synthetic data from a quadratic relationship $y = x^2 + epsilon$ ($epsilon tilde cal(N)(0, 1.5^2)$, $x in [-4, 4]$) with $n_"train" = n_"test" = 200$.  Four models were trained on the training set and evaluated on the held-out test set using squared errors per observation:

#figure(
  image("figures/problem3_mcs_shines.svg", width: 92%),
  caption: [
    MCS applied to a quadratic ground truth.  Left: fitted curves on test data (solid lines
    indicate models in the MCS at $alpha=10%$; dashed lines indicate excluded models).
    Right: test RMSE and MCS p-values (green = included; red = excluded).
  ],
) <mcs_shines>

@mcs_shines confirms that when there is a structurally best model, MCS correctly identifies it:

- *Quadratic* (the true model) achieves the lowest RMSE and is included in the MCS.
- *Cubic* is sometimes also included because the extra degree of freedom does not significantly increase variance on 200 test points.
- *Linear* is correctly excluded: its systematic bias (underfitting) is large enough for the EPA test to reject it.
- *Degree 8* is excluded due to overfitting: its higher test variance makes it statistically worse than the quadratic.

== Where MCS Fails: Outlier Contamination

A critical assumption of the MCS framework is that the *loss function reflects the true comparison of interest*.  When outliers are present, squared-error loss is dominated by a few extreme residuals that are unrelated to model quality, and the bootstrap resampling propagates those outliers, distorting the EPA test statistics.

@mcs_fails_ref shows the MCS analysis from Hansen, Lunde and Nason's type of setup applied to linear data contaminated with circular outliers—reproduced here from prior analysis @hansen2011.

#figure(
  image("references/or_mcs/helpers/demo_results_linear.svg", width: 97%),
  caption: [
    MCS applied to contaminated linear data.  Each row shows a different level of outlier
    contamination (none, some, many).  Columns show Least Squares (LS), RANSAC, LightGBM,
    and RANSAC+LightGBM.  Even at moderate contamination, LS and RANSAC are penalised by
    outlier-driven MSE, while more flexible methods (LightGBM) appear to "win" despite the
    true relationship being linear.
  ],
) <mcs_fails_ref>

@mcs_fails shows our simplified reproduction of the failure case with three models (Linear LS, Quadratic LS, Degree 6 polynomial):

#figure(
  image("figures/problem3_mcs_fails.svg", width: 97%),
  caption: [
    MCS failure on linear data with circular outliers.  Left: fitted models with true inlier
    relationship $y = x$ (black dashed).  Middle: RMSE and MCS p-values on the full
    contaminated dataset—flexible models appear optimal.  Right: the same on clean inliers
    only—Linear LS correctly wins.
  ],
) <mcs_fails>

*Why does MCS fail here?*  There are three compounding reasons:

+ *Non-robust loss.* MSE assigns equal weight to all residuals.  A circular outlier at distance $r$ from the true line contributes $r^2 approx 9$–$36$ to the loss, dwarfing inlier residuals (which are $approx 0.25$).  Flexible models can partially interpolate the outlier cluster, reducing their apparent MSE.
+ *Bootstrap contamination.* The stationary bootstrap resamples the full dataset; with probability proportional to the outlier fraction, resampled batches contain disproportionately many outliers, biasing the variance estimate of $bar(d)_(i j)$ and shrinking effective test power against the flexible model.
+ *Breakdown point of zero.* The standard MCS has no robustness guarantee against outliers.  Its asymptotic validity (Theorem 1) requires the *same* distribution across bootstrap replications; outliers violate this assumption in practice.

When evaluated on clean inliers only (right panel of @mcs_fails), MCS correctly recovers Linear LS as the sole member of the confidence set.  This motivates the research direction of *outlier-robust* model confidence sets.

// ============================================================
= Conclusion
// ============================================================

This work covered three interconnected topics in computational statistics.

*Problem 1* demonstrated that the sampling distribution of the mean rapidly converges to a Normal distribution (CLT), regardless of whether the underlying variable is discrete (Bernoulli) or continuous (Exponential).  The standard error decreases as $sigma/sqrt(n)$; large-sample estimation is far more precise than bootstrap estimation with small $n$, though bootstrap remains useful when data collection is expensive.

*Problem 2* applied the CLT and exact sampling theory (t and chi-squared distributions) to construct 95% confidence intervals for the mean and standard deviation of cholesterol levels.  The coverage property was confirmed by simulation: approximately 5% of intervals miss the true mean, matching the nominal $alpha = 5%$.

*Problem 3* introduced the Model Confidence Set of Hansen, Lunde and Nason (2011), a principled procedure to identify the best-performing model(s) from a candidate set while controlling the probability of excluding the true optimum.  When the data are clean and one model is structurally superior, MCS reliably identifies it.  When outliers are present and squared-error loss is used, MCS can fail: outlier residuals dominate the loss, the bootstrap propagates contamination, and flexible models appear falsely superior.  The remedy is an outlier-robust loss function or a fundamentally different resampling strategy.

// ============================================================
= References
// ============================================================

#bibliography("references.bib", style: "american-psychological-association")
