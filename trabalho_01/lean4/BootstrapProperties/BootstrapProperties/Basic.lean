import Mathlib.Algebra.BigOperators.Group.Finset.Basic
import Mathlib.Data.Finset.Basic
import Mathlib.Data.Real.Basic

def hello := "world"

open BigOperators

variable {n : ℕ}

def Sample (n : ℕ) := Fin n → ℝ

noncomputable def empiricalMean (X : Sample n) : ℝ :=
  (∑ i, X i) / n

noncomputable def empiricalSecondMoment (X : Sample n) : ℝ :=
  (∑ i, (X i) ^ 2) / n

noncomputable def empiricalVariance (X : Sample n) : ℝ :=
  empiricalSecondMoment X - (empiricalMean X) ^ 2

noncomputable def bootstrapMeanVariance (X : Sample n) (hn : (n : ℝ) ≠ 0) : ℝ :=
  empiricalVariance X / n
