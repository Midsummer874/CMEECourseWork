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