.PHONY: all figures pdf clean

TYPST = typst
SCRIPTS_DIR = scripts
FIGURES_DIR = figures

all: figures pdf

figures:
	@echo "Running script 01: visualization..."
	uv run $(SCRIPTS_DIR)/01_visualization.py
	@echo "Running script 02: estimation..."
	uv run $(SCRIPTS_DIR)/02_estimation.py
	@echo "Running script 03: noise..."
	uv run $(SCRIPTS_DIR)/03_noise.py
	@echo "Running script 04: stochastic..."
	uv run $(SCRIPTS_DIR)/04_stochastic.py
	@echo "Running script 05: real data (GARCH)..."
	uv run $(SCRIPTS_DIR)/05_real_data.py
	@echo "All figures generated."

pdf:
	@echo "Compiling Typst document..."
	$(TYPST) compile main.typ
	@echo "Done! PDF at main.pdf"

clean:
	@rm -f $(FIGURES_DIR)/0*.svg $(FIGURES_DIR)/0*.png
	@rm -f sections/*.csv
	@rm -f main.pdf
	@echo "Clean complete."
