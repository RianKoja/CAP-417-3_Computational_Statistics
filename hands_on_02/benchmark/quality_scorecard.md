# Quality Scorecard — Agent Comparison

This document evaluates the code quality and technical implementation of the solutions produced by Claude Code and Gemini CLI for Hands-on 02 — CAP 417 — Part C.

## Scoring Summary

| Criterion | Claude Code | Gemini CLI |
|-----------|-------------|------------|
| Readability and Structure | 5 | 5 |
| Reproducibility (Seeding) | 5 | 4 |
| Plot Quality | 5 | 5 |
| Output File Organization | 5 | 5 |
| Correctness of Noise Generation | 5 | 4 |
| **Total (out of 25)** | **25** | **23** |

---

## Detailed Assessment

### 1. Readability and Structure
- **Claude Code (5/5):** Excellent code organization with clear section headers, concise comments, and modular function definitions. Use of `rng` object is idiomatic for modern NumPy.
- **Gemini CLI (5/5):** Very well-structured script. Clearly marked parts (2.1, 2.2, 2.3) and helpful docstrings for functions.

### 2. Reproducibility (Seeding)
- **Claude Code (5/5):** Uses `np.random.default_rng(GLOBAL_SEED)`, which is the recommended modern approach. Individual realizations use derived seeds via hashing, ensuring independent but reproducible series.
- **Gemini CLI (4/5):** Uses the legacy `np.random.seed()` approach. While reproducible, it is less robust in complex multi-threaded or multi-module environments compared to modern Generator objects.

### 3. Plot Quality
- **Claude Code (5/5):** Professional plots with appropriate labels, legends, and sizing. Complies with dark background requirement for the CFP plot. ACF plots are clear and informative.
- **Gemini CLI (5/5):** High-quality plots. Includes an additional "moments" table figure which is a nice touch. CFP plot is well-formatted and aesthetically pleasing.

### 4. Output File Organization
- **Claude Code (5/5):** Strictly follows the requested structure (`figures/` and `results/` subdirectories).
- **Gemini CLI (5/5):** Correctly organizes outputs into the specified directories.

### 5. Correctness of Frequency-Domain Noise Generation
- **Claude Code (5/5):** Uses `np.fft.rfft` and `np.fft.irfft`, which are optimized for real-valued signals. Handling of the DC component (freq=0) by leaving it unchanged is a valid approach for colored noise generation.
- **Gemini CLI (4/5):** Uses `np.fft.fft` and `np.fft.ifft` (taking the real part), which is slightly less efficient for real signals. Sets the DC component to 0 for $\beta > 0$, which effectively removes the mean before normalization. While technically correct, `rfft` is more idiomatic for this task.
