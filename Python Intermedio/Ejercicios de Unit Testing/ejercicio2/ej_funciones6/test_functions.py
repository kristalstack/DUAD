import unittest
from functions import sort_hyphen_string


class TestSortHyphenString(unittest.TestCase):

    def test_sort_hyphen_string_case_1(self):
        self.assertEqual(
            sort_hyphen_string("python-variable-funcion-computadora-monitor"),
            "computadora-funcion-monitor-python-variable"
        )

    def test_sort_hyphen_string_case_2(self):
        self.assertEqual(
            sort_hyphen_string("b-a-c"),
            "a-b-c"
        )

    def test_sort_hyphen_string_case_3(self):
        self.assertEqual(
            sort_hyphen_string("z-y-x"),
            "x-y-z"
        )


if __name__ == "__main__":
    unittest.main()