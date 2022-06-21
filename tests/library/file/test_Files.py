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


import os

from test_references import members
from inssa.library import Files


_PATH = os.path.join(os.path.dirname(__file__), "test_Files_references")


class TestFiles(TestCase):
    def test_init(self):
        self.assertIsInstance(Files(_PATH), Files)

    def test_files(self):
        self.assertTrue(Files(_PATH).files())
        self.assertFalse(Files(os.path.join(_PATH, "directory")).files())

    def test_json(self):
        files = Files(_PATH)
        self.assertIsInstance(files, Files)

        self.assertEqual(files.json("data.members"), members())

        self.assertRaises(UnicodeDecodeError, files.json, "data.candles")
        self.assertRaises(ValueError, files.json, "data.file")

    def test_module(self):
        files = Files(_PATH)
        self.assertIsInstance(files, Files)

        self.assertIsInstance(files.module("module.get", "get_int")(), int)
        self.assertIsInstance(files.module("module.get", "get_float")(), float)

        self.assertRaises(AttributeError, files.module, "module.get", "get_str")
        self.assertRaises(ValueError, files.module, "data.set", "set_str")
