import pytest
from src.math import Math


def test_fibonacci():
    actual = Math().generate_fibonacci(11)
    expected = 89
    assert actual == expected, 'Actual value {} is different from Expected {} for number 11'.format(actual, expected)
