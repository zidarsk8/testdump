TEX = pdflatex -shell-escape -interaction=nonstopmode -file-line-error
PRE =  (TEX) -ini -job-name="preamble" "&pdflatex preamble.tex\dump"
BIB = bibtex

.PHONY: all view
	
all : diploma.pdf
	
view :
	open diploma.pdf
	
diploma.pdf : diploma.tex
	$(TEX) diploma.tex
	$(BIB) diploma
	$(TEX) diploma.tex
	$(TEX) diploma.tex
	rm *.aux
	rm diploma.log diploma.out diploma.toc
	
diploma.bbl diploma.blg : diploma.bib diploma.aux
	$(BIB) diploma
	
diploma.aux : diploma.tex
	$(TEX) diploma.tex
	
diploma.bib : diploma.tex
	$(TEX) diploma.tex
	
clean :
	rm -f *.aux
	rm -f diploma.log diploma.out diploma.toc diploma.pdf diploma.b*

