"""
A rational filter implemented in Python.
@Author Ross Heaney
"""
import random
from sympy import isprime
import math


def hashing_function(prime, length, data:int):

    """
    A hashing function that takes a prime number, a prime number greater than the length of the data, the length of the
    Is of the form (b + a * v) mod prime ) mod length where 1 <= a < p and 0 <= b < p.
    :param prime: A prime number greater than the length of the data.
    :param length: The length of the data.
    :param data: The data to hash.
    :return: an index in the range 0 <= index < length.
    """
    a = random.randint(1, prime - 1)
    b = random.randint(0, prime - 1)
    return ((b + a * data) % prime) % length

def generate_random_prime(length):
    """
    Generate a random prime greater than length.
    :param length: The length of the prime to generate.
    return: A random prime greater than length.
    """
    primes = [i for i in range(length, 1000) if isprime(i)]
    return random.choice(primes)


class RationalFilter:
    """
    A rational filter implemented in Python.
    A rational filter is a bloom filter that uses different hash functions for different values
    It essentially bypasses the integrality assumption of the standard bloom filter.
    @Param n: The number of values in the filter.
    @Param p: The positive rational
    @Param q: The negative rational
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
    def __init__(self,n,p,q):
        self.n = n
        self.p = p
        self.q = q
        self.k, self.bit_length, self.bitmap, self.fpr = self.calculate_parameters(p,n,q)
        self.r = self.k - math.floor(self.k)
        self.upper_k, self.lower_k = self.sample_k()
        self.h1 = hashing_function
        self.h2 = hashing_function

    def calculate_parameters(self,p, n, q):
        """
        Calculate the parameters for the rational filter.
        :param length: The length of the data.
        """
        L = math.log(2)
        GAMMA  = (1 / math.log(2)) ** 2
        k = math.log10(q * L ** 2 / p) 
        fpr = p * GAMMA ** 2 / q
        bit_length = (p*n) * k * GAMMA
        return k, math.ceil(bit_length), [0] * math.ceil(bit_length), fpr

    def add(self, data, k):
        """
        Add data to the filter.
        :param data: The data to add.
        :param k: The number of hash functions to use.
        "return The index values of the data.
        """
        index_values = []

        for hash in range(k):
            hash_func = self.generate_hash_functions(hash, generate_random_prime(self.bit_length))
            index_values.append(hash_func(data))
        
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
        index_values = []

        for hash in range(k):
            hash_func = self.generate_hash_functions(hash, generate_random_prime(self.bit_length))
            index_values.append(hash_func(data))

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
        upper_k = self.r * self.n
        lower_k = (1 -self.r) * self.n

        return math.ceil(upper_k), math.floor(lower_k)

    def generate_hash_functions(self, n:int, prime):
        """
        Generate the hash functions for the filter.
        :param n: The number of hash functions to generate.
        """
        def hash_function(data):
            return self.h1(prime, self.bit_length, data) + (n * self.h2(prime, self.bit_length, data))

        return hash_function

__author__ = 'Ross Heaney'
if __name__ == '__main__':
    pass

