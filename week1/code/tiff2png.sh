#!/bin/bash
# Author: shengge.tong22@imperial.ac.uk
# Script: tiff2png.sh
# Description: change the file to png
#
# Saves the output into a .png file
# Arguments: 1 -> tab delimited file
# Date: Oct 2022

if [ -z "$1" ] #If no input file name 
then
	echo "Please enter a file name"
elif [ ! -s $1 ]
then
	echo "The file does not exist"
else #There is an input file name
for f in *.tif; 
    do  
        echo "Converting $f"; 
        convert "$f"  "$(basename "$f" .tif).png"; 
    done
fi
