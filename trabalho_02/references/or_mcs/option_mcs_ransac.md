# an option I've been considering for my phd thesis is the following:

1-the RANSAC is an example of an outlier robust regression method, based on the idea that outlier don't vote consistently when evaluating different models, whether valid or not
2-The model confidence set is a technique by hansen, lunde and nason that allows determining a subset of models that has less than p probability of not containing the optimal model, and is likely an optimized subset. It depends on the loss metric and uses bootstrapping, but is not robust to outliers.

My initial idea would be to formulate the properties of both methods using lean or another language fit for theorem proving. Then creating and proving a new technique that could be branded as an outlier rejecting or outlier robust MCS, thus achieving the properties of both methods and creating a novel technique with wide application potential.

Create a fully fleshed out and referenced phd proposal (i.e. the document I should send to get accepted on the program, specifying my planned activities)
Mention what is the known state of the art on this regard and what effectively I would eb contributing.

Based on the search results, I now have sufficient information to craft a comprehensive PhD proposal that combines RANSAC's outlier robustness with the Model Confidence Set methodology, formalized through theorem proving. Let me create a detailed research proposal suitable for INPE's Applied Computing doctoral program.

***

# PhD Research Proposal: Outlier-Robust Model Confidence Sets with Formal Verification

**Candidate:** [Your Name]
**Program:** Doctorate in Applied Computing (CAP)
**Institution:** Instituto Nacional de Pesquisas Espaciais (INPE)
**Research Line:** Computational Modeling / Artificial Intelligence for Space Applications

## Executive Summary

This research proposes developing a novel statistical framework that unifies outlier-robust model selection with rigorous confidence guarantees through formal verification. The methodology combines RANSAC's (Random Sample Consensus) consensus-based outlier rejection mechanism with Hansen, Lunde, and Nason's Model Confidence Set (MCS) procedure, creating an "Outlier-Robust Model Confidence Set" (OR-MCS) formally verified using theorem-proving languages such as Lean. This contribution addresses a critical gap in model selection theory where existing methods either provide robustness or confidence guarantees, but not both simultaneously.[^1][^2][^3]

## Research Context and Motivation

### Current State of the Art

**RANSAC for Outlier Robustness**
RANSAC is an iterative, non-deterministic algorithm that estimates model parameters by separating data into inliers and outliers, using only inliers for final model estimation. The algorithm operates on the principle that outliers do not vote consistently when evaluating different model hypotheses. RANSAC has proven highly effective in computer vision and robust regression, particularly with contaminated datasets containing significant proportions of outliers.[^4][^5][^6][^1]

**Model Confidence Set Procedure**
The MCS procedure constructs a set of models with a specified confidence level (1-α) of containing the optimal forecasting model. It employs sequential hypothesis testing with bootstrap resampling to eliminate inferior models, resulting in a statistically rigorous subset likely containing the best model. However, MCS assumes clean data and is not robust to outliers, as bootstrap procedures can propagate contaminated samples.[^2][^7][^8]

**Gap in Literature**
Recent work on robust model selection has addressed outlier contamination through MM-estimators and stratified bootstrap, but these approaches do not provide the formal confidence guarantees of MCS. Conversely, MCS applications assume data quality that is unrealistic in many practical scenarios, particularly in space systems where sensor noise, communication errors, and anomalous measurements are common. No existing framework combines RANSAC's outlier detection principles with MCS's rigorous confidence set construction.[^6][^8][^1][^2]

**Formal Verification Gap**
While formal methods have been applied to correctness verification in software and algorithms, statistical procedures—particularly those involving bootstrapping and randomized algorithms—remain largely unverified formally. Lean and similar theorem provers offer the capability to establish mathematical guarantees about statistical properties, providing unprecedented reliability for critical applications.[^3][^9][^10]

## Research Objectives

### General Objective

Develop, formalize, and validate an Outlier-Robust Model Confidence Set (OR-MCS) methodology that simultaneously achieves RANSAC's outlier resistance and MCS's confidence guarantees, with properties formally verified using theorem-proving systems.

### Specific Objectives

1. **Theoretical Formulation**: Formalize the mathematical properties of RANSAC and MCS using category theory and measure-theoretic probability, identifying compatibility conditions for their integration.
2. **Algorithm Development**: Design the OR-MCS algorithm that incorporates:
    - Consensus-based outlier detection inspired by RANSAC principles
    - Bootstrap-based model elimination following MCS methodology
    - Stratified resampling that respects inlier/outlier structure[^8]
3. **Formal Verification**: Implement complete formal proofs in Lean 4 establishing:
    - Asymptotic validity (coverage probability guarantees)
    - Robustness properties (breakdown points, influence functions)
    - Algorithmic termination and complexity bounds
4. **Empirical Validation**: Conduct comprehensive simulation studies and real-world applications demonstrating:
    - Superior performance under various outlier contamination scenarios
    - Computational efficiency relative to existing methods
    - Application to satellite telemetry and space system anomaly detection
5. **Software Implementation**: Develop production-quality implementations in Python and Julia with formal specifications linking to verified theorems.

## Methodology

### Phase 1: Theoretical Foundation (Months 1-12)

**Literature Review and Formalization**
Conduct systematic review of robust statistics, model selection theory, and formal verification approaches. Translate core definitions and theorems into Lean 4's type theory framework.[^10][^6][^3]

**Property Specification**
Formally define:

- Outlier contamination models (ε-contamination, Huber mixture models)
- Consensus voting mechanisms and breakdown points
- Bootstrap distribution convergence under contamination
- Confidence set coverage probability under model misspecification

**Deliverables**: Formal Lean library of statistical foundations; conference paper on formalization methodology.

### Phase 2: Algorithm Design (Months 13-24)

**Core Algorithm Development**
Design OR-MCS procedure incorporating:

- Iterative consensus-based inlier identification (generalizing RANSAC)
- Adaptive threshold selection using statistical validation (similar to AC-RANSAC)[^11]
- Stratified bootstrap respecting detected inlier/outlier structure[^8]
- Sequential model elimination with outlier-robust loss functions

**Formal Proof Construction**
Prove in Lean:

- Theorem 1: OR-MCS achieves asymptotic coverage probability (1-α) under ε-contamination for ε below breakdown point
- Theorem 2: OR-MCS consensus mechanism converges to true inlier set with probability approaching 1
- Theorem 3: Computational complexity bounds for algorithm termination

**Deliverables**: Formally verified OR-MCS specification; journal paper on theoretical properties.

### Phase 3: Implementation and Validation (Months 25-36)

**Software Development**
Implement OR-MCS in Python (leveraging scikit-learn ecosystem) and Julia (for high-performance numerical computing), with formal specifications extracted from Lean proofs.[^3]

**Simulation Studies**
Systematic comparison against:

- Standard MCS[^2]
- Robust regression with AIC/BIC (MM-estimators)[^6]
- RANSAC-based model selection[^1]
- Cross-validation with robust loss functions

Scenarios covering: varied outlier proportions (0-30%), model dimensions, sample sizes, and contamination types.

**Real-World Applications**
Apply to:

- Satellite attitude determination with sensor outliers (leveraging INPE's mission data)
- Time series forecasting for space weather indices
- Orbit determination with measurement anomalies

**Deliverables**: Open-source software packages with formal correctness certificates; empirical validation papers.

### Phase 4: Dissertation Writing (Months 37-48)

Synthesize theoretical contributions, formal proofs, implementation details, and empirical results into comprehensive dissertation. Prepare manuscripts for high-impact journals in statistics, machine learning, and space systems.

## Expected Contributions

### Theoretical Contributions

1. **Novel Statistical Methodology**: First framework unifying outlier robustness with rigorous confidence set construction, filling critical gap in model selection theory.[^2][^6]
2. **Formal Verification of Statistical Procedures**: Pioneering application of theorem proving to bootstrap-based inference, establishing new standards for reliability in statistical computing.[^10]
3. **Breakdown Point Analysis**: Rigorous characterization of robustness properties for confidence set procedures under contamination.

### Practical Contributions

1. **Reliable Model Selection for Space Systems**: Direct applicability to INPE's satellite missions, enabling robust autonomous decision-making under anomalous conditions.
2. **Open-Source Tools**: Production-quality implementations serving statistics, machine learning, and aerospace communities.
3. **Computational Efficiency**: Algorithms scalable to modern high-dimensional problems through optimized consensus testing and parallel bootstrap.

### Methodological Innovation

The integration of formal verification with statistical methodology represents a paradigm shift toward provably correct data science, particularly valuable for safety-critical applications in aerospace and autonomous systems.[^9][^3]

## Feasibility and Resources

### Academic Preparation

Candidate possesses:

- Master's degree in Engineering and Space Technologies from INPE (2019)
- 12 credits in Applied Computing (2019-2021)
- Professional experience in satellite AOCS systems and data pipelines
- Strong programming background (Python, Julia, functional programming)


### Institutional Resources

INPE's Applied Computing program provides:

- World-class faculty in computational modeling and AI[^12]
- Access to satellite telemetry datasets for validation
- High-performance computing infrastructure
- International collaboration networks
- CAPES/CNPq scholarship opportunities[^13]


### Timeline Viability

Four-year timeline aligns with INPE doctoral requirements, with clear phase demarcations enabling progress monitoring and early publication opportunities.

## Expected Impact

This research will:

1. Advance theoretical statistics by bridging robust estimation and model selection
2. Establish new standards for verified statistical software in critical applications[^10]
3. Enhance INPE's capabilities in autonomous satellite anomaly detection
4. Contribute to Brazil's leadership in space technology and computational science
5. Generate high-impact publications and open-source software serving international communities

The combination of theoretical depth, formal rigor, and practical applicability positions this work at the intersection of statistics, computer science, and aerospace engineering—perfectly aligned with INPE's interdisciplinary Applied Computing program.[^12]

## References

All sources cited inline are available in the web search results provided. Key foundational works include:

- Hansen, P. R., Lunde, A., \& Nason, J. M. (2003). The Model Confidence Set[^2]
- Fischler \& Bolles (1981). RANSAC algorithm (original formulation)[^1]
- Lean theorem prover documentation and formal verification frameworks[^3]
- Müller, S. (2005). Outlier robust model selection in linear regression[^8]

***

**Candidate Signature:** _______________
**Date:** November 26, 2025
<span style="display:none">[^14][^15][^16][^17][^18][^19][^20][^21][^22][^23][^24][^25][^26][^27][^28]</span>

<div align="center">⁂</div>

[^1]: https://developer.nvidia.com/blog/dealing-with-outliers-using-three-robust-linear-regression-models/

[^2]: https://economics.brown.edu/sites/default/files/papers/2003-5_paper.pdf

[^3]: https://venturebeat.com/ai/lean4-how-the-theorem-prover-works-and-why-its-the-new-competitive-edge-in

[^4]: https://scikit-learn.org/stable/auto_examples/linear_model/plot_ransac.html

[^5]: https://www.linkedin.com/pulse/ransac-random-sample-consensus-rajathilagar-r-raj--4yzff

[^6]: https://www.nature.com/articles/s41598-022-14398-1

[^7]: https://lup.lub.lu.se/student-papers/record/1337277/file/1647311.pdf

[^8]: https://www.tandfonline.com/doi/abs/10.1198/016214505000000529

[^9]: https://www.rd.ntt/e/cs/team_project/media/computing_theory/research_media14.html

[^10]: https://nvlpubs.nist.gov/nistpubs/ir/2019/NIST.IR.8274.pdf

[^11]: https://www.ipol.im/pub/art/2022/357/article_lr.pdf

[^12]: https://www.gov.br/inpe/pt-br/area-conhecimento/posgraduacao/repositorio-de-arquivos/folderpos06-ingles-conversao.pdf

[^13]: https://www.gov.br/inpe/pt-br/area-conhecimento/posgraduacao/cap

[^14]: https://cran.r-project.org/web/packages/RANSAC/RANSAC.pdf

[^15]: https://www.kaggle.com/discussions/general/536196

[^16]: https://www.youtube.com/watch?v=L9gTuNLglxs

[^17]: https://pmc.ncbi.nlm.nih.gov/articles/PMC9041793/

[^18]: https://lean-lang.org

[^19]: https://leanprover.github.io/theorem_proving_in_lean/introduction.html

[^20]: https://arxiv.org/abs/2508.15878

[^21]: https://leandojo.org

[^22]: https://www.karlin.mff.cuni.cz/~krajicek/becca-22-X-21.pptx

[^23]: https://openaccess.thecvf.com/content/CVPR2022/papers/Barath_Learning_To_Find_Good_Models_in_RANSAC_CVPR_2022_paper.pdf

[^24]: https://www.gov.br/inpe/en/area-knowledge/postgraduate/ast/copy_of_applications/application

[^25]: https://www.inpe.br/posgraduacao/en/registration.php

[^26]: https://www.youtube.com/watch?v=Mgsv89UiRP0

[^27]: https://www.esensing.org/docs/pos-doc-announcement-esensing-agriculture.pdf

[^28]: https://neptune.ai/blog/select-model-for-time-series-prediction-task

