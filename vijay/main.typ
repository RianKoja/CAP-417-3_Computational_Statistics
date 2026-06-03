#set page(
  paper: "a4",
  margin: (x: 2.5cm, y: 2.5cm),
  numbering: "1 / 1",
)
#set text(
  font: "New Computer Modern",
  size: 11pt,
  lang: "en",
)
#set heading(numbering: "1.1")

#align(center)[
  #v(5cm)
  #text(24pt, weight: "bold")[Computational Statistics]
  #v(1cm)
  #text(18pt)[Exercise List Solutions]
  #v(2cm)
  #text(14pt)[Proposed by: Professor Vijay Kumar]
  #v(0.5cm)
  #text(14pt)[Student: Rian Koja]
  #v(5cm)
  #text(12pt)[April 2026]
  #pagebreak()
]

#outline(indent: 2em)
#pagebreak()

= Problem List 1: Basic Probability

== Problem 1 -- Sample Space & Tree Diagram

*Statement:* Suppose that 3 (three) items are selected at random from a manufacturing process.
Each item is inspected and classified as defective (D), or nondefective (ND). What are the
elements of the sample space, $Omega$?

Besides showing the elements, use a Tree Diagram to show all the elements.

*Solution:*

Each item has two possible states: D (Defective) or N (Nondefective). For three items the total
number of outcomes is $2^3 = 8$. The sample space is:

$ Omega = {"DDD", "DDN", "DND", "DNN", "NDD", "NDN", "NND", "NNN"} $

The tree diagram below shows all branching outcomes across the three successive inspections:

#align(center)[
  #image("assets/tree_diagram.png", width: 65%)
]

== Problem 2 -- Basic Probabilities on a Die

*Statement:* Given $Omega = {1, 2, 3, 4, 5, 6}$ and the following events:

- $A =$ Odd Number
- $B =$ Prime Number
- $C =$ Less than 4
- $D =$ Less than 7
- $E =$ Greater than 6

Compute:

- $P(C) = ?$
- $P(D) = ?$
- $P(E) = ?$
- $P(A inter B) = ?$
- $P(A union B) = ?$
- $P(D inter E) = ?$
- $C^c = ?$
- $B^c = ?$

*Solution:*

Expanding the events: $A = {1,3,5}$, $B = {2,3,5}$, $C = {1,2,3}$, $D = {1,2,3,4,5,6}$,
$E = emptyset$.

- $P(C) = 3\/6 = 1\/2 = 0.5$
- $P(D) = 6\/6 = 1.0$
- $P(E) = 0\/6 = 0$
- $A inter B = {3,5}$, so $P(A inter B) = 2\/6 = 1\/3 approx 0.3333$
- $A union B = {1,2,3,5}$, so $P(A union B) = 4\/6 = 2\/3 approx 0.6667$
- $P(D inter E) = P(emptyset) = 0$
- $C^c = {4,5,6}$
- $B^c = {1,4,6}$

== Problem 3 -- Deck of Cards

*Statement:* A deck of cards contains 52 cards. By chance, one is drawn. What are the
probabilities of the following events:

- The card is Queen of Hearts
- The card is a Queen
- The card is of Hearts
- The card is King, Queen or Jack
- The drawn card is not King

*Solution:*

1. $P("Queen of Hearts") = 1\/52 approx 0.0192$

2. $P("Queen") = 4\/52 = 1\/13 approx 0.0769$

3. $P("Hearts") = 13\/52 = 1\/4 = 0.25$

4. $P("K, Q, or J") = 12\/52 = 3\/13 approx 0.2308$

5. $P("not King") = 1 - P("King") = 1 - 4\/52 = 48\/52 = 12\/13 approx 0.9231$

== Problem 4 -- Flight Passengers

*Statement:* In a flight, there are 100 Brazilians, 90 Americans, 38 Spaniards, and 73 British
in a Mortal (Economy) Class. If a person is randomly selected to be upgraded to the Business
class, find the probability that the person chosen is:

- (a) a Brazilian
- (b) an American or British
- (c) a Spaniard or Brazilian

Also find out $P(Omega) = ?$

*Solution:*

Total passengers $= 100 + 90 + 38 + 73 = 301$.

- (a) $P("Brazilian") = 100\/301 approx 0.3322$
- (b) $P("American or British") = (90 + 73)\/301 = 163\/301 approx 0.5415$
- (c) $P("Spaniard or Brazilian") = (38 + 100)\/301 = 138\/301 approx 0.4585$
- $P(Omega) = 301\/301 = 1.0$

== Problem 5 -- Weather in SJ Campos

*Statement:* The probability that tomorrow will be a cold day in SJCampos is 0.5. The probability
that it will be a rainy day is 0.65. The probability that it will be both cold and rainy is 0.45.
What is the probability that it will be neither cold nor rainy?

*Solution:*

By the inclusion-exclusion principle:

$ P("Cold" union "Rainy") = P("Cold") + P("Rainy") - P("Cold" inter "Rainy") $
$ P("Cold" union "Rainy") = 0.5 + 0.65 - 0.45 = 0.7 $

$ P("Neither") = 1 - P("Cold" union "Rainy") = 1 - 0.7 = bold(0.3) $

== Problem 6 -- Conditional Probability $P(B|A)$

*Statement:* Given $Omega = {1, 2, 3, 4, 5, 6}$:

- $A =$ Odd numbers: $A = {1, 3, 5}$
- $B =$ Numbers $gt.eq 2$: $B = {2, 3, 4, 5, 6}$

It was shown that $P(A | B) = n(A inter B) \/ n(B) = 2\/5 = 0.4$.

Calculate $P(B | A)$.

*Solution:*

$ P(B | A) = frac(n(B inter A), n(A)) $

$B inter A = {3,5}$, so $n(B inter A) = 2$ and $n(A) = 3$, giving:

$ P(B | A) = 2\/3 approx bold(0.6667) $

== Problem 7 -- Gender and Marital Status

*Statement:* 400 people were classified according to their Gender and Marital Status as follows:

#table(
  columns: (auto,) * 6,
  align: center,
  table.header([], [*Single*], [*Married*], [*Divorced*], [*Widow*], [*Total*]),
  [Male],   [50], [60], [40], [30], [180],
  [Female], [150], [40], [10], [20], [220],
  [Total],  [200], [100], [50], [50], [400],
)

Calculate the following probabilities:

- A Person is Single given the Person is of Male Gender
- A Person is Divorced given the Person is of Female Gender
- A Person is of Female Gender given the Person is Divorced

*Solution:*

1. $P("Single" | "Male") = 50\/180 = 5\/18 approx bold(0.2778)$

2. $P("Divorced" | "Female") = 10\/220 = 1\/22 approx bold(0.0455)$

3. $P("Female" | "Divorced") = 10\/50 = bold(0.2)$

== Problem 8 -- Flight with Gender Breakdown (Conditional)

*Statement:* In a flight, there are 100 Brazilians (55 men and 45 women), 90 Americans
(30 men and 60 women), 38 Spaniards (all men), and 73 British (12 men and 61 women) in the
Economy (Mortals) Class. If a person is randomly selected to upgrade to the Business Class,
find the probability that the person chosen is:

- A Brazilian given the person is a man
- An American given the person is a woman
- A man given the person is a Spaniard

*Solution:*

Total men $= 55 + 30 + 38 + 12 = 135$. Total women $= 45 + 60 + 0 + 61 = 166$.

- $P("Brazilian" | "Man") = 55\/135 approx bold(0.4074)$
- $P("American" | "Woman") = 60\/166 approx bold(0.3614)$
- $P("Man" | "Spaniard") = 38\/38 = bold(1.0)$

== Problem 9 -- COVID Test (Bayes Theorem)

*Statement:* A new COVID test was evaluated with a group of people of which are known to have
been truly infected. The test diagnosis is positive among 98% of those which are truly infected
and of those who are not indeed infected. What is the probability that someone testing positive
for COVID under this new test is actually infected?

*Solution:*

The problem states the test is positive for 98% of truly infected individuals. Interpreting this
as sensitivity $P(+ | "Inf") = 0.98$ and specificity $P(- | "Not Inf") = 0.98$ (false positive
rate 2%), and applying Bayes' theorem:

$ P("Inf" | +) = frac(P(+ | "Inf") P("Inf"), P(+ | "Inf") P("Inf") + P(+ | "Not Inf") P("Not Inf")) $

$ P("Inf" | +) = frac(0.98 p, 0.98 p + 0.02(1-p)) $

The result depends on the prior prevalence $p$. Assuming $p = 0.5$ (equal prior):

$ P("Inf" | +) = frac(0.98 times 0.5, 0.98 times 0.5 + 0.02 times 0.5) = frac(0.49, 0.50) = bold(0.98) $

== Problem 10 -- Target Shooting (Independent Events)

*Statement:* Two people are practicing target shooting. The probability that the first person
hits the target is $P(A) = 1\/3$ and the probability that the second person hits the target is
$P(B) = 2\/3$.

Given that $A$ and $B$ are independent events, what is the probability that:

- Both hit the target
- At least one hits the target

*Solution:*

Since $A$ and $B$ are independent:

- Both hit: $P(A inter B) = P(A) P(B) = frac(1, 3) times frac(2, 3) = frac(2, 9) approx bold(0.2222)$

- At least one: $P(A union B) = P(A) + P(B) - P(A inter B) = frac(1, 3) + frac(2, 3) - frac(2, 9) = frac(7, 9) approx bold(0.7778)$

== Problem 11 -- Balls Without Replacement (Multiplicative Rule)

*Statement:* A box contains 8 red balls, 3 white balls, and 4 black balls. One ball is chosen
at random and, without replacement, another ball is chosen, also at random. What is the
probability that:

- The first is red and the second is white?
- The first is white and the second is red?
- The first and second are red?

*Solution:*

Total balls $= 8 + 3 + 4 = 15$.

- $P(R_1, W_2) = frac(8, 15) times frac(3, 14) = frac(24, 210) = frac(4, 35) approx bold(0.1143)$

- $P(W_1, R_2) = frac(3, 15) times frac(8, 14) = frac(24, 210) = frac(4, 35) approx bold(0.1143)$

- $P(R_1, R_2) = frac(8, 15) times frac(7, 14) = frac(56, 210) = frac(4, 15) approx bold(0.2667)$

== Problem 12 -- Naive Bayes Email Classification

*Statement:* A company wants to classify emails as Spam and Not Spam.

*Priors:* $P("Spam") = 0.3$ and $P("Not Spam") = 0.7$

*Likelihoods:*

- $P("FREE" | "Spam") = 0.8$
- $P("FREE" | "NotSpam") = 0.1$
- $P("WIN" | "Spam") = 0.6$
- $P("WIN" | "NotSpam") = 0.05$

Assume that the Naive Bayes independence assumption holds. A new email contains the words
FREE and WIN.

- Compute the Spam score: $P("FREE", "WIN" | "Spam") times P("Spam")$
- Compute the Not Spam score: $P("FREE", "WIN" | "NotSpam") times P("NotSpam")$
- Classify the email

*Solution:*

Under the Naive Bayes independence assumption:

- Spam score: $P("FREE","WIN" | "Spam") times P("Spam") = 0.8 times 0.6 times 0.3 = bold(0.144)$
- Not Spam score: $P("FREE","WIN" | "NotSpam") times P("NotSpam") = 0.1 times 0.05 times 0.7 = bold(0.0035)$

Since $0.144 > 0.0035$, the email is classified as *Spam*.

#pagebreak()
= Problem List 2: Discrete Distributions

== Problem 1 -- Joint Probabilities

*Statement:* Given that the probability of drawing a Red card from a standard deck is
$26\/52 = 1\/2 = 0.5$, and $P(6 inter "Red") = P(6) times P("Red") = 4\/52 times 26\/52$,
use a *Venn Diagram* to show the intersection of the events "drawing a 6" and
"drawing a Red card."

*Solution:*

- $P("6") = 4\/52$ (four sixes in the deck)
- $P("Red") = 26\/52 = 1\/2$ (26 red cards)
- $P("6" inter "Red") = 4\/52 times 26\/52 = 2\/52 = 1\/26 approx 0.0385$ (6 of Hearts and 6 of Diamonds)

The numbers in the Venn Diagram below represent card counts out of 52:

#align(center)[
  #image("assets/venn_diagram.png", width: 60%)
]

== Problem 2 -- Binomial Distribution

*Statement:* In a manufacturing process, *three* items are selected at random. Each item is
inspected and classified as *D* (Defective) or *N* (Non-Defective). The idea is to know about
Defective items. So, a Defective item is a success (and Non-Defective is a failure). The items
are selected independently. The process produces *25% Defective* items.

- Calculate the *PMF* (Probability Distribution) of the random variable $X$ related to this example.
- Show also the *Probability Histogram*.

*Solution:*

With $n=3$ and $p=0.25$, the binomial PMF is $P(X=x) = binom(n, x) p^x (1-p)^(n-x)$:

#table(
  columns: (auto,) * 4,
  align: center,
  table.header([*$x$*], [*Calculation*], [*Exact*], [*Decimal*]),
  [$0$], [$binom(3, 0)(0.25)^0 (0.75)^3$], [$27\/64$], [$0.421875$],
  [$1$], [$binom(3, 1)(0.25)^1 (0.75)^2$], [$27\/64$], [$0.421875$],
  [$2$], [$binom(3, 2)(0.25)^2 (0.75)^1$], [$9\/64$], [$0.140625$],
  [$3$], [$binom(3, 3)(0.25)^3 (0.75)^0$], [$1\/64$], [$0.015625$],
)

#align(center)[
  #image("assets/histogram.png", width: 70%)
]

== Problem 3 -- Uniform Distribution

*Statement:* The variance of the discrete uniform distribution is given by:

$ sigma^2 = frac((x_"high" - x_"low" + 1)^2 - 1, 12) $

*Why is the denominator 12? Find out.*

*Solution:*

For $X$ uniform on ${1, 2, dots, n}$ where $n = x_"high" - x_"low" + 1$, we derive
the variance from first principles. The mean and second moment are:

$ E[X] = frac(n+1, 2), quad E[X^2] = frac(1, n) sum_(i=1)^n i^2 = frac(n(n+1)(2n+1), 6n) = frac((n+1)(2n+1), 6) $

Therefore:

$ "Var"(X) = E[X^2] - (E[X])^2 = frac((n+1)(2n+1), 6) - frac((n+1)^2, 4) $

$ "Var"(X) = (n+1) lr([frac(2n+1, 6) - frac(n+1, 4)]) = (n+1) frac(4(2n+1) - 6(n+1), 24) $

$ "Var"(X) = (n+1) frac(2n - 2, 24) = frac((n+1)(n-1), 12) = frac(n^2-1, 12) $

The *12* comes from $"lcm"(6, 4) = 12$, the least common multiple of the denominators of
$E[X^2]$ and $(E[X])^2$.

== Problem 4 -- Poisson Distribution

*Statement 4a:* A call center receives an average of *5 calls per minute*. What is the
probability that they receive *exactly 3 calls* in a given minute?

*Statement 4b:* A bakery sells an average of *12 loaves of bread per hour*. What is the
probability that they sell *at most 8 loaves* in a given hour?

*Solution:*

The Poisson PMF is $P(X=k) = e^(-lambda) lambda^k \/ k!$.

*4a.* $lambda = 5$, $k = 3$:

$ P(X=3) = frac(e^(-5) dot 5^3, 3!) = frac(e^(-5) times 125, 6) approx bold(0.1404) $

*4b.* $lambda = 12$, $k lt.eq 8$:

$ P(X lt.eq 8) = sum_(k=0)^(8) frac(e^(-12) dot 12^k, k!) approx bold(0.1550) $

#pagebreak()
= Problem List 3: Continuous Distributions

== Problem 1 -- Continuous Random Variables

=== Problem 1.1

*Statement:* A fly lands on a 30 cm long ruler at a random position chosen uniformly along the
ruler. Let $X$ be the position of the fly in centimeters. Let $f_X (x)$ be the probability
density function for $X$. What is $f_X (5)$?

*Solution:*

Since the fly lands uniformly, $X tilde.op "Uniform"(0, 30)$, giving:

$ f_X (x) = frac(1, 30) quad "for" x in [0, 30] $

Therefore: $ f_X (5) = 1\/30 approx bold(0.0333) $

=== Problem 1.2

*Statement:* Let $X$ be a continuous random variable which has the PDF $f(x) = 3$ for
$[0, 1\/3]$. Calculate:

- $P(0.1 lt.eq X lt.eq 0.2)$
- The CDF

*Solution:*

$ P(0.1 lt.eq X lt.eq 0.2) = integral_(0.1)^(0.2) 3 space d x = 3 times (0.2 - 0.1) = bold(0.3) $

The CDF is obtained by integrating $f$:

$
  F(x) = cases(
    0 & "if" x < 0,
    3x & "if" 0 lt.eq x lt.eq 1\/3,
    1 & "if" x > 1\/3,
  )
$

== Problem 2 -- Continuous Uniform Distribution

=== Problem 2.1

*Statement:* Given that the variance of the continuous uniform distribution is
$sigma = (b - a)^2 \/ 12$, find out why 12 is the denominator.

*Solution:*

The mean is $mu = (a+b)\/2$. The variance is:

$ "Var"(X) = integral_a^b (x - mu)^2 frac(1, b-a) space d x $

Substituting $u = x - mu$ (so $d u = d x$, limits shift to $plus.minus(b-a)\/2$):

$
  "Var"(X) = frac(1, b-a) integral_(-(b-a)\/2)^((b-a)\/2) u^2 space d u = frac(1, b-a) lr([frac(u^3, 3)])_(-(b-a)\/2)^((b-a)\/2)
$

$
  "Var"(X) = frac(1, b-a) dot frac(2 lr(((b-a)\/2))^3, 3) = frac(1, b-a) dot frac((b-a)^3, 12) = bold(frac((b-a)^2, 12))
$

The denominator 12 arises because evaluating $lr([u^3\/3])$ over the symmetric limits
$plus.minus(b-a)\/2$ yields a factor of $2 dot ((b-a)\/2)^3 \/ 3$, and dividing by $(b-a)$
reduces this to $(b-a)^2 \/ 12$.

=== Problem 2.2

*Statement:* A random variable $X$ is uniformly distributed between 32 and 42. What is the
probability that $X$ will be between 32 and 40?

*Solution:*

$ P(32 < X < 40) = frac(40 - 32, 42 - 32) = frac(8, 10) = bold(0.8) $

== Problem 3 -- Gamma Distribution

=== Problem 3.1

*Statement:* The scenario is a call center where a new call arrives every 4 minutes. It is
important to plan staff's breaks. What is the expected (average) time it takes for 3 calls
to arrive?

*Solution:*

With rate $lambda = 1\/4$ calls per minute, the waiting time for $alpha = 3$ arrivals follows
a Gamma distribution. The expected value is:

$ E[T] = alpha \/ lambda = 3 \/ (1\/4) = bold(12) "minutes" $

=== Problem 3.2

*Statement:* Draw a graph varying parameters $alpha$ and $beta$ of the Gamma Distribution.

*Solution:*

#align(center)[
  #image("assets/gamma_plots.png", width: 85%)
]

=== Problem 3.3

*Statement:* Write the PDF and CDF of the Gamma Distribution.

*Solution:*

The PDF of the Gamma distribution with shape $alpha > 0$ and rate $beta > 0$ is:

$ f(x; alpha, beta) = frac(beta^alpha, Gamma(alpha)) x^(alpha - 1) e^(-beta x), quad x > 0 $

The CDF is given by the regularized lower incomplete gamma function:

$ F(x; alpha, beta) = frac(gamma(alpha, beta x), Gamma(alpha)) $

where $gamma(alpha, beta x) = integral_0^(beta x) t^(alpha-1) e^(-t) d t$ is the lower
incomplete gamma function.

=== Problem 3.4

*Statement:* Cite a few examples of problem types in which the Gamma Distribution is employed.

*Solution:*

- *Queuing theory:* time until the $k$-th customer or event arrives in a Poisson process.
- *Hydrology:* modelling rainfall totals and river discharge volumes.
- *Reliability engineering:* lifetime of a system requiring multiple sequential exponential-stage failures.
- *Bayesian statistics:* conjugate prior for the Poisson rate $lambda$.

== Problem 4 -- Exponential Distribution

=== Problem 4.1

*Statement:* Prove that the Exponential Distribution is memoryless.

*Solution:*

The memoryless property states $P(X > s+t | X > s) = P(X > t)$ for all $s, t > 0$.

For $X tilde.op "Exp"(lambda)$, the survival function is $P(X > t) = e^(-lambda t)$. Then:

$
  P(X > s+t | X > s) = frac(P(X > s+t), P(X > s)) = frac(e^(-lambda(s+t)), e^(-lambda s)) = frac(e^(-lambda s) e^(-lambda t), e^(-lambda s)) = e^(-lambda t) = P(X > t)
$

$ therefore P(X > s + t | X > s) = P(X > t) quad square.filled $

The past waiting time $s$ carries no information about the future --- the distribution resets
at each moment.

=== Problem 4.2

*Statement:* What is the relationship between the Exponential Distribution and the Poisson
Process?

*Solution:*

If events occur in a Poisson process at rate $lambda$ (the count of events in $[0, t]$ follows
$"Poisson"(lambda t)$), then the *inter-arrival time* between consecutive events follows
$"Exp"(lambda)$. This duality is fundamental: the Poisson process counts rare events per unit
time, while the Exponential distribution models the continuous waiting time between them.
