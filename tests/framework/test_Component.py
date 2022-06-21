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


from typing import Any
from random import random

from inssa.framework import Component, Interface


class Reflector(Component):
    interfaces = ("reflect",)

    def reflect(self, attr: Any, /) -> Any:
        return attr


class Calculator(Component):
    interfaces = ("add", "sub")

    def add(self, attr1: Any, attr2: Any, /) -> Any:
        return self.call("reflect", attr1) + self.call("reflect", attr2)

    def sub(self, attr1: Any, attr2: Any, /) -> Any:
        return self.call("reflect", attr1) - self.call("reflect", attr2)


class TestComponent(TestCase):
    def test_init(self):
        self.assertIsInstance(Reflector(), Component)

    def test_initialize(self):
        self.assertIsNone(Reflector(interface=Interface()).initialize())

    def test_finalize(self):
        reflector = Reflector(interface=Interface())
        self.assertIsInstance(reflector, Component)

        self.assertIsNone(reflector.initialize())
        self.assertIsNone(reflector.finalize())

    def test_call(self):
        interface = Interface()

        reflector = Reflector(interface=interface)
        calculator = Calculator(interface=interface)
        self.assertIsInstance(reflector, Component)
        self.assertIsInstance(calculator, Component)

        self.assertIsNone(reflector.initialize())
        self.assertIsNone(calculator.initialize())

        attr1, attr2, attr3 = random(), random(), random()

        self.assertEqual(interface.call("add", attr1, attr2), attr1 + attr2)
        self.assertEqual(interface.call("sub", attr1, attr2), attr1 - attr2)
