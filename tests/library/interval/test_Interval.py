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


from time import sleep

from inssa.library import Interval


class TestInterval(TestCase):
    def test_init(self):
        self.assertIsInstance(Interval(3), Interval)
        self.assertIsInstance(Interval(5.5), Interval)

    def test_start(self):
        interval = Interval(0.1)
        self.assertEqual(interval.start(), 0)

        sleep(0.1)
        self.assertEqual(interval.start(), 0)
        self.assertNotEqual(interval.start(), 0)
