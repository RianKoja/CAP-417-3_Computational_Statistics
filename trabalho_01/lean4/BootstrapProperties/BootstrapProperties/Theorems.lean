import BootstrapProperties.Basic

open BigOperators

/-- The bootstrap mean equals the empirical mean by definition (reflexivity). -/
theorem bootstrap_mean_unbiased
    (X : Sample n) (hn : (n : ℝ) ≠ 0) :
    empiricalMean X = (∑ i : Fin n, X i) / n := by
  rfl

/-- Unfolds empiricalVariance into its raw sum form. -/
theorem empiricalVariance_eq (X : Sample n) (hn : (n : ℝ) ≠ 0) :
    empiricalVariance X =
      (∑ i : Fin n, (X i) ^ 2) / n - ((∑ i : Fin n, X i) / n) ^ 2 := by
  simp [empiricalVariance, empiricalSecondMoment, empiricalMean]

/-- The bootstrap variance of the sample mean is empiricalVariance / n,
    mirroring the true Var(X̄) = σ²/n with σ² replaced by its plug-in estimator. -/
theorem bootstrap_variance_of_mean (X : Sample n) (hn : (n : ℝ) ≠ 0) :
    bootstrapMeanVariance X hn =
      ((∑ i : Fin n, (X i) ^ 2) / n - ((∑ i : Fin n, X i) / n) ^ 2) / n := by
  simp [bootstrapMeanVariance, empiricalVariance,
        empiricalSecondMoment, empiricalMean]
