// ============================================================
//  Computational Statistics — Assignment 04
//  Instituto Nacional de Pesquisas Espaciais (INPE)
//  Author: Rian Koja
// ============================================================

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

The *CongNaMul* dataset #cite(<ban2023congnamul>) documents soybean sprout cultivation for smart-agriculture research. Researchers photographed *205 individual sprouts* against three backgrounds (clear, green checkered, white checkered) and measured five physical attributes: *head length*, *body length*, *body thickness*, *tail length* (mm) and *weight* (mg). Since each individual appears in all three backgrounds with identical measurements, deduplication yields *205 unique sprouts*. Two records with clear measurement errors (body length of 9 129 mm; body thickness of 20.9 mm — both beyond the 3 × IQR fence) are removed, leaving *n = 203*. Weight data are available for *158 sprouts*; the remaining 45 are coded −1 (missing).

#figure(
  image("figs/fig0_dataset_overview.jpg", width: 95%),
  caption: [
    Visual overview of the CongNaMul dataset showing: (a) background types, (b) single sprout
    images for segmentation and measurement, and (c) multiple sprout images for density studies.
  ],
) <fig-overview>

= Descriptive Statistics

#figure(
  table(
    columns: (auto, 1fr, 1fr, 1fr, 1fr, 1fr, 1fr),
    align: (left, center, center, center, center, center, center),
    stroke: none,
    table.hline(stroke: 0.8pt),
    table.header(
      [*Feature*], [*Mean*], [*SD*], [*Median*], [*Skewness*], [*Ex. Kurt.*#super[†]], [*Range*],
    ),
    table.hline(stroke: 0.4pt),
    [Head length (mm)],    [11.96], [1.09], [11.92], [ 0.11], [−0.42], [9.1 – 14.9],
    [Body length (mm)],    [88.80], [11.38], [87.49], [ 0.34], [ 1.33], [49.8 – 135.9],
    [Body thickness (mm)], [ 2.40], [ 0.28], [ 2.38], [−0.23], [ 0.84], [1.4 – 3.2],
    [Tail length (mm)],    [91.69], [21.29], [90.90], [−0.01], [−0.84], [45.6 – 142.0],
    [Weight (mg)],         [ 0.762], [0.136], [0.753], [—], [—], [0.47 – 1.11],
    table.hline(stroke: 0.8pt),
  ),
  caption: [
    Descriptive statistics (*n* = 203 for morphological features; *n* = 158 for weight). \
    #super[†] Excess (Fisher) kurtosis = Pearson kurtosis − 3; a Normal distribution has excess kurtosis = 0. Positive values indicate heavier tails than Normal; negative values indicate lighter tails.
  ],
) <tbl-desc>

#figure(
  image("figs/fig1_distributions.svg", width: 98%),
  caption: [
    Histograms with KDE (blue) and fitted Normal curves (dashed) for all four morphological
    features (*n* = 203). Head length closely matches the Normal fit; body length shows
    positive skew and leptokurtosis (excess kurtosis = 1.33).
  ],
) <fig-dist>

= Normality Testing

Two complementary tests were applied to each feature (@tbl-norm). *Shapiro–Wilk* (S-W) is powerful for small-to-moderate samples and sensitive to tail departures. *Kolmogorov–Smirnov* (K-S) measures the maximum CDF distance; with parameters estimated from the same data it becomes conservative. S-W rejects normality for body length and tail length (both p < 0.05), consistent with their skewness in @tbl-desc. K-S fails to reject any feature (all p > 0.22), illustrating its lower power when parameters are estimated.

#figure(
  table(
    columns: (auto, 1fr, 1fr, 1fr, 1fr),
    align: (left, center, center, center, center),
    stroke: none,
    table.hline(stroke: 0.8pt),
    table.header(
      [*Feature*], [*S-W W*], [*S-W p*], [*K-S D*], [*K-S p*],
    ),
    table.hline(stroke: 0.4pt),
    [Head length],    [0.9933], [0.482], [0.0474], [0.733],
    [Body length],    [0.9825], [*0.013*], [0.0664], [0.318],
    [Body thickness], [0.9883], [0.094], [0.0499], [0.673],
    [Tail length],    [0.9823], [*0.012*], [0.0723], [0.227],
    table.hline(stroke: 0.8pt),
  ),
  caption: [
    Normality test results (*n* = 203). *H*#sub[0]: the data are drawn from a Normal distribution.
    *H*#sub[1]: the data are not Normally distributed. Bold p-values indicate rejection of *H*#sub[0]
    at α = 0.05. W = Shapiro–Wilk statistic; D = Kolmogorov–Smirnov statistic (maximum absolute
    CDF deviation). Neither statistic alone is meaningful — the p-value determines the decision.
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

@fig-corr shows Pearson correlations for the 158 weight-complete sprouts. The strongest predictors of *weight* are body thickness (r = 0.67) and head length (r = 0.62), both p < 0.001. Body length is moderately correlated (r = 0.41, p < 0.001). Tail length shows no significant linear relationship (r = 0.10, p = 0.21).

#figure(
  image("figs/fig3_correlation.svg", width: 55%),
  caption: [Pearson correlation heatmap (*n* = 158).],
) <fig-corr>

== OLS vs RANSAC Regression

Both an ordinary least-squares (OLS) model and a RANSAC (Random Sample Consensus) model were fitted to predict weight from all four morphological features. RANSAC iteratively identifies an inlier consensus set that minimises residuals, making it robust to atypical observations. The automatic residual threshold (median absolute deviation) classified *131 sprouts as inliers* and *27 as outliers*.

#figure(
  table(
    columns: (auto, 1fr, 1fr, 1fr, 1fr, 1fr),
    align: (left, center, center, center, center, center),
    stroke: none,
    table.hline(stroke: 0.8pt),
    table.header(
      [*Predictor*], [*OLS coef.*], [*OLS p*], [*RANSAC coef.*], [*OLS R²*], [*RANSAC R²*],
    ),
    table.hline(stroke: 0.4pt),
    [Intercept],      [−1.055], [< 0.001], [−1.046], table.cell(rowspan: 5)[0.739], table.cell(rowspan: 5)[0.868#super[†]],
    [Head length],    [ 0.0463], [< 0.001], [ 0.0415],
    [Body length],    [ 0.0059], [< 0.001], [ 0.0052],
    [Body thickness], [ 0.3037], [< 0.001], [ 0.3195],
    [Tail length],    [−0.0001], [  0.889], [ 0.0005],
    table.hline(stroke: 0.8pt),
  ),
  caption: [
    OLS vs RANSAC coefficient comparison. #super[†] RANSAC R² computed on inliers only (n = 131).
    OLS R² computed on all 158 observations.
  ],
) <tbl-models>

#figure(
  image("figs/fig4_ransac.svg", width: 98%),
  caption: [
    Fitted vs actual weight for OLS (left) and RANSAC (right). RANSAC outliers (red ×, n = 27)
    are sprouts whose weight deviates substantially from the linear morphology–weight relationship.
    The identity line (dashed) represents a perfect fit.
  ],
) <fig-ransac>

Both models agree on the sign and rough magnitude of all coefficients. RANSAC achieves R² = 0.868 on its inlier set by discarding the 27 atypical observations, while OLS uses all data and obtains R² = 0.739. The similar coefficient estimates confirm that OLS is not severely distorted by the outliers, but RANSAC reveals a tighter underlying relationship among the majority of sprouts. Tail length remains non-significant under OLS and negligibly small under RANSAC, confirming it adds no predictive value.

= Conclusions

Three morphological dimensions — head length, body length, and body thickness — jointly predict soybean sprout weight with R² ≈ 0.74 (OLS) and R² ≈ 0.87 among the inlier consensus set (RANSAC). Tail length contributes no predictive information. Head length is the only feature whose distribution is well approximated by a Normal; body length and tail length display mild right skew detected by the more powerful Shapiro–Wilk test but missed by Kolmogorov–Smirnov, highlighting the importance of choosing an appropriate normality test for moderate sample sizes.

#bibliography("references/congnamul.bib", title: "References", style: "ieee")
