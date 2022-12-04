#!/bin/bash
# Author: Shengge Tong(shengge.tong22@imperial.ac.uk)
# Script: run_MiniProject.sh
# Description: Run all the scripts
# Date: Dec 2022

# run data preprocessing and model fitting script
python3 -W ignore data_preprocess_and_models.py

# Compile the LaTex document
latexmk -pdf
mv MiniProject.pdf ../writeup
latexmk -C
rm *.bbl
echo -e "Run all the scripts successfully!"
