# Makefile for Computational Statistics — Assignment 03

VENV        = references/or_mcs/.venv
PYTHON_VENV = $(VENV)/bin/python
# Fallback: use uv for problems 1 & 2 (no arch dependency)
PYTHON_UV   = uv run --with numpy --with scipy --with matplotlib python3
TYPST       = typst compile

FIGURES_DIR = figures
SRC_DIR     = src

# ── Figure discovery ─────────────────────────────────────────────────────────
# Stamp files are the authoritative "did this script run?" signal — they avoid
# the GNU Make multi-target footgun (two outputs, one recipe runs twice) and
# work correctly on clean builds.  FIGURE_FILES then auto-discovers every image
# present at parse time so the report also rebuilds on manual additions.

STAMPS = $(FIGURES_DIR)/.stamp.p1 \
         $(FIGURES_DIR)/.stamp.p2 \
         $(FIGURES_DIR)/.stamp.p3

IMG_EXTS    := svg png jpg jpeg gif pdf
FIGURE_FILES = $(foreach ext,$(IMG_EXTS),$(wildcard $(FIGURES_DIR)/*.$(ext)))

.PHONY: all figures report clean watch

all: figures report

# ── Figures ──────────────────────────────────────────────────────────────────

figures: $(STAMPS)

$(FIGURES_DIR)/.stamp.p1: $(SRC_DIR)/problem1.py
	mkdir -p $(FIGURES_DIR)
	$(PYTHON_UV) $<
	@touch $@

$(FIGURES_DIR)/.stamp.p2: $(SRC_DIR)/problem2.py
	mkdir -p $(FIGURES_DIR)
	$(PYTHON_UV) $<
	@touch $@

$(FIGURES_DIR)/.stamp.p3: $(SRC_DIR)/problem3.py
	mkdir -p $(FIGURES_DIR)
	$(PYTHON_VENV) $<
	@touch $@

# ── Report ────────────────────────────────────────────────────────────────────

report: report.pdf

# Stamps guarantee scripts ran; FIGURE_FILES catches manual additions;
# report.typ and references.bib trigger a rebuild whenever they change.
report.pdf: report.typ references.bib $(STAMPS) $(FIGURE_FILES)
	$(TYPST) $<

# ── Watch ────────────────────────────────────────────────────────────────────
# Watches only source files to avoid a feedback loop with generated outputs.
# Make handles the dependency graph — watchexec just re-invokes it on changes.

watch:
	watchexec \
	    -w $(SRC_DIR) \
	    -w report.typ \
	    -w references.bib \
	    -e py,typ,bib \
	    -- make all

# ── Helpers ───────────────────────────────────────────────────────────────────

clean:
	rm -rf $(FIGURES_DIR) report.pdf
