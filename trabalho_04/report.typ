// ============================================================
//  Computational Statistics — Assignment 04
//  Instituto Nacional de Pesquisas Espaciais (INPE)
//  Author: Rian Koja
// ============================================================

#let res = toml("outputs/results.toml")

#set page(
  paper: "a4",
  margin: (top: 1.9cm, bottom: 1.9cm, left: 2.2cm, right: 2.2cm),
  numbering: "1",
  number-align: center,
)
#set text(font: "Linux Libertine", size: 10.5pt, lang: "en")
#set heading(numbering: "1.")
#set par(justify: true, leading: 0.60em)
#show heading.where(level: 1): it => { v(0.4em); it; v(0.15em) }
#show heading.where(level: 2): it => { v(0.25em); it; v(0.08em) }

// --- FRONT MATTER ---
#align(center)[
  #v(0.3em)
  #text(size: 12pt)[Instituto Nacional de Pesquisas Espaciais (INPE)] \
  #text(size: 11pt)[Graduate Program in Applied Computing (CAP)] \
  #v(1em)
  #text(size: 19pt, weight: "bold")[Computational Statistics] \
  #v(0.3em)
  #text(size: 14pt)[Assignment 04 — Soybean Sprout Growth Analysis] \
  #v(0.8em)
  #text(size: 12pt)[*Author:* Rian Koja] \
  #text(size: 11pt)[April 2026] \
  #v(0.4em)
]

#line(length: 100%, stroke: 0.5pt)
#v(0.2em)

= Dataset Overview

The *CongNaMul* dataset #cite(<ban2023congnamul>) documents soybean sprout cultivation for smart-agriculture research. Researchers photographed *#res.data.n_total individual sprouts* against three backgrounds (clear, green checkered, white checkered) and measured five physical attributes: *head length*, *body length*, *body thickness*, *tail length* (mm) and *weight* (mg). Since each individual appears in all three backgrounds with identical measurements, deduplication yields *#res.data.n_total unique sprouts*. Two records with clear measurement errors (body length of 9 129 mm; body thickness of 20.9 mm — both beyond the 3 × IQR fence) are removed, leaving *n = #res.data.n_total*. Weight data are available for *#res.data.n_weight sprouts*; the remaining #res.data.n_missing are coded −1 (missing).

#figure(
  image("figs/fig0_dataset_overview.jpg", width: 95%),
  caption: [
    Visual overview of the CongNaMul dataset showing: (a) background types, (b) single sprout
    images for segmentation and measurement, and (c) multiple sprout images for density studies.
  ],
) <fig-overview>

= Descriptive Statistics

#figure(
  include "outputs/tbl_desc.typ",
  caption: [
    Descriptive statistics (*n* = #res.data.n_total for morphological features; *n* = #res.data.n_weight for weight). \
    Ex. Kurt. = excess (Fisher) kurtosis = Pearson kurtosis − 3; a Normal distribution has excess kurtosis = 0.
    Positive values indicate heavier tails than Normal; negative values indicate lighter tails.
  ],
) <tbl-desc>

#figure(
  image("figs/fig1_distributions.svg", width: 98%),
  caption: [
    Histograms with KDE (blue) and fitted Normal curves (dashed) for all four morphological
    features (*n* = #res.data.n_total). Head length closely matches the Normal fit; body length shows
    positive skew and leptokurtosis (excess kurtosis = 1.33).
  ],
) <fig-dist>

= Normality Testing

Two complementary tests were applied to each feature (@tbl-norm). *Shapiro–Wilk* (S-W) is powerful for small-to-moderate samples and sensitive to tail departures. *Kolmogorov–Smirnov* (K-S) measures the maximum CDF distance; with parameters estimated from the same data it becomes conservative. S-W rejects normality for body length and tail length (both p < 0.05), consistent with their skewness in @tbl-desc. K-S fails to reject any feature (minimum p = #res.normality.ks_min_p), illustrating its lower power when parameters are estimated.

#figure(
  include "outputs/tbl_norm.typ",
  caption: [
    Normality test results (*n* = #res.data.n_total). *H*#sub[0]: the data are drawn from a Normal distribution.
    *H*#sub[1]: the data are not Normally distributed. Bold p-values indicate rejection of *H*#sub[0]
    at α = 0.05. W = Shapiro–Wilk statistic; D = Kolmogorov–Smirnov statistic (maximum absolute
    CDF deviation).
  ],
) <tbl-norm>

#figure(
  image("figs/fig2_qqplots.svg", width: 96%),
  caption: [
    Normal Q-Q plots. Systematic deviation in the right tails of body length and tail length
    confirms the positive skew flagged by Shapiro–Wilk.
  ],
) <fig-qq>

= Correlation and Regression

== Pairwise Correlations

@fig-corr shows Pearson correlations for the #res.data.n_weight weight-complete sprouts. The strongest predictors of *weight* are body thickness (r = #res.correlations.thickness_r) and head length (r = #res.correlations.head_r), both p #res.correlations.head_p. Body length is moderately correlated (r = #res.correlations.body_r, p #res.correlations.body_p). Tail length shows no significant linear relationship (r = #res.correlations.tail_r, p = #res.correlations.tail_p).

#figure(
  image("figs/fig3_correlation.svg", width: 55%),
  caption: [Pearson correlation heatmap (*n* = #res.data.n_weight).],
) <fig-corr>

== OLS vs RANSAC Regression

Both an ordinary least-squares (OLS) model and a RANSAC (Random Sample Consensus) model were fitted to predict weight from all four morphological features. RANSAC iteratively identifies an inlier consensus set that minimises residuals, making it robust to atypical observations. The automatic residual threshold (median absolute deviation) classified *#res.regression.n_inliers sprouts as inliers* and *#res.regression.n_outliers as outliers*.

#figure(
  include "outputs/tbl_models.typ",
  caption: [
    OLS vs RANSAC coefficient comparison. R²(OLS) = #res.regression.r2_ols (all *n* = #res.data.n_weight);
    R²(RANSAC) = #res.regression.r2_ransac_inliers on inliers only (*n* = #res.regression.n_inliers).
    Bold p-values: significant at α = 0.05.
  ],
) <tbl-models>

#figure(
  image("figs/fig4_ransac.svg", width: 98%),
  caption: [
    Fitted vs actual weight for OLS (left) and RANSAC (right). RANSAC outliers (red ×, n = #res.regression.n_outliers)
    are sprouts whose weight deviates substantially from the linear morphology–weight relationship.
    The identity line (dashed) represents a perfect fit.
  ],
) <fig-ransac>

Both models agree on the sign and rough magnitude of all coefficients. RANSAC achieves R² = #res.regression.r2_ransac_inliers on its inlier set by discarding the #res.regression.n_outliers atypical observations, while OLS uses all data and obtains R² = #res.regression.r2_ols. The similar coefficient estimates confirm that OLS is not severely distorted by the outliers, but RANSAC reveals a tighter underlying relationship among the majority of sprouts. Tail length remains non-significant under OLS and negligibly small under RANSAC, confirming it adds no predictive value.

= Conclusions

Three morphological dimensions — head length, body length, and body thickness — jointly predict soybean sprout weight with R² = #res.regression.r2_ols (OLS) and R² = #res.regression.r2_ransac_inliers among the inlier consensus set (RANSAC). Tail length contributes no predictive information. Head length is the only feature whose distribution is well approximated by a Normal; body length and tail length display mild right skew detected by the more powerful Shapiro–Wilk test but missed by Kolmogorov–Smirnov, highlighting the importance of choosing an appropriate normality test for moderate sample sizes.

#bibliography("references/congnamul.bib", title: "References", style: "ieee")
