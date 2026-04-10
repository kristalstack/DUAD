import unittest
from bubble_sort import bubble_sort

class TestBubbleSort(unittest.TestCase):

    def test_works_with_small_list(self):
        self.assertEqual(bubble_sort([5, 2, 8, 1, 3]), [1, 2, 3, 5, 8])

    def test_works_with_large_list(self):
        lst = list(range(150, 0, -1))
        self.assertEqual(bubble_sort(lst), sorted(lst))

    def test_works_with_empty_list(self):
        self.assertEqual(bubble_sort([]), [])

    def test_fails_with_non_list_parameter(self):
        with self.assertRaises(TypeError):
            bubble_sort("not a list")

if __name__ == "__main__":
    unittest.main()