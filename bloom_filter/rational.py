"""
A rational filter implemented in Python.
@Author Ross Heaney
"""
import random
import math
random.seed(2)
import xxhash

class RationalFilter:
    """
    A rational filter implemented in Python.
    A rational filter is a bloom filter that uses different hash functions for different values
    It essentially bypasses the integrality assumption of the standard bloom filter.
    @Param n: The number of values in the filter.
    @Param k: The number of hash functions to use.
    @Param bit_length: The length of the bit array.
    @Param bitmap: The bit array.
    @Param fpr: The false positive rate.
    @Param r: Sampling parameter which determines the number of hash functions to subject to the data.
    @Param upper_k: The upper bound of the sampled k. How many values we are subjecting to k + 1 hash functions.
    @Param lower_k: The lower bound of the sampled k. How many values we are subjecting to k hash functions.
    @Param h1: The first hash function.
    @Param h2: The second hash function.
    """
    def __init__(self,n, p, q):
        self.n, self.p, self.q = n, p, q
        self.k, self.bit_length, self.bitmap = self.calculate_parameters(n, p, q)
        self.r = self.k - math.floor(self.k)
        self.upper_k, self.lower_k = self.sample_k()
        self.h1 = xxhash.xxh64
        self.h2 = xxhash.xxh64
        self.witness_size = math.ceil((self.p * self.n) * (1 + 1/math.log(2) ** 2))

    def calculate_parameters(self,n, p, q):
        """
        Calculate the parameters for the rational filter.
        :param length: The length of the data.
        :param fp: The false positive rate.
        @return k: The number of hash functions to use.
        @return bit_length: The length of the bit array.
        @return bitmap: The actual filter
        @return fp: The false positive rate.
        """
        L = math.log(2) 
        GAMMA = 1 / math.log(2)
        k = math.log10(q * L **2  / p) 
        bit_length = (p * n) * k * GAMMA

        # we will use math.ceil to approximate the values to the next integer
        return k, math.ceil(bit_length), [0] * math.ceil(bit_length)

    def add(self, data, k):
        """
        Add data to the filter.
        :param data: The data to add.
        :param k: The number of hash functions to use.
        "return The index values of the data.
        """
        hash_values = []

        for hash in range(k):
            hash_func = self.generate_hash_functions(hash)
            hash_values.append(hash_func(data))
        
        index_values = [h % self.bit_length for h in hash_values]
        for idx in index_values:
            self.bitmap[idx] = 1

        return index_values

    def query(self, data, k):
        """
        Query the filter.
        :param data: The data to query.
        :param k: The number of hash functions to use.
        :return: True if the data is in the filter, False otherwise.
        """
        hash_values = []

        for hash in range(k):
            hash_func = self.generate_hash_functions(hash)
            hash_values.append(hash_func(data))

        index_values = [h % self.bit_length for h in hash_values]
        for idx in index_values:
            if self.bitmap[idx] == 0:
                return False

        return True

    def sample_k(self):
        """
        Sample to get an optimal k for values in the filter
        r dictates the number of hash function we subject to the data
        """

        #if r is .6 then 60 % will go k + 1 and 40 % will go to k
        upper_k = self.r * (self.n * self.p)
        lower_k = (1 -self.r) * (self.n * self.p)

        return math.floor(upper_k), math.ceil(lower_k)

    def generate_hash_functions(self, n:int):
        """
        Generate the hash functions for the filter.
        :param n: The number of hash functions to generate.
        """
        def hash_function(data):
            return self.h1(data).intdigest() + (n * self.h2(data).intdigest())

        return hash_function

__author__ = 'Ross Heaney'
if __name__ == '__main__':
    pass

