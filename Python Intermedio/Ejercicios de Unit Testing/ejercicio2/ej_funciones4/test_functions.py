import unittest
from functions import reverse_string


class TestReverseString(unittest.TestCase):

    def test_reverse_string_case_1(self):
        self.assertEqual(reverse_string("Hola mundo"), "odnum aloH")

    def test_reverse_string_case_2(self):
        self.assertEqual(reverse_string("Python"), "nohtyP")

    def test_reverse_string_case_3(self):
        self.assertEqual(reverse_string("abc"), "cba")


if __name__ == "__main__":
    unittest.main()