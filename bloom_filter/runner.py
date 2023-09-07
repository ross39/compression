import rational
import math
from pprint import pprint
import random
""" 
    This file is used to run the application.
"""

if __name__ == '__main__':
    # Define N & T
    N = [i for i in range(0, 100)]
    T = [i for i in random.sample(range(0, 100), 20)]
    witness = []
    fp = []
    t = []

    #convert T and N to bytes
    N = [bytes(str(i), 'utf-8') for i in N]
    T = [bytes(str(i), 'utf-8') for i in T]
   
    # Define the parameters p & q
    p = len(T) / len(N)
    q = 1 - p

    # Create a rational filter
    bloomy = rational.RationalFilter(len(N), p, q)
    u_k, l_k = bloomy.sample_k()

    upper_k = T[:u_k]
    lower_k = T[-l_k:]

    for i in upper_k:
        bloomy.add(i, math.floor(bloomy.k + 1))

    for i in lower_k:
        bloomy.add(i, math.floor(bloomy.k))


        

    pprint("The bitmap is: {}".format(bloomy.bitmap))
    pprint("N is: {}".format(bloomy.n))
    pprint("p is: {}".format(bloomy.p))
    pprint("q is: {}".format(bloomy.q))
    pprint("k is: {}".format(bloomy.k))
    pprint("upper_k is: {}".format(math.floor(bloomy.k + 1)))
    pprint("lower_k is: {}".format(math.floor(bloomy.k)))
    pprint("r is: {}".format(bloomy.r))
    pprint("T is: {}".format(T))
    pprint("Length of T is: {}".format(len(T)))
    pprint("=============================================================")
    pprint("u_k is: {}".format(u_k))
    pprint("l_k is: {}".format(l_k))
    pprint("Based on T, the upper_k is: {}".format(upper_k))
    pprint("Based on T, the lower_k is: {}".format(lower_k))
    pprint("Witness size is: {}".format(bloomy.witness_size))
    pprint("=============================================================")
    pprint("The length of the bitmap is: {}".format(len(bloomy.bitmap)))
    pprint("=============================================================")
    pprint("Initiating sanity check...")
    pprint("Check that the true positives are in the filter...")

    for i in upper_k:
        pprint("checking using k = {}".format(math.floor(bloomy.k)))
        pprint(bloomy.query(i, math.floor(bloomy.k)))

    for i in lower_k:
        pprint("checking using k = {}".format(math.floor(bloomy.k + 1)))
        pprint(bloomy.query(i, math.floor(bloomy.k + 1)))
        

    pprint("=============================================================")
    pprint("now we query the set N against the filter...")

    u_k_n = bloomy.r * len(N)
    l_k_n = (1 - bloomy.r) * len(N)

    upper_k_n = N[:math.floor(u_k_n)]
    lower_k_n = N[-math.ceil(l_k_n):]

    for i in upper_k_n:
        if i in T:
            if bloomy.query(i, math.floor(bloomy.k)):
                t.append(i)
        else:
            if bloomy.query(i, math.floor(bloomy.k + 1)):
                fp.append(i)

    for i in lower_k_n:
        if i in T:
            if bloomy.query(i, math.floor(bloomy.k)):
                t.append(i)
        else:
            if bloomy.query(i, math.floor(bloomy.k + 1)):
                fp.append(i)
     
    pprint("=============================================================")
    pprint("The true positives are: {}".format(t))
    pprint("The false positives are: {}".format(fp))
    pprint("size of true positives is: {}".format(len(t)))
    pprint("size of false positives is: {}".format(len(fp)))




