#!/bin/bash
# Author: shengge.tong22@imperial.ac.uk
# Script: csvtospace.sh
# Description: substitute the commas in the file with spaces
# Save the output into a a space separated .txt file
# Arguements: 1 -> txt delimited file
# Date: Oct.2022

if [ -z "$1" ] #check if the input is empty
then
	echo "Please enter the file name"
else
	echo "Creating a space separated version of $1 ..."
	cat $1 | tr -s "," " " >> ${1%.csv}.txt
	echo "done!"
	exit
fi
