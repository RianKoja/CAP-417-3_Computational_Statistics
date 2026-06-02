
## Problem Statements — CAP-417-3 Computational Statistics

### Problem 1 — Sample Space \& Tree Diagram

*(Slide 11)*

Suppose that 3 (three) items are selected at random from a manufacturing process. Each item is inspected and classified as defective (D), or nondefective (ND). What are the elements of the sample space, Ω?

Besides showing the elements, use a Tree Diagram to show all the elements.

***

### Problem 2 — Basic Probabilities on a Die

*(Slide 19)*

Given Ω = {1, 2, 3, 4, 5, 6} and the following events:

- A = Odd Number
- B = Prime Number
- C = Less than 4
- D = Less than 7
- E = Greater than 6

Compute:

- P(C) = ?
- P(D) = ?
- P(E) = ?
- P(A ∩ B) = ?
- P(A ∪ B) = ?
- P(D ∩ E) = ?
- C^c = ?
- B^c = ?

***

### Problem 3 — Deck of Cards

*(Slide 20)*

A deck of cards contains 52 cards. By chance, one is drawn. What are the probabilities of the following events:

- The card is Queen of Hearts
- The card is a Queen
- The card is of Hearts
- The card is King, Queen or Jack
- The drawn card is not King

***

### Problem 4 — Flight Passengers

*(Slide 21)*

In a flight, there are 100 Brazilians, 90 Americans, 38 Spaniards, and 73 British in a Mortal (Economy) Class. If a person is randomly selected to be upgraded to the Business class, find the probability that the person chosen is:

- (a) a Brazilian
- (b) an American or British
- (c) a Spaniard or Brazilian

Also find out P(Ω) = ?

***

### Problem 5 — Weather in SJ Campos

*(Slide 22)*

The probability that tomorrow will be a cold day in SJCampos is 0.5. The probability that it will be a rainy day is 0.65. The probability that it will be both cold and rainy is 0.45. What is the probability that it will be neither cold nor rainy?

***

### Problem 6 — Conditional Probability P(B|A)

*(Slide 25)*

Given Ω = {1, 2, 3, 4, 5, 6}:

- A = Odd numbers: A = {1, 3, 5}
- B = Numbers ≥ 2: B = {2, 3, 4, 5, 6}

It was shown that P(A | B) = n(A ∩ B) / n(B) = 2/5 = 0.4.

Calculate P(B | A).

***

### Problem 7 — Gender and Marital Status

*(Slide 26)*

400 people were classified according to their Gender and Marital Status as follows:


|  | Single | Married | Divorced | Widow | Total |
| :-- | :-- | :-- | :-- | :-- | :-- |
| Male | 50 | 60 | 40 | 30 | 180 |
| Female | 150 | 40 | 10 | 20 | 220 |
| Total | 200 | 100 | 50 | 50 | 400 |

Calculate the following probabilities:

- A Person is Single given the Person is of Male Gender
- A Person is Divorced given the Person is of Female Gender
- A Person is of Female Gender given the Person is Divorced

***

### Problem 8 — Flight with Gender Breakdown (Conditional)

*(Slide 27)*

In a flight, there are 100 Brazilians (55 men and 45 women), 90 Americans (30 men and 60 women), 38 Spaniards (all men), and 73 British (12 men and 61 women) in the Economy (Mortals) Class. If a person is randomly selected to upgrade to the Business Class, find the probability that the person chosen is:

- A Brazilian given the person is a man
- An American given the person is a woman
- A man given the person is a Spaniard

***

### Problem 9 — COVID Test (Bayes Theorem)

*(Slide 45)*

A new COVID test was evaluated with a group of people of which are known to have been truly infected. The test diagnosis is positive among 98% of those which are truly infected and of those who are not indeed infected. What is the probability that someone testing positive for COVID under this new test is actually infected?

***

### Problem 10 — Target Shooting (Independent Events)

*(Slide 48)*

Two people are practicing target shooting. The probability that the first person hits the target is P(A) = 1/3 and the probability that the second person hits the target is P(B) = 2/3.

Given that A and B are independent events, what is the probability that:

- Both hit the target
- At least one hits the target

***

### Problem 11 — Balls Without Replacement (Multiplicative Rule)

*(Slide 49)*

A box contains 8 red balls, 3 white balls, and 4 black balls. One ball is chosen at random and, without replacement, another ball is chosen, also at random. What is the probability that:

- The first is red and the second is white?
- The first is white and the second is red?
- The first and second are red?

***

### Problem 12 — Naïve Bayes Email Classification

*(Slides 56–57)*

A company wants to classify emails as Spam and Not Spam.

**Priors:** P(Spam) = 0.3 and P(Not Spam) = 0.7

**Likelihoods:**

- P("FREE" | Spam) = 0.8
- P("FREE" | NotSpam) = 0.1
- P("WIN" | Spam) = 0.6
- P(WIN | NotSpam) = 0.05

Assume that the Naïve Bayes independence assumption holds. A new email contains the words FREE and WIN.

- Compute the Spam score: P("FREE","WIN" | Spam) × P(Spam)
- Compute the Not Spam score: P("FREE","WIN" | NotSpam) × P(NotSpam)
- Classify the email

