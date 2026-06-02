# Definitions
STAGING := /tmp/repo_staging
DOC_CODE := rian_bachelier_presentation
PYTHON ?= python3
VENV := .venv
BIN := $(VENV)/bin
PIP := $(BIN)/pip
RUFF := $(BIN)/ruff
PYTEST := $(BIN)/pytest
TYPST ?= typst
TYPSTYLE ?= typstyle

.PHONY: all build build-typst bundle clean fetch-data format format-python format-typst \
	install lint preprocess analyze figures tables test watch watch-data watch-python watch-typst

all: build

build: preprocess analyze build-typst

build-typst:
	$(TYPST) compile main.typ $(DOC_CODE).pdf --font-path inpe-cbers6-report/fonts

fetch-data: install
	$(BIN)/python scripts/fetch_data.py

preprocess: install
	$(BIN)/python scripts/process_raw_data.py

analyze: tables figures

tables: install
	$(BIN)/python scripts/generate_tables.py
	$(BIN)/python scripts/fit_garch.py
	$(BIN)/python scripts/fit_ml_models.py

figures: install
	$(BIN)/python scripts/generate_window_plots.py

format: format-typst format-python

format-typst:
	find . -name "*.typ" -not -path "./.venv/*" -print0 | xargs -0 $(TYPSTYLE) --inplace

format-python: install
	$(RUFF) format scripts tests
	$(RUFF) check --fix scripts tests

lint: install
	$(RUFF) check scripts tests
	$(RUFF) format --check scripts tests

test: install
	$(PYTEST)

$(VENV)/bin/activate: requirements.txt requirements-dev.txt
	$(PYTHON) -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt -r requirements-dev.txt
	touch $(VENV)/bin/activate

install: $(VENV)/bin/activate
	@command -v $(TYPST) >/dev/null 2>&1 || echo "Warning: typst not found in PATH"
	@command -v $(TYPSTYLE) >/dev/null 2>&1 || echo "Warning: typstyle not found in PATH"
	@command -v watchexec >/dev/null 2>&1 || echo "Warning: watchexec not found in PATH; watch targets will be unavailable"

# Continuously re-run on file changes, keeping outputs up to date.
watch:
	@echo "Starting auto-updates for Python scripts, data processing, and Typst compiler..."
	@make -j3 watch-typst watch-python watch-data

watch-typst:
	@echo "Watching Typst files for changes..."
	watchexec -n -e typ -- $(MAKE) build-typst

watch-python:
	@echo "Watching Python scripts for changes..."
	watchexec -n \
		-w scripts \
		-w parameters.toml \
		-e py,toml \
		-- $(MAKE) analyze

watch-data:
	@echo "Watching raw data and processing scripts for changes..."
	watchexec -n \
		-w data \
		-w scripts/process_raw_data.py \
		-e csv,parquet,py \
		-- $(MAKE) preprocess analyze

clean:
	rm -rf $(VENV) .pytest_cache .ruff_cache $(DOC_CODE).pdf bundle*.tar.gz
	mkdir -p output/logs output/figures output/tables