import rational
import math
from pprint import pprint
""" 
    This file is used to run the application.
"""

if __name__ == '__main__':
    p = 0.1
    q = 0.9
    n = 100
    bloomy = rational.RationalFilter(n, p, q)
    upper_k, lower_k = bloomy.sample_k()

    N = [i for i in range(n)]

    #get upper_k of N 
    upper_k_N = N[:upper_k]
    #get lower_k of N
    lower_k_N = N[-lower_k:]
    
    pprint("Rational Filter")
    pprint("Upper k: {}".format(upper_k))
    pprint("Lower k: {}".format(lower_k))
    for i in upper_k_N:
        bloomy.add(i, math.floor(bloomy.k + 1))
    for i in lower_k_N:
        bloomy.add(i, math.floor(bloomy.k))

    #print the state of the filter
    pprint(bloomy.bitmap)
