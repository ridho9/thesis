all: clean install

install:
	mkdir -p output
	mkdir -p build
	latexmk -pdf -bibtex -outdir=../build -cd src/thesis.tex
	# latexmk -xelatex -bibtex -outdir=../build -cd src/thesis.tex
	cp build/thesis.pdf thesis.pdf

clean:
	rm -f output/* build/*
	find . -iname "*~" -exec rm '{}' ';'
