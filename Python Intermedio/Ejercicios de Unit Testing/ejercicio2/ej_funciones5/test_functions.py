import unittest
from functions import count_case


class TestCountCase(unittest.TestCase):

    def test_count_case_1(self):
        self.assertEqual(
            count_case("I love Nación Sushi"),
            "There’s 3 upper cases and 13 lower cases"
        )

    def test_count_case_2(self):
        self.assertEqual(
            count_case("Hello"),
            "There’s 1 upper cases and 4 lower cases"
        )

    def test_count_case_3(self):
        self.assertEqual(
            count_case("ABCdef"),
            "There’s 3 upper cases and 3 lower cases"
        )


if __name__ == "__main__":
    unittest.main()