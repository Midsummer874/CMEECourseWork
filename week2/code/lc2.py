#!/usr/bin/env python3
# Filename: lc2.py
"""Function to lc2"""
#docstrings are considered part of the running code (normal comments are
#stripped). Hence, you can access your docstrings at run time.

__author__ = 'Shengge Tong (shengge.tong22@imperial.ac.uk)'
__version__ = '0.0.1'

# Average UK Rainfall (mm) for 1910 by month
# http://www.metoffice.gov.uk/climate/uk/datasets
rainfall = (('JAN',111.4),
            ('FEB',126.1),
            ('MAR', 49.9),
            ('APR', 95.3),
            ('MAY', 71.8),
            ('JUN', 70.2),
            ('JUL', 97.1),
            ('AUG',140.2),
            ('SEP', 27.0),
            ('OCT', 89.4),
            ('NOV',128.4),
            ('DEC',142.2),
           )

# (1) Use a list comprehension to create a list of month,rainfall tuples where
# the amount of rain was greater than 100 mm.
"""
    Des:
    	An exercise for list

    Return:
    	lists for new_list
    """
new_list = [i for i in rainfall if i[1]>100]
print(new_list)

# (2) Use a list comprehension to create a list of just month names where the
# amount of rain was less than 50 mm. 
"""
    Des:
    	An exercise for list

    Return:
    	lists for month_names
    """
month_names = [i[0] for i in rainfall if i[1]<50]
print(month_names)

# (3) Now do (1) and (2) using conventional loops (you can choose to do 
# this before 1 and 2 !). 
"""
    Des:
    	An exercise for list

    Return:
    	lists for new_list, month_names
    """
new_list = []
for i in rainfall:
    if i[1]>100:
        new_list.append(i)
print(new_list)

month_names = []
for i in rainfall:
    if i[1]<50:
        month_names.append(i[0])
print(month_names)
# A good example output is:
#
# Step #1:
# Months and rainfall values when the amount of rain was greater than 100mm:
# [('JAN', 111.4), ('FEB', 126.1), ('AUG', 140.2), ('NOV', 128.4), ('DEC', 142.2)]
# ... etc.

