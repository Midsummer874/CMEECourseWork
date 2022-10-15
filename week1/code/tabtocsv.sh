#!/bin/sh
# Author: shengge.tong22@imperial.ac.uk
# Script: tabtocsv.sh
# Description: substitute the tabs in the files with commas
#
# Saves the output into a .csv file
# Arguments: 1 -> tab delimited file
# Date: Oct 2022

if [ -z "$1" ] #If no input file name 
then
	echo "Please enter a file name"

elif [ ! -s $1 ]
then
	echo "The file does not exist"
else #There is an input file name
	echo "Creating a comma delimited version of $1 ..."
	cat $1 | tr -s "\t" "," >> $1.csv
	echo "Done!"
fi
exit

