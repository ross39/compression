import rational 
import unittest
from sympy import isprime
import math
from unittest.mock import Mock
import random
random.seed(2)
"""
    This is a unit test for the rational filter.
"""


class RationalTest(unittest.TestCase):
    
    def setUp(self):
        """
        Set up the test.
        """
        self.data = [i for i in random.sample(range(0, 100), 10)]
        self.bloomy = rational.RationalFilter(10, 0.01)
        self.r = self.bloomy.r
        self.u_k, self.l_k = self.bloomy.sample_k()

    def test_add_and_query(self):
        """
        Test that the data is added to the filter.
        Test that the data is queried correctly.
        """
        #check the bitmap is empty
        self.assertEqual(self.bloomy.bitmap, [0] * math.ceil(self.bloomy.bit_length))
        #add data to the filter
        upper_k = self.data[:self.u_k]
        lower_k = self.data[-self.l_k:]
        #convert values in upper_k and lower_k to bytes
        upper_k = [bytes(str(i), 'utf-8') for i in upper_k]
        lower_k = [bytes(str(i), 'utf-8') for i in lower_k]
        for i in lower_k:
            self.bloomy.add(i, math.floor(self.bloomy.k))

        for i in upper_k:
            self.bloomy.add(i, math.floor(self.bloomy.k + 1))

        #check the bitmap is not empty
        self.assertNotEqual(self.bloomy.bitmap, [0] * math.ceil(self.bloomy.bit_length))
        for i in lower_k:
            self.assertTrue(self.bloomy.query(i, math.floor(self.bloomy.k)))

        for i in upper_k:
            self.assertTrue(self.bloomy.query(i, math.floor(self.bloomy.k + 1)))

    def test_sampling(self):
        """
        Test that a sampled k for the values in the filter is accurate.
        A successful test will return a k that is close to the calculated k
        """
        self.assertEqual(self.u_k, math.floor(self.r * len(self.data)))
        self.assertEqual(self.l_k, math.ceil((1 - self.r) * len(self.data)))

    def test_calculate_parameters(self):
        """
        Test that the parameters are calculated correctly
        """
        pass
    def test_generate_hash_functions(self):
        """
        Test the generation of hash functions.
        If we use k = 3 then we should get 3 indexes
        A successful test will return k  indexes in range 0 - length of bit array
        """
        pass
    
    def test_output(self):
        """
        Test that the output is correct.
        witness size should be T(1 + 1/ln(2) **2) 
        bitmap size should be T * K * ln(2)
        """
        pass


if __name__ == '__main__':
    unittest.main()
