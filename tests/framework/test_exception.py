from functools import reduce
from unittest import TestCase
import os, sys, pytest

DEPTH: int = 2
sys.path.append(
    reduce(  # parent directory
        lambda path, _: os.path.dirname(os.path.abspath(path)),
        range(DEPTH),
        os.path.abspath(os.path.dirname(__file__)),
    )
)

from inssa.library import clear

if __name__ == "__main__":
    pytest.main([os.path.realpath(__file__).replace(os.getcwd(), "")[1:]])
    clear()


from inssa.framework import exception


class TestInterval(TestCase):
    def test_exception(self):
        self.assertRaises(ValueError, exception)

        def divide_zero() -> float:
            try:
                return 1 / 0

            except Exception:
                return exception()

        self.assertIsInstance(divide_zero(), str)
