from functools import reduce
from unittest import TestCase
import os, sys, pytest

DEPTH: int = 3
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


from tempfile import TemporaryDirectory
from random import choice

from inssa.library import Upbit


class TestUpbit(TestCase):
    def test_init(self):
        self.assertIsInstance(Upbit(), Upbit)

    def test_markets(self):
        self.assertTrue(Upbit.markets())

    def test_candles(self):
        self.assertNotEqual(len(Upbit.candles(choice(Upbit.markets()), "month")), 0)
