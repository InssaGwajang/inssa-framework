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
from typing import List, Any
import os

from inssa.library import KWARGS, execute, RAISE


class TestBuiltins(TestCase):
    def test_kwargs(self):
        self.assertIn("attr1", KWARGS(attr1=3, attr2="attr2", attr3=[], attr4=None))
        self.assertIn("attr2", KWARGS(attr1=3, attr2="attr2", attr3=[], attr4=None))
        self.assertIn("attr3", KWARGS(attr1=3, attr2="attr2", attr3=[], attr4=None))
        self.assertNotIn("attr4", KWARGS(attr1=3, attr2="attr2", attr3=[], attr4=None))
        self.assertNotIn("attr5", KWARGS(attr1=3, attr2="attr2", attr3=[], attr4=None))

    def test_kwargs_dict(self):
        data = {"attr1": 3, "attr2": "attr2", "attr3": [], "attr4": None}

        self.assertIn("attr1", KWARGS(**data))
        self.assertIn("attr2", KWARGS(**data))
        self.assertIn("attr3", KWARGS(**data))
        self.assertNotIn("attr4", KWARGS(**data))
        self.assertNotIn("attr5", KWARGS(**data))

    def test_execute(self):
        def _func(attr: List) -> Any:
            return attr[0]

        self.assertEqual(execute([], _func, [3, 4]), 3)
        self.assertNotEqual(execute([], _func, [4]), 3)

        self.assertIsNone(execute(IndexError, _func, []), None)
        self.assertRaises(TypeError, execute, [], _func, [])
        self.assertRaises(IndexError, execute, TypeError, _func, [])

    def test_raise_(self):
        self.assertRaises(KeyError, RAISE, KeyError, "KeyError")
