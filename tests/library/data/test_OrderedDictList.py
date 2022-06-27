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
from random import randint
import os

from references import members, candles
from inssa.library import OrderedDictList


class TestOrderedDictList(TestCase):
    def test_init(self):
        self.assertIsInstance(OrderedDictList("key"), OrderedDictList)

        for key, references in (("name", members()), ("datetime", candles())):
            self.assertIsInstance(OrderedDictList(key, references), OrderedDictList)

        self.assertRaises(KeyError, OrderedDictList, "phone", members())

    def test_len(self):
        for key, references in (("name", members()), ("datetime", candles())):
            data = OrderedDictList(key, references)
            self.assertIsInstance(data, OrderedDictList)
            self.assertEqual(len(data), len(references))

            data = OrderedDictList(key)
            self.assertIsInstance(data, OrderedDictList)
            self.assertIsNone(data.extend(references))
            self.assertEqual(len(data), len(references))

    def test_iter(self):
        for key, references in (("name", members()), ("datetime", candles())):
            for element in OrderedDictList(key, references):
                self.assertIsInstance(element, dict)

    def test_index(self):
        for key, references in (("name", members()), ("datetime", candles())):
            data = OrderedDictList(key, references)
            self.assertIsInstance(data, OrderedDictList)

            index = randint(0, len(references) - 1)
            self.assertIn(data[index], references)

    def test_slice(self):
        for key, references in (("name", members()), ("datetime", candles())):
            data = OrderedDictList(key, references)
            self.assertIsInstance(data, OrderedDictList)

            index = randint(0, len(references) - 1)
            for element in data[0:index]:
                self.assertIn(element, references)

    def test_str(self):
        for key, references in (("name", members()), ("datetime", candles())):
            data = OrderedDictList(key, references)
            self.assertIsInstance(data, OrderedDictList)

            self.assertIsInstance(f"{data}", str)

    def test_print(self):
        for key, references in (("name", members()), ("datetime", candles())):
            data = OrderedDictList(key, references)
            self.assertIsInstance(data, OrderedDictList)

            self.assertIsNone(data.print())

    def test_get(self):
        for key, references in (("name", members()), ("datetime", candles())):
            data = OrderedDictList(key, references)
            self.assertIsInstance(data, OrderedDictList)

            self.assertIsNotNone(data.get())

            index = randint(0, len(references) - 1)
            self.assertEqual(data.get(references[index][key]), references[index])

            index = randint(0, len(references) - 1)
            key = list(references[index].keys())[0]
            self.assertEqual(data.get(key, references[index][key]), references[index])

            index = randint(0, len(references) - 1)
            self.assertEqual(
                data.get({key: references[index][key] for key in references[index].keys()}),
                references[index],
            )

            index = randint(0, len(references) - 1)
            self.assertEqual(
                data.get(tuple((key, references[index][key]) for key in references[index].keys())),
                references[index],
            )

            index = randint(0, len(references) - 1)
            self.assertEqual(
                data.get([(key, references[index][key]) for key in references[index].keys()]),
                references[index],
            )

    def test_items(self):
        for key, references in (("name", members()), ("datetime", candles())):
            data = OrderedDictList(key, references)
            self.assertIsInstance(data, OrderedDictList)

            self.assertTrue(data.items())

            index = randint(0, len(references) - 1)
            self.assertTrue(data.items(references[index][key]))

            index = randint(0, len(references) - 1)
            key = list(references[index].keys())[0]
            self.assertEqual(data.items(key, references[index][key])[0], references[index])

            index = randint(0, len(references) - 1)
            self.assertEqual(
                data.items({key: references[index][key] for key in references[index].keys()})[0],
                references[index],
            )

            index = randint(0, len(references) - 1)
            self.assertEqual(
                data.items(
                    tuple((key, references[index][key]) for key in references[index].keys())
                )[0],
                references[index],
            )

            index = randint(0, len(references) - 1)
            self.assertEqual(
                data.items([(key, references[index][key]) for key in references[index].keys()])[0],
                references[index],
            )

    def test_values(self):
        for key, references in (("name", members()), ("datetime", candles())):
            data = OrderedDictList(key, references)
            self.assertIsInstance(data, OrderedDictList)

            index = randint(0, len(references) - 1)
            key = list(references[index].keys())[0]
            self.assertTrue(data.values(key))
            self.assertTrue(data.values(key, overlap=False, sort=True))

            self.assertTrue(data.values())
            self.assertTrue(data.values(key))

    def test_append(self):
        data = OrderedDictList("name", members())
        self.assertIsInstance(data, OrderedDictList)

        self.assertIsNone(data.append({"name": "name"}))
        self.assertEqual(len(data), len(members()) + 1)

    def test_insert(self):
        data = OrderedDictList("name", members())
        self.assertIsInstance(data, OrderedDictList)

        self.assertRaises(ValueError, data.insert, {"name": "name"})

    def test_extend(self):
        for key, references in (("name", members()), ("datetime", candles())):
            data = OrderedDictList(key, references)
            self.assertIsInstance(data, OrderedDictList)

            self.assertIsNone(data.extend(references))
            self.assertEqual(len(data), len(references) * 2)

            self.assertIsNone(data.extend([]))
            self.assertEqual(len(data), len(references) * 2)

    def test_remove(self):
        for key, references in (("name", members()), ("datetime", candles())):
            data = OrderedDictList(key, references)
            self.assertIsInstance(data, OrderedDictList)

            index = randint(0, len(references) - 1)
            self.assertIsNone(data.remove(references[index]))
            self.assertRaises(ValueError, data.remove, references[index])

    def test_pop(self):
        for key, references in (("name", members()), ("datetime", candles())):
            data = OrderedDictList(key, references)
            self.assertIsInstance(data, OrderedDictList)

            for _ in range(len(data)):
                self.assertNotIn(data.pop(), data)

            self.assertRaises(IndexError, data.pop)

    def test_clear(self):
        for key, references in (("name", members()), ("datetime", candles())):
            data = OrderedDictList(key, references)
            self.assertIsInstance(data, OrderedDictList)

            self.assertTrue(data.items())
            self.assertIsNone(data.clear())
            self.assertFalse(data.items())

    def test_read_write(self):
        with TemporaryDirectory() as directory:
            for type in ("DictList", "csv", "json"):
                path = os.path.join(directory, "file." + type)

                data = OrderedDictList("name", members())
                self.assertTrue(data.write(path))
                self.assertListEqual(
                    list(OrderedDictList("name", path).items()), list(data.items())
                )

                path = os.path.join(directory, "file")
                data = OrderedDictList("name", members())
                self.assertTrue(data.write(path, type=type))
                self.assertListEqual(
                    list(OrderedDictList("name", path, type=type).items()), list(data.items())
                )
