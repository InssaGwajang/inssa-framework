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


from random import randint
import os

from references import candles
from inssa.library import MongoDB


_DATABASE = "TestMongoDB"
_COLLECTION = "CANDLES"

_MONGODB = MongoDB()


class TestMongoDB(TestCase):
    @classmethod
    def setUpClass(cls):
        if _DATABASE in _MONGODB.databases():
            _MONGODB.drop_database(_DATABASE)

    @classmethod
    def tearDownClass(cls):
        if _DATABASE in _MONGODB.databases():
            _MONGODB.drop_database(_DATABASE)

    def tearDown(self):
        if _DATABASE in _MONGODB.databases():
            _MONGODB.drop_database(_DATABASE)

    def test_init(self):
        self.assertIsInstance(_MONGODB, MongoDB)

    def test_databases(self):
        self.assertNotIn(_DATABASE, _MONGODB.databases())

        _MONGODB.insert(_DATABASE, _COLLECTION, candles())
        self.assertIn(_DATABASE, _MONGODB.databases())

    def test_collections(self):
        self.assertNotIn(_COLLECTION, _MONGODB.collections(_DATABASE))
        _MONGODB.insert(_DATABASE, _COLLECTION, candles())

        self.assertIn(_COLLECTION, _MONGODB.collections(_DATABASE))

    def test_insert(self):
        _MONGODB.insert(_DATABASE, _COLLECTION, candles())
        self.assertEqual(len(_MONGODB.select(_DATABASE, _COLLECTION)), len(candles()))

        _MONGODB.insert(_DATABASE, _COLLECTION, [{"key": "value"}])
        self.assertEqual(len(_MONGODB.select(_DATABASE, _COLLECTION)), len(candles()) + 1)
        self.assertIsNotNone(_MONGODB.select(_DATABASE, _COLLECTION).get("key", "value"))

    def test_select(self):
        _MONGODB.insert(_DATABASE, _COLLECTION, candles())
        self.assertEqual(len(_MONGODB.select(_DATABASE, _COLLECTION)), len(candles()))
        self.assertEqual(
            len(
                _MONGODB.select(
                    _DATABASE,
                    _COLLECTION,
                    key="datetime",
                    value=candles()[3]["datetime"],
                )
            ),
            1,
        )
        self.assertEqual(
            len(
                _MONGODB.select(
                    _DATABASE,
                    _COLLECTION,
                    key="datetime",
                    start=candles()[1]["datetime"],
                    end=candles()[4]["datetime"],
                )
            ),
            4,
        )
