---
trigger: always_on
---


# GEMINI.md - INPE PhD Study Plan Instructions

## Core Project Goal
**Primary Output**: Generate a complete Study Plan ("Plano de Estudos") document for INPE CAP PhD application in Applied Computing. Final deliverable: `plano_estudos.tex` (2-4 pages, LaTeX) + compiled PDF, strictly following edital requirements.[file:1]

**Theme & Ideas Source**: Base ALL content on `option_mcs_ransac.md`. Read it first—extract problem, relevance to INPE (satellite systems, AOCS, space computing), challenges, methods (MCS-RANSAC focus), expected results, and bibliography. Align with INPE's Earth observation, satellite control, computational modeling.

## Strict Structure (Enforce Always)
Produce ONLY this 4-section format in LaTeX:

1. **Enunciado do Problema** (Problem Statement): Research problem from `option_mcs_ransac.md` + INPE relevance (space/satellite applications).
2. **Desafios e Métodos** (Challenges & Methods): Key challenges + existing methods + 5-10 cited references.
3. **Resultados Esperados** (Expected Results): Concrete outputs + benefits to INPE missions.
4. **Bibliografia** (Bibliography): 15-25 references (IEEE/ABNT style), prioritize satellite/AOCS papers.

**Length**: 2-4 pages (concise). Portuguese language. Professional academic tone.

## Workflow Enforcement
```
1. Analyze option_mcs_ransac.md → Extract core ideas
2. Map to INPE domains (AOCS, satellite attitude control, orbit determination)
3. Generate content per section above
4. Format as plano_estudos.tex (use article class, 12pt, a4paper)
5. **MANDATORY**: Run Rust LaTeX formatter BEFORE pdflatex: `cargo run --bin latex-fmt plano_estudos.tex`
6. Compile: `pdflatex -synctex=1 -interaction=nonstopmode plano_estudos.tex`
7. Output: plano_estudos.pdf (verify 2-4 pages)
```

## LaTeX Standards
- Use `article` document class, Portuguese babel
- Sections: `\section{Enunciado do Problema}`, etc.
- **ALWAYS** format with Rust tool first: `cargo run --bin latex-fmt` (enforce this step)
- Bibliography: `bibtex` or manual `\begin{thebibliography}`
- No colors, minimal packages (geometry, hyperref, biblatex optional)

## Quality Rules
- Cite INPE-relevant works (CBERS, AOCS anomaly detection, RANSAC in orbit estimation)
- Technical depth: Algorithms, math (Julia/Python pseudocode if relevant to your expertise)
- No fluff—direct, evidence-based
- Suggest 2-3 potential advisors from INPE CAP faculty list
- Version control: Commit as `v1-plano_estudos.tex` → `v2-...`

## NEVER Do
- Deviate from 4-section structure
- Skip Rust formatter step
- Generate >4 pages or <2 pages
- Use English (Portuguese only)
- Ignore `option_mcs_ransac.md` content

**Success Metric**: `plano_estudos.pdf` ready for INPE online submission system.
