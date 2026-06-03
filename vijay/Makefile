.PHONY: all clean check plots

all: computational_statistics_solutions.pdf

computational_statistics_solutions.pdf: main.typ plots check
	typst compile main.typ computational_statistics_solutions.pdf

plots: scripts/generate_plots.py
	uv run scripts/generate_plots.py

check: scripts/sanity_check.py
	uv run scripts/sanity_check.py

clean:
	$(RM) assets/*.png computational_statistics_solutions.pdf
