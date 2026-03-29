PYTHON  := uv run python
TYPST   := typst
REPORT  := report/main.typ
PDF     := report/main.pdf
PLOTS   := outputs/plots/part1_matrix.png \
           outputs/plots/part2_distribution.png \
           outputs/plots/part2_percentiles.png \
           outputs/plots/pi_convergence.png
METRICS := report/metrics.typ

.PHONY: all plots report clean bundle

all: report

# Run all Python analysis scripts → produces plots + metrics.typ
$(PLOTS) $(METRICS): scripts/run_all.py scripts/part1_analysis.py \
                     scripts/part2_analysis.py scripts/part3_analysis.py \
                     wrappers.py
	PYTHONPATH=. $(PYTHON) scripts/run_all.py

plots: $(PLOTS) $(METRICS)

# Compile the Typst report to PDF
$(PDF): $(REPORT) report/metrics.typ $(PLOTS)
	$(TYPST) compile --root . $(REPORT) $(PDF)

report: $(PDF)

clean:
	rm -f $(PDF) $(METRICS) $(PLOTS)

bundle: 
	git bundle create repo.bundle HEAD