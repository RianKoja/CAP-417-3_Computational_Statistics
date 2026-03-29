= Data Visualization: $y = a x + b$

Simple linear regression models the relationship between an explanatory variable $x$ and
a response variable $y$ through two parameters: the *slope* $a$ and the
*intercept* $b$.

$
y = a x + b
$

The coefficient $a$ determines the *slope* of the line — positive, zero, or negative —
while $b$ fixes the point where the line crosses the $y$-axis when $x = 0$.

To build visual intuition, @fig-param-grid presents a grid of lines
generated with combinations of $a in {-2, -0.5, 0, 0.5, 2, 10}$ and
$b in {-5, 0, 5}$. Lines with $a > 0$ are drawn in red
(positive slope), with $a = 0$ in green (horizontal) and with $a < 0$ in blue
(negative slope). The black dot in each panel marks the $y$-intercept $(0, b)$.

#figure(
  image("../figures/01_param_grid.svg", width: 100%),
  caption: [
    Grid of lines $y = a x + b$ for different values of $a$ (columns) and $b$ (rows).
    Red: $a > 0$; green: $a = 0$; blue: $a < 0$.
    The black dot indicates the $y$-intercept.
  ],
) <fig-param-grid>

#pagebreak()

== Observations

- When $a = 0$ the line is horizontal, regardless of the value of $b$.
- A large value of $a$ ($a = 10$) produces nearly vertical lines, highly sensitive to
  small changes in $x$.
- The parameter $b$ shifts the line vertically without changing its slope.
- The $x$-intercept (root) is $x^* = -b/a$ for $a != 0$.
