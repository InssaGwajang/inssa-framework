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
from time import sleep

from inssa.library import Intervals


class TestIntervals(TestCase):
    def test_init(self):
        self.assertIsInstance(Intervals({5: 10, 60: 100}, file=True), Intervals)
        self.assertIsInstance(Intervals({5: 10, 60: 100}, file="TestIntervals.DictList"), Intervals)
        self.assertIsInstance(Intervals({5: 10, 60: 100}, name="TestIntervals"), Intervals)

    def test_leave(self):
        intervals = Intervals({0.1: 2, 0.2: 3})

        self.assertEqual(intervals.leave(), 0)
        self.assertEqual(intervals.leave(), 0)
        self.assertNotEqual(intervals.leave(), 0)

    def test_file(self):
        intervals = Intervals({0.1: 2, 0.2: 3})
        self.assertEqual(intervals.leave(), 0)
        self.assertEqual(intervals.leave(), 0)

        intervals = Intervals({0.1: 2, 0.2: 3})
        self.assertEqual(intervals.leave(), 0)
        self.assertEqual(intervals.leave(), 0)

        with TemporaryDirectory() as directory:
            file = os.path.join(directory, "TestIntervals.DictList")

            intervals = Intervals({0.1: 2, 0.2: 3}, file)
            self.assertEqual(intervals.leave(), 0)
            self.assertEqual(intervals.leave(), 0)

            intervals = Intervals({0.1: 2, 0.2: 3}, file)
            self.assertNotEqual(intervals.leave(), 0)
