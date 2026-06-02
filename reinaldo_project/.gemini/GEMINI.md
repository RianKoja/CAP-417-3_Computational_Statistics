## Purpose

This repository produces a CAP 417 final presentation in Typst/Touying about Louis Bachelier, generative AI, and computational statistics. The remaining work is to finish the reproducible research pipeline around the slides: data acquisition, preprocessing, statistical analysis, figure generation, and build automation.

The primary stack is:

- Python for all data work, scraping, analysis, and figure generation.
- Typst + Touying for slides.
- Bash/Make for orchestration.
- Optional Docker for reproducible local execution.

Do **not** introduce Julia. Do **not** introduce GitLab-specific tooling. Prefer plain Python CLIs, standard Make recipes, and tools that run locally or in CI without vendor lock-in.

---

## Repository goals

The agent should complete the missing production code so that the repository supports the following workflow:

1. Acquire or refresh raw data.
2. Clean and normalize the dataset.
3. Compute analysis tables and derived metrics.
4. Generate plots for the presentation.
5. Compile the Typst slides to PDF.
6. Package a clean reproducible bundle.

The result should be a repository where `make build` regenerates the presentation from source data and scripts.

---

## Expected directory structure

Use or migrate toward this structure:

```text
.
├── main.typ
├── theme.typ
├── bachelier_lexicon.typ
├── bachelier_ai_response.typ
├── hf_analysis.typ
├── refs.typ
├── Makefile
├── CLAUDE.md
├── requirements.txt
├── requirements-dev.txt
├── parameters.toml
├── data/
│   ├── raw/
│   ├── interim/
│   └── processed/
├── output/
│   ├── figures/
│   ├── tables/
│   └── logs/
├── scripts/
│   ├── fetch_data.py
│   ├── process_raw_data.py
│   ├── generate_window_plots.py
│   ├── generate_tables.py
│   ├── build_features.py
│   ├── fit_garch.py
│   ├── fit_ml_models.py
│   └── utils/
│       ├── io.py
│       ├── plotting.py
│       └── config.py
└── tests/
```

If the current tree differs, adapt incrementally rather than rewriting everything at once.

---

## What the agent should produce

### 1. Data acquisition code

Implement Python scripts for acquiring financial data suitable for the presentation.

Preferred design:

- `scripts/fetch_data.py`
- CLI-friendly, e.g.:

```bash
python scripts/fetch_data.py --symbol SPY --interval 5min --start 2024-01-01 --end 2024-12-31
```

Possible sources:

- Official or documented APIs.
- Public finance APIs with clear usage constraints.
- Vendor export files already present in `data/raw/`.

Rules:

- Save raw files into `data/raw/`.
- Never overwrite silently; use deterministic filenames.
- Log source, symbol, date range, interval, and timestamp of retrieval.
- If scraping is required, prefer robust HTTP requests over browser automation.
- Only use browser automation if the source cannot reasonably be accessed otherwise.
- Respect robots.txt, rate limits, and terms of service.

If no public source is stable enough for intraday historical data, the agent should support a manual-drop workflow:

- user places CSV/Parquet files in `data/raw/`
- pipeline discovers them automatically
- processing scripts validate schema and fail loudly on mismatch

### 2. Data preprocessing

Implement:

- `scripts/process_raw_data.py`

Responsibilities:

- Load raw intraday bars.
- Standardize schema to canonical columns such as:
  - `timestamp`
  - `symbol`
  - `open`
  - `high`
  - `low`
  - `close`
  - `volume`
- Normalize timezone explicitly.
- Sort, deduplicate, and validate monotonic timestamps.
- Handle missing bars according to explicit rules.
- Write cleaned datasets to `data/processed/`.
- Produce a compact data-quality report in `output/logs/`.

The script should exit nonzero on:

- missing required columns
- unparseable timestamps
- duplicate timestamps after normalization
- empty output after filtering

### 3. Statistical analysis code

Implement production scripts, not notebooks first.

Required scripts:

- `scripts/generate_tables.py`
- `scripts/generate_window_plots.py`
- `scripts/build_features.py`
- `scripts/fit_garch.py`
- `scripts/fit_ml_models.py`

Suggested responsibilities:

- `generate_tables.py`
  - descriptive statistics for returns
  - normality diagnostics summary
  - Ljung–Box results
  - volatility summary
  - export CSV tables to `output/tables/`

- `generate_window_plots.py`
  - return time series
  - histogram / KDE
  - QQ-plot
  - ACF for returns and squared returns
  - rolling volatility plots
  - save PNG/PDF figures to `output/figures/`

- `build_features.py`
  - create lagged volatility, absolute returns, time-of-day features, volume features
  - save model-ready dataset to `data/interim/` or `data/processed/`

- `fit_garch.py`
  - fit baseline conditional volatility models
  - save parameter tables and forecast outputs

- `fit_ml_models.py`
  - fit baseline ML predictors for volatility or risk
  - compare against naive benchmark
  - save metrics tables and optional feature importance chart

Use scripts as importable modules with a `main()` entrypoint so they can be tested.

### 4. Typst integration

The analysis scripts should generate assets that Typst can include directly.

Conventions:

- figures in `output/figures/`
- tables in `output/tables/`
- slide PDF target in repository root or `output/`

Prefer stable filenames such as:

- `output/figures/returns_ts.png`
- `output/figures/ret_acf.png`
- `output/figures/ret2_acf.png`
- `output/figures/qqplot_returns.png`
- `output/tables/descriptive_stats.csv`
- `output/tables/ljung_box.csv`
- `output/tables/garch_summary.csv`
- `output/tables/ml_metrics.csv`

The Typst slides should refer only to generated artifacts with predictable names.

---

## Coding rules

### Python rules

- Target Python 3.11+.
- Use `pathlib` instead of string paths.
- Use type hints where practical.
- Use `argparse` or `typer` for CLI entrypoints.
- Use `pandas`, `numpy`, `scipy`, `statsmodels`, `scikit-learn`, `matplotlib`, `seaborn`, and `arch` if needed.
- Prefer plain scripts over notebooks for core pipeline logic.
- Keep notebooks optional and secondary.
- Use logging, not ad hoc print spam.
- Fail loudly on schema or data integrity issues.

### Style and quality

Use:

- `ruff` for linting
- `black` for formatting
- `pytest` for tests
- optional `mypy` if type coverage is not too painful

### Plotting rules

- Produce publication-quality figures sized for slides.
- Use readable font sizes and tight layouts.
- Avoid interactive-only outputs for the build pipeline.
- Save deterministic files with explicit DPI.

---

## Makefile requirements

The Makefile should orchestrate the entire pipeline and remain readable.

Principles:

- No Julia references.
- No GitLab references.
- No CI-vendor-specific local runner requirements.
- Keep targets composable and deterministic.
- Use Python entrypoints directly.

Expected targets:

- `all`
- `build`
- `build-typst`
- `preprocess`
- `fetch-data`
- `analyze`
- `figures`
- `tables`
- `test`
- `lint`
- `format`
- `install`
- `clean`
- `bundle`
- `watch`
- `watch-typst`
- `watch-data`
- `watch-python`
- `pre-commit`
- `pre-push`

Optional targets:

- `docker-build`
- `docker-run`

---

## Updated Makefile

Use the following Makefile as the new baseline and extend it only if needed:

```make
# Definitions
HASH := $(shell git rev-parse HEAD)
BUNDLE := bundle-$(HASH).tar.gz
STAGING := /tmp/repo_staging
DOC_CODE := ZBCN-TSP-1001
PYTHON ?= python3
VENV := .venv
BIN := $(VENV)/bin
PIP := $(BIN)/pip
RUFF := $(BIN)/ruff
BLACK := $(BIN)/black
PYTEST := $(BIN)/pytest
WATCH := $(BIN)/watchfiles
TYPST ?= typst
TYPSTYLE ?= typstyle

.PHONY: all build build-typst bundle clean fetch-data force-push format format-python format-typst \
	install lint pre-commit pre-push preprocess analyze figures tables test watch watch-data watch-python watch-typst

all: build

force-push:
	git lfs push origin HEAD:$(shell git rev-parse --abbrev-ref HEAD)
	git push --no-verify

bundle:
	git submodule update --init --recursive
	@if [ -n "$$(git status --porcelain)" ]; then \
		echo "Error: Repository or submodules are dirty. Please commit changes before bundling."; \
		exit 1; \
	fi
	rm -rf $(STAGING) && mkdir -p $(STAGING)
	rsync -a --exclude='.git' --filter=':- .gitignore' ./ $(STAGING)/
	tar czf $(BUNDLE) -C $(STAGING) .
	rm -rf $(STAGING)

build: preprocess analyze build-typst

build-typst:
	$(TYPST) compile main.typ $(DOC_CODE).pdf --font-path inpe-cbers6-report/fonts

fetch-data:
	$(BIN)/python scripts/fetch_data.py

preprocess:
	$(BIN)/python scripts/process_raw_data.py

analyze: tables figures

tables:
	$(BIN)/python scripts/generate_tables.py
	$(BIN)/python scripts/fit_garch.py
	$(BIN)/python scripts/fit_ml_models.py

figures:
	$(BIN)/python scripts/generate_window_plots.py

format: format-typst format-python

format-typst:
	find . -name "*.typ" -not -path "./.venv/*" -print0 | xargs -0 $(TYPSTYLE) --inplace

format-python:
	$(BLACK) scripts tests
	$(RUFF) check --fix scripts tests

lint:
	$(RUFF) check scripts tests
	$(BLACK) --check scripts tests

test:
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

pre-commit: install format lint test
	@git diff --exit-code || (echo "Error: formatting or generated changes detected." && exit 1)

pre-push: install test

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
	rm -rf $(VENV) .pytest_cache .ruff_cache .mypy_cache output/logs/* $(DOC_CODE).pdf bundle*.tar.gz
```

Notes on fixes relative to the old Makefile:

- Replaced all Julia recipes with Python entrypoints.
- Removed `gitlab-ci-local` and `.gitlab-ci-local` references.
- Removed `.julia_depot` logic.
- Replaced `format-julia` with `format-python`.
- Replaced Julia watchers with Python watchers.
- Added Python virtualenv bootstrap.
- Kept `git lfs` force-push recipe only because it is generic Git usage, not GitLab-specific.
- Normalized target names and dependencies around a Python analysis pipeline.

---

## Testing expectations

Add tests for at least:

- schema validation of raw input
- return computation
- no duplicate timestamps after normalization
- output artifact existence for analysis scripts
- CLI argument parsing for main scripts where practical

Tests should use tiny fixture datasets under `tests/fixtures/`.

---

## Data and scraping guidance

If scraping or downloading data is needed, follow this priority order:

1. Use direct file/API download.
2. Use documented SDK or HTTP endpoint.
3. Use HTML scraping with `requests` + `pandas.read_html` or `BeautifulSoup`.
4. Use browser automation only as a last resort.

Every downloader should:

- set a user agent
- retry transient failures with backoff
- validate response content type
- save raw payload unchanged when feasible
- write a sidecar metadata file if useful

For market data, prefer reproducibility over cleverness. A robust manual-ingest path is better than a brittle unofficial scraper.

---

## Deliverables expected from the agent

The agent should generate or update:

- `Makefile`
- `requirements.txt`
- `requirements-dev.txt`
- Python scripts under `scripts/`
- tests under `tests/`
- minimal README notes if needed for usage
- any Typst include updates needed to point at generated tables/figures

The agent should not leave placeholder function bodies once it starts implementing code.

---

## Definition of done

The work is done when all of the following are true:

- `make install` succeeds on a normal Unix-like environment with Python 3.11+.
- `make preprocess` runs successfully on available raw data.
- `make analyze` produces figures and tables in deterministic locations.
- `make build-typst` compiles the presentation.
- `make build` runs end-to-end.
- `make test`, `make lint`, and `make format` are meaningful and pass.
- The pipeline uses Python only for the analysis and data-processing layer.

---

## Agent behavior guidance

When modifying this repository:

- Prefer small, reviewable commits.
- Do not add unnecessary frameworks.
- Do not add notebook-only logic for core steps.
- Do not hide failures behind broad exception handlers.
- Do not fabricate data when a source is missing; instead, create a validated manual-ingest path.
- Keep filenames, target names, and output conventions stable once introduced.
- Preserve reproducibility and explicitness over convenience.
