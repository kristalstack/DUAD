import unittest
from functions import sum_list


class TestSumList(unittest.TestCase):

    def test_sum_list_case_1(self):
        self.assertEqual(sum_list([4, 6, 2, 29]), 41)

    def test_sum_list_case_2(self):
        self.assertEqual(sum_list([1, 2, 3, 4]), 10)

    def test_sum_list_case_3(self):
        self.assertEqual(sum_list([0, 0, 0]), 0)


if __name__ == "__main__":
    unittest.main()