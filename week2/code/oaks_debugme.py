#!/usr/bin/env python3
# Filename: oaks_debugme.py
"""Function to oaks_debugme.py"""
#docstrings are considered part of the running code (normal comments are
#stripped). Hence, you can access your docstrings at run time.

__author__ = 'Shengge Tong (shengge.tong22@imperial.ac.uk)'
__version__ = '0.0.1'

import csv
import sys

#Define function
def is_an_oak(name):
    """ Returns True if name is starts with 'quercus' 
    >>> is_an_oak("Quercus")
    True
    >>> is_an_oak("Fraxinus")
    False
    >>> is_an_oak("Pinus")
    False
    >>> is_an_oak("Quercuss")
    False
    >>> is_an_oak("Quercuss Quercus")
    False
    >>> is_an_oak("quercus")
    True
    >>> is_an_oak("quercus petraea")
    True
    >>> is_an_oak('QuercusPetraea')
    True
    """
    return name.lower().startswith('quercs')

def main(argv): 
"""
    Des:
    	The main function to run all the functions
    Arg:
	argv
    Return:
    	0
    """
    f = open('../data/TestOaksData.csv','r')
    g = open('../data/JustOaksData.csv','w')
    taxa = csv.reader(f)
    csvwrite = csv.writer(g)
    oaks = set()
    for row in taxa:
        print(row)
        print ("The genus is: ") 
        print(row[0] + '\n')
        if is_an_oak(row[0]):
            print('FOUND AN OAK!\n')
            csvwrite.writerow([row[0], row[1]])    

    return 0
    
if (__name__ == "__main__"):
    status = main(sys.argv)
