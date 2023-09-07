import rational
import math
from pprint import pprint
import random
""" 
    This file is used to run the application.
"""

if __name__ == '__main__':
    # Define N & T
    N = [i for i in range(0, 10)] #these are just indexes 
    T = [i for i in random.sample(range(0, 10), 3)] #these are just indexes
    #sort T 
    T.sort()
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
    pprint("The optimal witness size: {}".format(bloomy.witness_size))
    pprint("=============================================================")
    pprint("The length of the bitmap is: {}".format(len(bloomy.bitmap)))
    pprint("=============================================================")
    pprint("Initiating sanity check...")
    pprint("Check that the true positives are in the filter...")

    pprint("=============================================================")
    pprint("now we query the set N against the filter...")

    u_k_n = bloomy.r * len(N)
    l_k_n = (1 - bloomy.r) * len(N)

    upper_k_n = N[:math.floor(u_k_n)]
    lower_k_n = N[-math.ceil(l_k_n):]

    #convert t to a set, should get faster lookups 
    for i in upper_k_n:
        if i in T:
            if bloomy.query(i, math.floor(bloomy.k)):
                witness.append(1)
                fp.append(i)
        else:
            if bloomy.query(i, math.floor(bloomy.k + 1)):
                witness.append(0)
                fp.append(i)

    for i in lower_k_n:
        if i in T:
            if bloomy.query(i, math.floor(bloomy.k)):
                witness.append(1)
                fp.append(i)
        else:
            if bloomy.query(i, math.floor(bloomy.k + 1)):
                witness.append(0)
                fp.append(i)
     
    pprint("=============================================================")
    pprint("The actual witness size is: {}".format(len(witness)))
    pprint("Witness is: {}".format(witness))
    pprint("The elements caught are: {}".format(fp))
    pprint("the true positives are in the filter(should be equal to size of T): {}".format(witness.count(1)))
    pprint("the false positives are in the filter: {}".format(witness.count(0)))
    pprint("=============================================================")
    pprint("=============================================================")
    pprint("=============================================================")
    pprint("Now we decode to recover T..")
    reconstructed_T = []
    caught = []
    count = 0

    for i in upper_k_n:
        if i in T:
            if bloomy.query(i, math.floor(bloomy.k)):
                caught.append(i)
        else:
            if bloomy.query(i, math.floor(bloomy.k + 1)):
                caught.append(i)

    for i in lower_k_n:
        if i in T:
            if bloomy.query(i, math.floor(bloomy.k)):
                caught.append(i)
        else:
            if bloomy.query(i, math.floor(bloomy.k + 1)):
                caught.append(i)


    pprint("caught is size: {}".format(len(caught)))
    pprint("caught is: {}".format(caught))

    for i in caught:
        try:
            if witness[count] == 1:
                reconstructed_T.append(i)
                count += 1
            elif witness[count] == 0:
                count += 1
        except IndexError:
            break

    if reconstructed_T == T:
        pprint("The reconstructed T is: {}".format(reconstructed_T))
        pprint("The reconstructed T is equal to T: {}".format(True))



