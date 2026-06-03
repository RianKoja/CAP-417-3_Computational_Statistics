// theme.typ
// Basic Touying theme for CAP 417 presentation

#import "@preview/touying:0.3.0": *

// Color palette
#let cap417-blue = rgb("#005f9e")
#let cap417-dark = rgb("#08304a")
#let cap417-light = rgb("#e8f2fa")
#let cap417-accent = rgb("#d95f02")

#let cap417-theme = theme.with(
  // Background and text
  background: cap417-light,
  foreground: cap417-dark,

  // Fonts
  text: (
    family: "Liberation Sans",
    size: 24pt,
  ),
  heading: (
    family: "Liberation Sans",
    weight: "bold",
    color: cap417-blue,
  ),

  // Title slide customization happens via a helper below
)

// Title slide helper
#let title-slide() = slide(
  fill: linear-gradient(
    start: (0%, 0%),
    end: (100%, 100%),
    stops: ((0%, cap417-dark), (100%, cap417-blue)),
  ),
  foreground: white,
  [
    align(center)[
      = CAP 417 — Trabalho Final

      #v(0.8em)
      *Louis Bachelier, IA Generativa e Estatística Computacional*

      #v(1.2em)
      Autor: _Seu Nome_

      Curso: CAP 417 — Estatística Computacional

      Data: _[Preencher data da apresentação]_
    ]
  ]
)