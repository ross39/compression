import rational 
import unittest
from sympy import isprime
import math

"""
    This is a unit test for the rational filter.
"""


class RationalTest(unittest.TestCase):

    def test_add(self):
        """
        Test that the data is added to the filter.
        A successful test will set k indexe in the filter to 1
        """
        p = 0.1
        q = 0.9
        n = 100
        bloomy = rational.RationalFilter(n, p, q)
        data = 2
        bloomy.add(data, math.ceil(bloomy.k))
        #count number of 1's in the filter
        count = 0
        for bit in bloomy.bitmap:
            if bit == 1:
                count += 1

        self.assertEqual(count, math.ceil(bloomy.k))

    def test_query(self):
        pass

    def test_sampling(self):
        """
        Test that a sampled k for the values in the filter is accurate.
        A successful test will return a k that is close to the calculated k
        """
        p = 0.1
        q = 0.9
        n = 100
        bloomy = rational.RationalFilter(n, p, q)
        upper_k, lower_k = bloomy.sample_k()

        #assert that upper_k = bloomy.r * bloomy.n
        self.assertEqual(upper_k, math.ceil(bloomy.r * bloomy.n))
        #assert that lower_k = (1 - bloomy.r) * bloomy.n
        self.assertEqual(lower_k, math.floor((1 - bloomy.r) * bloomy.n))

    def test_calculate_parameters(self):
        """
        Test that the parameters are calculated correctly
        """
        GAMMA = (1 / math.log(2)) ** 2
        p = 0.1
        q = 0.9
        k = 0.64
        n = 100
        bloomy = rational.RationalFilter(n, p, q)
        #assert that the parameters are calculated correctly
        self.assertEqual(bloomy.p, p)
        self.assertEqual(bloomy.q, q)
        self.assertEqual(round(bloomy.k, 2), k)
        self.assertEqual(bloomy.n, n)
        self.assertEqual(bloomy.bit_length,math.ceil((p*n) * bloomy.k * GAMMA))

    def test_generate_prime(self):
        prime = rational.generate_random_prime(100)
        self.assertTrue(isprime(prime))

    def test_generate_hash_functions(self):
        """
        Test the generation of hash functions.
        If we use k = 3 then we should get 3 indexes
        A successful test will return k  indexes in range 0 - length of bit array
        """
        p = 0.1
        q = 0.9
        n = 100
        bloomy = rational.RationalFilter(n, p, q)
        index_values = []

        data = [2,3,8,9]
        #convert to bytes
        for i in data:
            for hash in range(math.ceil(bloomy.k)):
                hash_func = bloomy.generate_hash_functions(hash, rational.generate_random_prime(bloomy.bit_length))
                index_values.append(hash_func(i))

        for idx in index_values:
            self.assertTrue(idx < len(bloomy.bitmap))

    def test_witness_generation(self):
        pass

    def test_compress(self):
        pass

    def test_decompress(self):
        pass

if __name__ == '__main__':
    unittest.main()
