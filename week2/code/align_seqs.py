"""takes the DNA sequences as an input from a single external file
and saves the best alignment along with its corresponding score in a single text file."""

__appname__ = 'align_seqs.py'
__author__ = 'shengge.tong22@imperial.ac.uk'
__version__= '0.0.1'

import csv
import sys

def read_csv(): #read the sequence
    """
    Returns:
    	Two sequences seq1,seq2
    	
    Des:
    	Read the seq csv
    """
    with open('../data/example_seq.csv','r') as r:
        seq_list = []
        seq = csv.reader(r)
        for i in seq:
            seq_list.append(i[1])
        seq1 = seq_list[0]
        seq2 = seq_list[1]
    return seq1,seq2


# Assign the longer sequence s1, and the shorter to s2
# l1 is length of the longest, l2 that of the shortest
def sequence_length(seq1,seq2):
    """
    Des:
    	Compare the sequence length for later calculation
    	
    Returns:
    	return seq1,seq2 and the lenth l1,l2
    """
    l1 = len(seq1)
    l2 = len(seq2)
    if l1 >= l2:
        s1 = seq1
        s2 = seq2
    else:
        s1 = seq2
        s2 = seq1
        l1, l2 = l2, l1 # swap the two lengths
    return s1, s2, l1, l2


# A function that computes a score by returning the number of matches starting
# from arbitrary startpoint (chosen by user)
def calculate_score(s1, s2, l1, l2, startpoint):
    """
    Des:
    	A function that computes a score by returning the number of matches starting
    	
    Arguments:
    	s1,s2,l1,l2,startpoint

    Return:
    	Score 
    """
    matched = "" # to hold string displaying alignements
    score = 0
    for i in range(l2):
        if (i + startpoint) < l1:
            if s1[i + startpoint] == s2[i]: # if the bases match
                matched = matched + "*"
                score = score + 1
            else:
                matched = matched + "-"

    return score

# Test the function with some example starting points:
# calculate_score(s1, s2, l1, l2, 0)
# calculate_score(s1, s2, l1, l2, 1)
# calculate_score(s1, s2, l1, l2, 5)

# now try to find the best match (highest score) for the two sequences
def best_align(s1, s2, l1, l2):
    """
    Des:
    	A function that find the best match (highest score) for the two sequences
    	
    Arguments:
    	s1,s2,l1,l2

    Return:
    	my_best_align,my_best_score
    """
    my_best_align = None
    my_best_score = -1

    for i in range(l1): # Note that you just take the last alignment with the highest score
        z = calculate_score(s1, s2, l1, l2, i)
        if z > my_best_score:
            my_best_align = "." * i + s2 # think about what this is doing!
            my_best_score = z 
    print(my_best_align)
    print(s1)
    print("Best score:", my_best_score)

    return my_best_align,my_best_score


def result(my_best_align, my_best_score): 

    """
    Des:
    	Output the result into txt file
    	
    Arguments:
    	s1,s2,l1,l2

    Return:
    	align_result.txt
    """
    result = open('../results/align_result.txt','w') 
    result.write('Best alignment:' + str(my_best_align) + '\n')
    result.write('Best score:' + str(my_best_score) + '\n')
    result.close()
    return 0

def main(argv): #Makes sure the "main" function is called from command line
    """ 
    Main process running the program.
    """ 
    seq1, seq2 = read_csv()
    s1, s2, l1, l2 = sequence_length(seq1, seq2)
    my_best_align, my_best_score = best_align(s1, s2, l1, l2)
    result(my_best_align, my_best_score)
    return 0

if __name__ == "__main__": 
    
    status = main(sys.argv)
    sys.exit(status)
