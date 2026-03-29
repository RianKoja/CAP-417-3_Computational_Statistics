.PHONY: compile clean all

# Default target
all: compile

# Compile the LaTeX document
compile:
	@echo "Creating cache directory..."
	@mkdir -p .cache/tex
	@echo "Compiling plano_estudos.tex..."
	@pdflatex -output-directory=.cache/tex -interaction=nonstopmode plano_estudos.tex
	@echo "Running second pass for cross-references..."
	@pdflatex -output-directory=.cache/tex -interaction=nonstopmode plano_estudos.tex
	@echo "Copying PDF to project root..."
	@cp .cache/tex/plano_estudos.pdf .
	@echo "Done! PDF generated at plano_estudos.pdf"

# Clean auxiliary files
clean:
	@echo "Cleaning auxiliary files..."
	@rm -rf .cache/tex
	@rm -f plano_estudos.aux plano_estudos.fdb_latexmk plano_estudos.fls
	@rm -f plano_estudos.log plano_estudos.out plano_estudos.synctex.gz plano_estudos.synctex.gz(busy)
	@rm -f plano_estudos.pdf
	@echo "Clean complete!"
