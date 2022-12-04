"""
Author: Shengge Tong (shengge.tong22@imperial.ac.uk)
Date: Nov,2022
Description: Using subprocess to run a R script
"""

import subprocess

#Python will first run a shell, and then interpret the entire string with that shell
p = subprocess.call("Rscript fmr.R", shell=True)

if p == 0:
	print("The run was successful!")
else:
	print("Failed!")

