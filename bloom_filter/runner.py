import rational
import math
from pprint import pprint
""" 
    This file is used to run the application.
"""

if __name__ == '__main__':
    data = [2,3,8,9,15,16,17]
    witness = []
    fp = []
    #convert values in data to bytes
    data = [bytes(str(i), 'utf-8') for i in data]
    n = len(data)
    fp = 0.01
    bloomy = rational.RationalFilter(n, fp)
    u_k, l_k = bloomy.sample_k()

    upper_k = data[:u_k]
    lower_k = data[-l_k:]
    #convert values in upper_k and lower_k to bytes

    for i in lower_k:
        bloomy.add(i, math.floor(bloomy.k))

    for i in upper_k:
        bloomy.add(i, math.floor(bloomy.k + 1))

    #getupper_k of N 
    pprint("=====================================")
    pprint("n: {}".format(n))
    pprint("fp: {}".format(fp))
    pprint("k: {}".format(bloomy.k))
    pprint("bit_length: {}".format(bloomy.bit_length))
    pprint("r: {}".format(bloomy.r))
    pprint("=====================================")
    pprint("Upper k: {}".format(upper_k))
    pprint("Lower k: {}".format(lower_k))
    pprint("=====================================")
    pprint("Bitmap: {}".format(bloomy.bitmap))
    pprint("=====================================")
    pprint("values in filter: {}".format(data))
    pprint("=====================================")

    for i in upper_k:
        pprint("Querying: {}".format(i))
        pprint(bloomy.query(i, math.floor(bloomy.k + 1)))
    for i in lower_k:
        pprint("Querying: {}".format(i))
        pprint(bloomy.query(i, math.floor(bloomy.k)))
    pprint("=====================================")
    pprint("Check FPR on dummy data")
    #generate dummy data and convert to bytes
    dummy = [i for i in range(0, 100)]
    dummy = [bytes(str(i), 'utf-8') for i in dummy]
    #need r to accurately split the data 
    r = bloomy.r
    #split the data into upper and lower k
    upper_k = math.floor( r * len(dummy)) 
    lower_k = math.ceil((1 - r) * len(dummy))

    upper_k = dummy[:upper_k]
    lower_k = dummy[-lower_k:]
    #convert values in upper_k and lower_k to bytes

    #query the filtef for values in upper_k and lower_k
    for i in upper_k:
        if bloomy.query(i, math.floor(bloomy.k + 1)):
            pprint("True or false positive: {}".format(i)) 
            if i in data:
                witness.append(1) #true positive
            else:
                witness.append(0) #false positive
    for i in lower_k:
        if bloomy.query(i, math.floor(bloomy.k)):
            pprint("True or false positive: {}".format(i))
            if i in data:
                witness.append(1)
            else:
                witness.append(0)
    print("=====================================")
    print("Witness: {}".format(witness))
    print("witnes length: {}".format(len(witness)))
