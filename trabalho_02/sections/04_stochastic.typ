= Stochastic Optimization

== Motivation

Exhaustive grid search is $O(G^2 n)$: for $G = 200$ and $n = 50$, this amounts to
$2 times 10^6$ error evaluations. In larger parameter spaces or with more data,
this cost becomes prohibitive.

An alternative is *stochastic search with random restarts*: at each iteration a pair
$(a, b)$ is sampled uniformly at random; if it improves the best known error it becomes
the new candidate. The process stops when the error falls below a tolerance $tau$ or
when the maximum number of iterations is reached.

== Algorithm

```
Input: x, y, τ = 0.5, max_iter = 50 000
  (a, b) ← Uniform([-5, 5]²)
  best_err ← L2(x, y, a, b)
  for i = 1 to max_iter:
    (a', b') ← Uniform([-5, 5]²)
    err ← L2(x, y, a', b')
    if err < best_err:
      (a, b), best_err ← (a', b'), err
    if best_err < τ: break
Output: â, b̂
```

== Execution Time Comparison

The experiment ran 500 independent rounds of the stochastic search for each
noise level $sigma in {0.1, 0.5, 2.0}$, comparing against 5 rounds of the grid
search (300×300).

#figure(
  image("../figures/04_timing.svg", width: 82%),
  caption: [Mean execution time (± standard deviation) for grid search versus stochastic search.],
) <fig-timing>

#figure(
  caption: [Quantitative summary of execution times and mean iteration counts.],
  table(
    columns: (auto, auto, auto, auto, auto, auto),
    align: (auto, auto, auto, auto, auto, auto),
    table.header[*$sigma$*][*Grid (ms)*][*$plus.minus$*][*Stochastic (ms)*][*$plus.minus$*][*Mean iters*],
    [0.1], [15.4], [2.2],  [105.8], [93.0],  [16 239],
    [0.5], [39.2], [30.8], [333.8], [15.5],  [50 000],
    [2.0], [40.9], [18.8], [349.0], [20.1],  [50 000],
  )
) <tab-timing>

For low noise ($sigma = 0.1$) the stochastic search converges quickly
($approx 16\,000$ iterations), although it takes longer per iteration than the
vectorised grid. For higher noise levels, the threshold $tau$ is never reached and
the algorithm exhausts the maximum number of iterations, becoming slower than the grid.

== Distributions of Recovered Parameters

A direct consequence of the algorithm's randomness is that, by running it many times,
we obtain *distributions* for $hat(a)$ and $hat(b)$. @fig-histograms shows
these distributions across 500 runs for each noise level.

#figure(
  image("../figures/04_param_histograms.svg", width: 100%),
  caption: [
    Distributions of $hat(a)$ (top row) and $hat(b)$ (bottom row) obtained from
    500 independent stochastic runs.
    Dashed black lines: true values. Dotted coloured lines: sample means.
  ],
) <fig-histograms>

== Discussion

The histograms confirm that $hat(a)$ and $hat(b)$ *do have distributions*, centred
on the true values and with spread increasing with $sigma$. This is analogous to the
sampling distribution of the OLS estimator:
$hat(bold(theta)) tilde.op cal(N)(bold(theta)_0, sigma^2 (bold(A)^top bold(A))^(-1))$.

The stochastic search can be interpreted as an implicit sampling of this parameter
space: each run returns a point from this distribution, with bias tending to zero
and variance controlled by the noise level and tolerance $tau$.
