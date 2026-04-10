import unittest
from functions import get_primes


class TestGetPrimes(unittest.TestCase):

    def test_get_primes_case_1(self):
        self.assertEqual(
            get_primes([1, 4, 6, 7, 13, 9, 67]),
            [7, 13, 67]
        )

    def test_get_primes_case_2(self):
        self.assertEqual(
            get_primes([2, 3, 4, 5, 6]),
            [2, 3, 5]
        )

    def test_get_primes_case_3(self):
        self.assertEqual(
            get_primes([10, 11, 12, 13]),
            [11, 13]
        )


if __name__ == "__main__":
    unittest.main()