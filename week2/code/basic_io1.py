#!/usr/bin/env python3

"""
Script to align two sequences after taking an input from user.
If no input is provided the script will run with default arguements.
"""

__author__ = 'Shengge Tong (shengge.tong22@imperial.ac.uk)'
__version__ = '0.0.1'
__license__ = 'None'

#############################
# FILE INPUT
#############################
# Open a file for reading
f = open('../sandbox/test.txt', 'r')

"""
use "implicit" for loop:
if the object is a file, python will cycle over lines
"""
for line in f:
    print(line)

# close the file
f.close()


"""
Same example, skip blank lines
"""
f = open('../sandbox/test.txt', 'r')
for line in f:
    if len(line.strip()) > 0:
        print(line)

f.close()


#############################
# FILE INPUT
#############################
# Open a file for reading
with open('../sandbox/test.txt', 'r') as f:
    # use "implicit" for loop:
    # if the object is a file, python will cycle over lines
    for line in f:
        print(line)
        
"""
Once you drop out of the with, the file is automatically closed
"""
 
# Same example, skip blank lines
with open('../sandbox/test.txt', 'r') as f:
    for line in f:
        if len(line.strip()) > 0:
            print(line)
