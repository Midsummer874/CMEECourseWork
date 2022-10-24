#!/usr/bin/env python3

"""Some functions exemplifying the use of control statements"""
#docstrings are considered part of the running code (normal comments are
#stripped). Hence, you can access your docstrings at run time.
__author__ = 'Shengge Tong (shengge.tong22@imperial.ac.uk)'
__version__ = '0.0.1'

from cgitb import reset
import sys

def foo_1(x): #Calculate the root
    return "The square root of %d is %d" % (x, x ** 0.5)

def foo_2(x,y): #Compare two numbers
    if x > y:
        return "The larger number is %d" % x
    return "The larger number is %d" % y

def foo_3(x, y, z): #Get the ascending order
    if x > y:
        tmp = y
        y = x
        x = tmp
    if y > z:
        tmp = z
        z = y
        y = tmp
    return "The ascending order is [%d,%d,%d]" % (x, y, z)

def foo_4(x): #Calculate the factorial
    result = 1
    for i in range(1, x + 1):
        result = result * i
    return "The result is %d" % result

def foo_5(x): # a recursive function that calculates the factorial of x
    if x == 1:
        return 1
    result = x * foo_5(x - 1)
    return "Factorial result is %d" %result
     
def foo_6(x): # Calculate the factorial of x in a different way; no if statement involved
    facto = 1
    while x >= 1:
        facto = facto * x
        x = x - 1
    return "Rusult is %d" % facto
 
def main(argv):  # running all the functions with specified input
  
    print(foo_1(4))
    print(foo_2(5,7))
    print(foo_3(5,2,6))
    print(foo_4(8)) 
    print(foo_5(8))
    print(foo_6(8))

    return 0 



if (__name__ == "__main__"):
    status = main(sys.argv)
    sys.exit(status)