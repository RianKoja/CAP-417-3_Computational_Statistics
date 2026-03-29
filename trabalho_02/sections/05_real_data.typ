= Real Data Application: Financial Returns and GARCH Models

== Motivation and Data Description

Financial returns constitute an abundant, publicly accessible dataset with rich
statistical properties that make linear regression an instructive starting point
— *and an insufficient one*.

Daily closing price series for four assets between
2019-01-03 and 2024-12-30 were downloaded via Yahoo Finance:
Petrobras (PETR4.SA), Vale (VALE3.SA), Ibovespa (^BVSP), and S\&P 500 (SPY).
Log-returns are computed as $r_t = 100 times log(P_t / P_(t-1))$ (in percentage points).

#figure(
  image("../figures/05_returns.svg", width: 100%),
  caption: [Daily log-return series (%) for the four assets. Period: 2019–2024.],
) <fig-returns>

== Linear Regression: $r_t$ on $r_(t-1)$

The first approach directly applies the tools from previous sections:
fitting a line $r_t = a r_(t-1) + b$ (@fig-linear-fit).

#figure(
  image("../figures/05_linear_fit.svg", width: 95%),
  caption: [Linear regression of $r_t$ on $r_(t-1)$. $R^2 approx 0$ for all assets.],
) <fig-linear-fit>

The coefficients of determination are around $R^2 < 0.01$, confirming
that *successive returns are practically uncorrelated* — consistent with the
efficient market hypothesis. The linear model is therefore inadequate for
describing the dynamics of $r_t$.

What the linear model *fails* to capture, however, is visible in @fig-returns:
periods of high volatility (e.g., March 2020, COVID-19 crisis) alternate with
calm periods — the phenomenon of *volatility clustering*. Modelling the
*conditional variance* is therefore necessary.

== GARCH(1,1) Model

The GARCH(1,1) model (_Generalized Autoregressive Conditional Heteroskedasticity_)
[Engle, 1982] [Bollerslev, 1986] specifies:

$
r_t = sigma_t epsilon_t, quad epsilon_t tilde.op D(0,1)
$

$
sigma_t^2 = omega + alpha r_(t-1)^2 + beta sigma_(t-1)^2
$

where $omega > 0$, $alpha, beta >= 0$ and $alpha + beta < 1$
(stationarity condition). The parameter $alpha$ captures the volatility response
to recent shocks; $beta$, the persistence of past volatility. $D(0,1)$ denotes the
innovation distribution, which we consider in two forms: the standard Normal
$cal(N)(0,1)$ and the standardised Student-$t$ with $nu$ degrees of freedom.

== Estimated Parameters (Normal Distribution)

#figure(
  caption: [GARCH(1,1)-Normal parameters estimated by maximum likelihood. Persistence: $alpha + beta$.],
  table(
    columns: (auto, auto, auto, auto, auto),
    align: (left, auto, auto, auto, auto),
    table.header[*Asset*][*$hat(omega)$*][*$hat(alpha)$*][*$hat(beta)$*][*Persistence*],
    [Petrobras (PETR4)], [0.4621], [0.1487], [0.7851], [0.934],
    [Vale (VALE3)],      [0.0923], [0.0474], [0.9314], [0.979],
    [Ibovespa],          [0.0448], [0.0897], [0.8873], [0.977],
    [S\&P 500 (SPY)],    [0.0605], [0.1781], [0.7827], [0.961],
  )
) <tab-garch-params>

All assets exhibit *high persistence* ($alpha + beta > 0.93$), indicating that
volatility shocks dissipate slowly. Petrobras shows the largest relative $alpha$
(more immediate response to shocks), while Vale exhibits the largest $beta$
(higher volatility inertia).

#figure(
  image("../figures/05_volatility.svg", width: 100%),
  caption: [
    Daily returns (grey) and conditional volatility $hat(sigma)_t$ (red) estimated by GARCH(1,1).
    The $plus.minus hat(sigma)_t$ bands are symmetric by construction.
  ],
) <fig-volatility>

== Model Diagnostics

#figure(
  image("../figures/05_qq.svg", width: 95%),
  caption: [
    Q-Q plot of GARCH(1,1)-Normal standardised residuals $hat(epsilon)_t = r_t / hat(sigma)_t$
    against Normal quantiles.
    Tail deviations indicate residual leptokurtosis — the Normal assumption is misspecified.
  ],
) <fig-qq>

The Q-Q plots in @fig-qq reveal a systematic pattern: the Normal-GARCH residuals
deviate from the diagonal at both tails, confirming that even after removing volatility
clustering, the innovations exhibit *fat tails* (leptokurtosis). This motivates
replacing the Normal innovation with a heavier-tailed distribution.

#figure(
  image("../figures/05_acf.svg", width: 100%),
  caption: [
    Autocorrelation function (ACF) of $r_t^2$ before (top row) and after GARCH (bottom row).
    GARCH removes most of the squared-return autocorrelation.
  ],
) <fig-acf>

The ACF of $r_t^2$ shows significant correlations before the GARCH fit
(@fig-acf, top row), evidencing volatility clustering. After fitting (bottom row),
correlations are substantially reduced, validating the model.

== Normal vs. Student-$t$ Innovation Distribution

=== Motivation

The Q-Q plots above show that Normal-GARCH residuals have heavier tails than
the Normal distribution predicts. A natural remedy is to specify
$epsilon_t tilde.op t_nu$ — a standardised Student-$t$ with $nu$ degrees of freedom,
where smaller $nu$ implies fatter tails. As $nu -> infinity$ the model collapses
to the Normal.

=== Q-Q Comparison

@fig-dist-comp (Petrobras) illustrates the improvement: whereas Normal-GARCH
residuals bend away from the diagonal at the extremes (left panel), Student-$t$-GARCH
residuals align substantially better with the corresponding $t(hat(nu))$ quantiles
(right panel).

#figure(
  image("../figures/05_dist_comparison.svg", width: 100%),
  caption: [
    Petrobras: Q-Q plot of GARCH(1,1)-Normal residuals against $cal(N)(0,1)$ quantiles (left)
    versus GARCH(1,1)-$t$ residuals against $t(hat(nu))$ quantiles (right).
    The Student-$t$ specification produces markedly better tail alignment.
  ],
) <fig-dist-comp>

=== AIC / BIC Comparison

#figure(
  caption: [
    AIC and BIC for GARCH(1,1)-Normal versus GARCH(1,1)-$t$.
    $hat(nu)$: estimated degrees of freedom. Lower AIC/BIC = better penalised fit.
    Bold: preferred specification per criterion.
  ],
  table(
    columns: (auto, auto, auto, auto, auto, auto),
    align: (left, auto, auto, auto, auto, auto),
    table.header[*Asset*][*Normal AIC*][*Normal BIC*][*t AIC*][*t BIC*][*$hat(nu)$*],
    [Petrobras], [6557], [6578], [*6367*], [*6393*], [4.4],
    [Vale],      [6344], [6365], [*6197*], [*6223*], [4.9],
    [Ibovespa],  [4782], [4803], [*4741*], [*4768*], [9.4],
    [S\&P 500],  [4145], [4166], [*4040*], [*4066*], [6.1],
  )
) <tab-dist-compare>

The Student-$t$ specification improves both AIC and BIC for every asset, with
AIC reductions ranging from 41 points (Ibovespa) to 190 points (Petrobras).
The estimated degrees of freedom $hat(nu) in [4.4, 9.4]$ are well within the
heavy-tail regime ($nu << 30$), confirming that the Normal assumption is
statistically rejected. The BIC improvement is also significant despite the extra
parameter $nu$, meaning the heavier tails are genuinely warranted by the data.
Brazilian assets (PETR4, VALE3) exhibit lower $hat(nu)$ than the U.S. ones,
consistent with their higher propensity for extreme return events.

=== Interpretation

The key finding is that *GARCH(1,1) with a Student-$t$ innovation is the preferred
specification* across all assets: it captures volatility clustering (via $alpha, beta$)
and fat tails (via $nu$) simultaneously. The Normal GARCH is useful as a baseline
but systematically underestimates the probability of extreme returns — a critical
failure for risk management applications.

== Order Selection: AIC and BIC (Normal, Multiple Orders)

#figure(
  caption: [AIC and BIC for three GARCH-Normal specifications. Lower values = better penalised fit.],
  table(
    columns: (auto, auto, auto, auto, auto, auto, auto),
    align: (left, auto, auto, auto, auto, auto, auto),
    table.header[*Asset*][*GARCH(1,1) AIC*][*BIC*][*GARCH(2,1) AIC*][*BIC*][*GARCH(1,2) AIC*][*BIC*],
    [Petrobras], [6557], [6578], [6559], [6586], [*6551*], [6577],
    [Vale],      [6344], [6365], [6346], [6373], [*6342*], [6369],
    [Ibovespa],  [*4782*], [*4803*], [4783], [4809], [4784], [4810],
    [S\&P 500],  [*4145*], [*4166*], [4147], [4173], [4147], [4173],
  )
) <tab-aic-bic>

For Petrobras and Vale, GARCH(1,2) offers a slight AIC advantage, while BIC penalises
the extra parameter and does not favour it conclusively. For Ibovespa and S\&P 500,
GARCH(1,1) is already the most parsimonious specification and is preferred by both
criteria.

== Discussion: Is Linear Regression Appropriate?

*No*, for the purpose of return forecasting. Linear regression $r_t = a r_(t-1) + b$
yields $R^2 approx 0$ and residuals with strong patterns in variance — violating the
homoscedasticity assumed by OLS.

The GARCH model explicitly captures *conditional heteroscedasticity*, modelling
$sigma_t^2$ as a function of history. It does *not* forecast the sign of $r_t$
(conditional mean is zero), but enables the estimation of dynamic confidence intervals
and risk measures such as conditional VaR.

The correct approach for financial time series is therefore to:

1. Abandon linear mean models ($R^2 approx 0$ offers no predictive value).
2. Model *conditional variance* with GARCH($p$,$q$).
3. Use a *fat-tailed innovation* (Student-$t$) to capture extreme return events.

The Normal GARCH is a useful pedagogical baseline, but for practical risk management
the Student-$t$ specification is strongly preferred — as confirmed by both information
criteria and visual diagnostics.
