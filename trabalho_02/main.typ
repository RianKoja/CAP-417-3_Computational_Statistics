#set document(
  title: "Computational Statistics — Exercise List 2",
  author: "Rian Koja",
)

#set page(
  paper: "a4",
  margin: (top: 2.5cm, bottom: 2.5cm, left: 2.5cm, right: 2.5cm),
  numbering: "1",
)

#set text(font: "New Computer Modern", size: 11pt, lang: "en")
#set heading(numbering: "1.1")
#show heading.where(level: 1): h => {
  pagebreak(weak: true)
  v(0.5em)
  h
  v(0.3em)
}
#set math.equation(numbering: "(1)")
#set figure(gap: 0.8em)
#show figure.caption: it => [
  #set text(size: 9.5pt)
  *#it.supplement #it.counter.display():* #it.body
]

// ── cover page ────────────────────────────────────────────────────────────────
#align(center)[
  #v(3cm)
  #text(size: 16pt, weight: "bold")[National Institute for Space Research — INPE]
  #v(0.4cm)
  #text(size: 13pt)[Graduate Program in Applied Computing]
  #v(1.2cm)
  #line(length: 80%)
  #v(0.5cm)
  #text(size: 17pt, weight: "bold")[
    Computational Statistics \
    Exercise List 2
  ]
  #v(0.5cm)
  #line(length: 80%)
  #v(1.5cm)
  #text(size: 13pt)[*Autor:* Rian Koja]
  #v(0.4cm)
  #text(size: 12pt)[#datetime.today().display("[month repr:long] [year]")]
  #v(3cm)
]

#pagebreak()

// ── table of contents ─────────────────────────────────────────────────────────
#outline(
  title: "Contents",
  indent: auto,
)

#pagebreak()

// ── sections ─────────────────────────────────────────────────────────────────
#include "sections/01_visualization.typ"
#include "sections/02_estimation.typ"
#include "sections/03_noise.typ"
#include "sections/04_stochastic.typ"
#include "sections/05_real_data.typ"

// ── references ────────────────────────────────────────────────────────────────
#pagebreak()
= References <references>

#set par(hanging-indent: 1.5em)

[*[hansen2011]*] Hansen, P. R., Lunde, A., & Nason, J. M. (2011).
_The model confidence set_. Econometrica, 79(2), 453–497.

[*[engle1982]*] Engle, R. F. (1982). Autoregressive conditional heteroscedasticity
with estimates of the variance of United Kingdom inflation.
_Econometrica_, 50(4), 987–1007.

[*[bollerslev1986]*] Bollerslev, T. (1986). Generalized autoregressive conditional
heteroskedasticity. _Journal of Econometrics_, 31(3), 307–327.

[*[ormcs]*] Koja, R. (2025). _OR-MCS: Outlier-Robust Model Confidence Set —
Research Study Plan_. INPE.

[*[fischler1981]*] Fischler, M. A., & Bolles, R. C. (1981). Random sample
consensus: a paradigm for model fitting with applications to image analysis
and automated cartography. _Communications of the ACM_, 24(6), 381–395.
