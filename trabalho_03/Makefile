# Makefile for Computational Statistics — Assignment 03


VENV        = references/or_mcs/.venv
PYTHON_VENV = $(VENV)/bin/python
# Fallback: use uv for problems 1 & 2 (no arch dependency)
PYTHON_UV   = uv run --with numpy --with scipy --with matplotlib python3
TYPST       = typst compile

FIGURES_DIR = figures
SRC_DIR     = src

FIGURES = \
  $(FIGURES_DIR)/problem1_sampling.svg \
  $(FIGURES_DIR)/problem1_std_comparison.svg \
  $(FIGURES_DIR)/problem2_clt.svg \
  $(FIGURES_DIR)/problem2_ci.svg \
  $(FIGURES_DIR)/problem3_mcs_shines.svg \
  $(FIGURES_DIR)/problem3_mcs_fails.svg

.PHONY: all figures report clean

all: figures report

# ── Figures ──────────────────────────────────────────────────────────────────

figures: $(FIGURES)

$(FIGURES_DIR)/problem1_sampling.svg $(FIGURES_DIR)/problem1_std_comparison.svg: \
    $(SRC_DIR)/problem1.py
	mkdir -p $(FIGURES_DIR)
	$(PYTHON_UV) $<

$(FIGURES_DIR)/problem2_clt.svg $(FIGURES_DIR)/problem2_ci.svg: \
    $(SRC_DIR)/problem2.py
	mkdir -p $(FIGURES_DIR)
	$(PYTHON_UV) $<

$(FIGURES_DIR)/problem3_mcs_shines.svg $(FIGURES_DIR)/problem3_mcs_fails.svg: \
    $(SRC_DIR)/problem3.py
	mkdir -p $(FIGURES_DIR)
	$(PYTHON_VENV) $<

# ── Report ────────────────────────────────────────────────────────────────────

report: report.pdf

report.pdf: report.typ references.bib $(FIGURES)
	$(TYPST) $<

# ── Helpers ───────────────────────────────────────────────────────────────────

clean:
	rm -rf $(FIGURES_DIR) report.pdf
