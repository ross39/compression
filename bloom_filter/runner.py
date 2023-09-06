import rational
import math
from pprint import pprint
""" 
    This file is used to run the application.
"""

if __name__ == '__main__':
    n = 100
    fp = 0.01
    bloomy = rational.RationalFilter(n, fp)
    upper_k, lower_k = bloomy.sample_k()

    N = [i for i in range(n)]

    #get upper_k of N 
    upper_k_N = N[:upper_k]
    #get lower_k of N
    lower_k_N = N[-lower_k:]
    
    pprint("Rational Filter")
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

    

    hash_values = []
    data = [2,3,8,9]
    sampled_values = [6,6,7,7]
    for i in data:
        count = 0
        hash_func = bloomy.generate_hash_functions(sampled_values[count], rational.generate_random_prime(bloomy.bit_length))
        hash_values.append(hash_func(i))
        count += 1
    
    pprint("Indexes: {}".format(hash_values))

    indexes = [h % bloomy.bit_length for h in hash_values]

    pprint("Indexes: {}".format(indexes))
    pprint("bit_length: {}".format(bloomy.bit_length))
     
    #print the state of the filter
