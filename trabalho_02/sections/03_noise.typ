= Noise Analysis and Model Selection

== Noise Models

Real data rarely follow an exact relationship. Three perturbation models are
considered, where $epsilon, epsilon_1, epsilon_2 tilde.op cal(N)(0, sigma^2)$ i.i.d.:

*Additive noise:*
$
tilde(y) = a x + b + epsilon
$

*Multiplicative noise:*
$
tilde(y) = (a x + b)(1 + epsilon)
$

*Combined noise:*
$
tilde(y) = (a x + b)(1 + epsilon_1) + epsilon_2
$

== Statistical Impact

For each model, the mean $EE[tilde(y)]$ and variance $"Var"[tilde(y)]$ are derived
analytically as a function of $sigma$.

#figure(
  caption: [Statistical properties of the noise models ($a=1.5, b=-2$).],
  table(
    columns: (auto, auto, auto),
    align: (left, center, center),
    table.header[*Model*][*$EE[tilde(y)]$*][*$"Var"[tilde(y)]$*],
    [Additive],       [$a x + b$], [$sigma^2$],
    [Multiplicative], [$a x + b$], [$(a x + b)^2 sigma^2$],
    [Combined],       [$a x + b$], [$(a x + b)^2 sigma^2 + sigma^2$],
  )
) <tab-noise-theory>

*Key result:* all three models preserve the mean when $EE[epsilon] = 0$.
The variance, however, grows in different ways: in multiplicative noise it scales
with $(a x + b)^2$, penalising regions of large magnitude; in the combined model
both contributions accumulate.

@tab-noise-mc validates these expressions via Monte Carlo ($10\,000$ realisations),
confirming the match between analytical and empirical values.

#figure(
  caption: [Monte Carlo validation: analytical vs. empirical means and variances (selection $sigma in {0.1, 1, 2}$).],
  table(
    columns: (auto, auto, auto, auto, auto, auto),
    align: (left, auto, auto, auto, auto, auto),
    table.header[*Model*][*$sigma$*][*$EE$ analytical*][*$EE$ MC*][*Var analytical*][*Var MC*],
    [Additive],        [0.1], [-2.000], [-2.000], [0.010],  [0.010],
    [Additive],        [1.0], [-2.000], [-1.999], [1.000],  [0.998],
    [Additive],        [2.0], [-2.000], [-1.999], [4.000],  [3.997],
    [Multiplicative], [0.1], [-2.000], [-2.000], [0.110],  [0.110],
    [Multiplicative], [1.0], [-2.000], [-1.993], [10.979], [10.947],
    [Multiplicative], [2.0], [-2.000], [-1.996], [43.915], [43.791],
    [Combined],       [0.1], [-2.000], [-2.000], [0.120],  [0.120],
    [Combined],       [1.0], [-2.000], [-1.997], [11.979], [11.994],
    [Combined],       [2.0], [-2.000], [-2.007], [47.915], [47.681],
  )
) <tab-noise-mc>

#figure(
  image("../figures/03_noise_analysis.svg", width: 100%),
  caption: [
    Scatter of one realisation for each model (rows) and noise intensity (columns).
    The true line is shown in black.
  ],
) <fig-noise>

#pagebreak()

== Model Selection under Contamination: OR-MCS Reproduction

The noise analysis raises a deeper question: given that multiple fitting methods can be
evaluated on noisy data, *which one is actually the best?*
The _Model Confidence Set_ (MCS) procedure [Hansen et al., 2011] answers this in a
statistically rigorous way: given a confidence level $1-alpha$, it identifies the
minimal subset of models that contains the best one with probability $>= 1-alpha$.

To illustrate its application — and its limitations — we reproduce the OR-MCS experiment
[Koja, 2025]. Nine datasets are generated:
linear ($y=x$), quadratic ($y=x^2$) and exponential ($y=e^x$) relationships,
each in three variants: no outliers, ~20%, and ~50% contamination.
Four methods are fitted: Least Squares (LS), RANSAC, LightGBM, and
RANSAC+LightGBM. The MCS is computed at $alpha = 0.10$.

#figure(
  image("../figures/or_mcs/demo_results_linear.svg", width: 100%),
  caption: [Fits of the four methods for linear data (none / some / many outliers).
            Blue dots: inliers; red dots: outliers.
            Circles indicate points classified as inliers by RANSAC; crosses, as outliers.],
) <fig-ormcs-linear>

#figure(
  image("../figures/or_mcs/demo_results_quadratic.svg", width: 100%),
  caption: [Fits for quadratic data. Same convention as @fig-ormcs-linear.],
) <fig-ormcs-quad>

#figure(
  image("../figures/or_mcs/demo_results_exponential.svg", width: 100%),
  caption: [Fits for exponential data. Same convention as @fig-ormcs-linear.],
) <fig-ormcs-exp>

=== MCS p-value Analysis

#figure(
  caption: [
    Selected MCS p-values (10% confidence level). Models with $p > 0.10$ belong
    to the confidence set. Results for the heavy-outlier scenarios.
  ],
  table(
    columns: (auto, auto, auto, auto, auto),
    align: (left, auto, auto, auto, auto),
    table.header[*Dataset*][*LS*][*RANSAC*][*LightGBM*][*RANSAC+LightGBM*],
    [Linear (Many)],      [0.012], [0.099], [*1.000*], [0.753],
    [Quadratic (Many)],  [0.246], [0.246], [*1.000*], [0.158],
    [Exponential (Many)], [0.765], [0.747], [*1.000*], [0.424],
  )
) <tab-mcs-pvals>

=== Critical Interpretation

The results reveal a *fundamental weakness* of the original MCS: under heavy
contamination, it systematically selects LightGBM as the "best" model
(@tab-mcs-pvals). LightGBM, being highly flexible, interpolates the outliers
rather than rejecting them, achieving lower loss on the full dataset — but this is
precisely overfitting behaviour.

RANSAC with the correct model is the most robust estimator visually (@fig-ormcs-linear),
but the MCS rarely distinguishes it as superior to plain LS, demonstrating that
*the original MCS was not designed to operate in the presence of outliers*.
This motivates OR-MCS: a procedure that integrates RANSAC's outlier detection with
the sequential confidence guarantees of the MCS.
