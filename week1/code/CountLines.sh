#!/bin/bash
# Author: shengge.tong22@imperial.ac.uk
# Script: CountLines.sh
# Description: Count lines
# Arguments: none
# Date: Oct 2022

if [ -z "$1" ] #If no input file name 
then
	echo "Please enter a file name"

elif [ ! -s $1 ]
then
	echo "The file does not exist"
else #There is an input file name
	NumLines=`wc -l < $1`
	echo "The file $1 has $NumLines lines"
fi
exit
