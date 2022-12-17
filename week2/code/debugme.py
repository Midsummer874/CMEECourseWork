#!/usr/bin/env python3
# Filename: debugme.py

"""Function to debugme"""
#docstrings are considered part of the running code (normal comments are
#stripped). Hence, you can access your docstrings at run time.
__author__ = 'Shengge Tong (shengge.tong22@imperial.ac.uk)'
__version__ = '0.0.1'
def buggyfunc(x):
    """
    Des:
    	To debug the function
    Arg:
    	x
    Return:
    	different bug results
    """
    y = x
    for i in range(x):
        try: 
            y = y-1
            z = x/y
        except ZeroDivisionError:
            print(f"The result of dividing a number by zero is undefined")
        except:
            print(f"This didn't work;{x = }; {y = }")
        else:
            print(f"OK; {x = }; {y = }, {z = };")
    return z

buggyfunc(20)
