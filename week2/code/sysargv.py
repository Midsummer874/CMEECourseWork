#!/usr/bin/env python3
# Filename: sysargv.py
"""Function to sysargv"""
#docstrings are considered part of the running code (normal comments are
#stripped). Hence, you can access your docstrings at run time.

__author__ = 'Shengge Tong (shengge.tong22@imperial.ac.uk)'
__version__ = '0.0.1'

import sys
"""
    Des:
    	The function for sysargv
    Arg:
	argv
    Return:
    	0
    """
print("This is the name of the script: ", sys.argv[0])
print("Number of arguments: ", len(sys.argv))
print("The arguments are: " , str(sys.argv))
