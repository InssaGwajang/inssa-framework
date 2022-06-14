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
from inssa.library import kwargs, execute


class TestBuiltins(TestCase):
    def test_kwargs(self):
        self.assertIn("attr1", kwargs(attr1=3, attr2="attr2", attr3=[], attr4=None))
        self.assertIn("attr2", kwargs(attr1=3, attr2="attr2", attr3=[], attr4=None))
        self.assertIn("attr3", kwargs(attr1=3, attr2="attr2", attr3=[], attr4=None))
        self.assertNotIn("attr4", kwargs(attr1=3, attr2="attr2", attr3=[], attr4=None))
        self.assertNotIn("attr5", kwargs(attr1=3, attr2="attr2", attr3=[], attr4=None))

    def test_kwargs_dict(self):
        data = {"attr1": 3, "attr2": "attr2", "attr3": [], "attr4": None}

        self.assertIn("attr1", kwargs(**data))
        self.assertIn("attr2", kwargs(**data))
        self.assertIn("attr3", kwargs(**data))
        self.assertNotIn("attr4", kwargs(**data))
        self.assertNotIn("attr5", kwargs(**data))

    def test_execute(self):
        def _func(attr: List) -> Any:
            return attr[0]

        self.assertEqual(execute([], _func, [3, 4]), 3)
        self.assertNotEqual(execute([], _func, [4]), 3)

        self.assertIsNone(execute(IndexError, _func, []), None)
        self.assertRaises(TypeError, execute, [], _func, [])
        self.assertRaises(IndexError, execute, TypeError, _func, [])
