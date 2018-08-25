import unittest
from src.math import Math

class MathTest(unittest.TestCase):
    def test_addition(self):
        # Make test fail
        self.assertEqual(Math.addition(4, 4), 8)

    def test_fibonacci(self):
        actual = Math.generate_fibonacci(11)
        expected = 89
        self.assertEqual(
            actual, expected, 'Actual value {} is different from Expected {} for number 11'.format(actual, expected)
        )
