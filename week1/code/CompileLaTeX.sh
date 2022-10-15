#!/bin/bash
# Author: shengge.tong22@imperial.ac.uk
# Script: CompileLaTeX.sh
# Description: change the file to png
# Switch the .tex file to .pdf
# Arguments: 1 -> tab delimited file
# Date: Oct 2022

new=${1%.tex}
pdflatex $new.tex
bibtex $new
pdflatex $new.tex
pdflatex $new.tex
evince $new.pdf &

## Cleanup
rm *.aux
rm *.log
rm *.bbl
rm *.blg

