.PHONY: clean download run

run:
	uv run python analysis.py
	typst compile report.typ

clean:
	rm -rf figs/*.svg

download:
	uv run python download_data.py