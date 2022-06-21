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


from random import random

from inssa.framework import Interface


class TestInterface(TestCase):
    def test_init(self):
        self.assertIsInstance(Interface(), Interface)
        self.assertIsInstance(Interface(name="TestInterface"), Interface)

    def test_str(self):
        self.assertIsInstance(f"{Interface()}", str)
        self.assertIsInstance(f"{Interface(name='TestInterface')}", str)

    def test_print(self):
        self.assertIsNone(Interface().print())
        self.assertIsNone(Interface(name="TestInterface").print())

    def test_commands(self):
        interface = Interface()
        self.assertIsInstance(Interface(), Interface)

        self.assertFalse(interface.commands())
        self.assertIsNone(interface.register("command", "func"))
        self.assertTrue(interface.commands())

    def test_register(self):
        interface = Interface()
        self.assertIsInstance(Interface(), Interface)

        self.assertIsNone(interface.register("command", "func"))
        self.assertIsNone(interface.register("internal", "func", internal=True))
        self.assertRaises(ValueError, interface.register, "command", "func")

    def test_remove(self):
        interface = Interface()
        self.assertIsInstance(Interface(), Interface)

        self.assertIsNone(interface.register("command", "func"))
        self.assertIsNone(interface.remove("command"))
        self.assertRaises(ValueError, interface.remove, "command")

    def test_call(self):
        interface = Interface()
        self.assertIsInstance(Interface(), Interface)

        self.assertIsNone(interface.register("add", self._add))
        self.assertIsNone(interface.register("sub", self._sub))

        attr1, attr2, attr3 = random(), random(), random()

        self.assertEqual(interface.call("add", attr1, attr2), attr1 + attr2)
        self.assertEqual(interface.call("sub", attr1, attr2), attr1 - attr2)

        self.assertRaises(TypeError, interface.call, "add", attr1, attr2, attr3)

        self.assertEqual(interface.call("add", attr1, attr2, attr3=attr3), attr1 + attr2 + attr3)
        self.assertEqual(interface.call("sub", attr1, attr2, attr3=attr3), attr1 - attr2 - attr3)

        self.assertRaises(ValueError, interface.call, "mul")

    @staticmethod
    def _add(attr1, attr2, *, attr3=None):
        return (attr1 + attr2 + attr3) if attr3 else (attr1 + attr2)

    @staticmethod
    def _sub(attr1, attr2, *, attr3=None):
        return (attr1 - attr2 - attr3) if attr3 else (attr1 - attr2)
