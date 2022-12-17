"""
Author: Shengge Tong (shengge.tong22@imperial.ac.uk)
Date: Nov,2022
Description: Profiling to locate the sections of your code where speed bottlenecks exist.
"""

def my_squares(iters):
    """
    Des:
	A function to calculate square
    Arg:
	iters
    Return
	result
    """
    out = []
    for i in range(iters):
        out.append(i ** 2)
    return out

def my_join(iters, string):
    """
    Des:
	A function for join
    Arg:
	iters, string
    Return
	out
    """ 
    out = ''
    for i in range(iters):
        out += string.join(", ")
    return out

def run_my_funcs(x,y):
    """
    Des:
	A function to run functions
    Arg:
	x,y
    Return
	0
    """
    print(x,y)
    my_squares(x)
    my_join(x,y)
    return 0

run_my_funcs(10000000,"My string")
