= Parameter Estimation: The Inverse Problem

Given a set of $n$ observed pairs $(x_i, y_i)$, the *inverse problem* consists of
estimating the parameters $(a, b)$ that best explain the data according to some error
criterion.

== Objective Functions

Two classical criteria are defined below.

*L2 — Sum of Squared Errors (OLS):*

$
cal(L)_2(a,b) = sum_(i=1)^n (y_i - a x_i - b)^2
$

*L1 — Sum of Absolute Errors (LAD):*

$
cal(L)_1(a,b) = sum_(i=1)^n |y_i - a x_i - b|
$

The $cal(L)_2$ surface is convex and differentiable, admitting an exact analytical solution.
The $cal(L)_1$ surface is convex but non-differentiable at zero, making analytical
minimization more complex.

== Analytical Solution (OLS)

Writing the system in matrix form with
$bold(A) = [bold(x), bold(1)] in RR^(n times 2)$ and $bold(y) in RR^n$:

$
hat(bold(theta)) = (bold(A)^top bold(A))^(-1) bold(A)^top bold(y), quad
hat(bold(theta)) = [hat(a), hat(b)]^top
$

This expression is computationally efficient ($O(n)$ for well-conditioned data) and
yields the minimum-variance unbiased estimator (Gauss-Markov theorem).

== Exhaustive Grid Search

An alternative is to evaluate $cal(L)$ over a dense grid of $(a,b)$ pairs and select the
pair with the lowest error. With a $300 times 300$ grid the cost is
$O(G^2 n)$ evaluations — adequate for illustration, but not scalable.

== Results

Synthetic data were generated with $a_0 = 1.5$, $b_0 = -2.0$ and $n = 50$
observations with Gaussian noise $sigma = 0.8$.
@fig-surface-L2 and @fig-surface-L1 show the error surfaces.
@fig-fit-comp overlays the estimated lines on the data.

#figure(
  image("../figures/02_error_surface_L2.svg", width: 85%),
  caption: [L2 error surface. The white star marks the true value; the red ✕ marks the grid minimum.],
) <fig-surface-L2>

#figure(
  image("../figures/02_error_surface_L1.svg", width: 85%),
  caption: [L1 error surface. Non-differentiability produces sharper edges near the minimum.],
) <fig-surface-L1>

#figure(
  image("../figures/02_fit_comparison.svg", width: 90%),
  caption: [Comparison of fitted lines: true (black), analytical OLS (red), and grid L2 (blue).],
) <fig-fit-comp>

#figure(
  caption: [Parameter recovery: comparison of methods.],
  table(
    columns: (auto, auto, auto, auto, auto, auto),
    align: center,
    table.header[*Method*][*$hat(a)$*][*$hat(b)$*][*$|Delta a|$*][*$|Delta b|$*][*Time*],
    [True], [1.5000], [-2.0000], [—], [—], [—],
    [Grid L2], [1.5217], [-2.1472], [0.0217], [0.1472], [374 ms],
    [Grid L1], [1.4950], [-2.2274], [0.0050], [0.2274], [—],
    [Analytical OLS], [1.5121], [-2.1368], [0.0121], [0.1368], [0.17 ms],
  )
) <tab-recovery>

== Discussion

The analytical OLS is $approx 2200times$ faster than the grid search and produces
comparable results. The grid L1 achieved the smallest error in $a$ in this experiment,
illustrating that different criteria may prefer slightly different solutions
in the presence of Gaussian noise.
