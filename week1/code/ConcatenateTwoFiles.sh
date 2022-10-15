#!/bin/bash
# Author: shengge.tong22@imperial.ac.uk
# Script: ConcatenateTwoFiles.sh
# Description: Merge files
# Saves the output into a new file
# Date: Oct 2022

if [ -z "$1" ] || [ -z "$2" ]
then 
	echo "Please enter 2 file names to be merged"

elif [ -z "$3" ]
then 
	echo "Please enter the output file name"
else
	cat $1 > $3
	cat $2 >> $3
	echo "Merged File is"
	cat $3
fi
exit
