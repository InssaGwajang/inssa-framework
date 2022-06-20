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


from typing import Dict
from tempfile import TemporaryDirectory
from random import randint
import os

from test_references import members, candles
from inssa.library import HandledDictList


class TestDictList(TestCase):
    def test_init(self):
        self.assertIsInstance(
            HandledDictList(
                [],
            ),
            HandledDictList,
        )
        for references in (members(), candles()):
            self.assertIsInstance(HandledDictList([self._pass], references), HandledDictList)

    def test_len(self):
        for references in (members(), candles()):
            data = HandledDictList([self._pass], references)
            self.assertIsInstance(data, HandledDictList)
            self.assertEqual(len(data), len(references))

            data = HandledDictList(
                [],
            )
            self.assertIsInstance(data, HandledDictList)
            self.assertEqual(len(data), 0)
            self.assertIsNone(data.extend(references))
            self.assertEqual(len(data), len(references))

    def test_iter(self):
        for references in (members(), candles()):
            for element in HandledDictList([self._pass], references):
                self.assertIsInstance(element, dict)

    def test_index(self):
        for references in (members(), candles()):
            data = HandledDictList([self._pass], references)
            self.assertIsInstance(data, HandledDictList)

            index = randint(0, len(references) - 1)
            self.assertEqual(data[index], references[index])

    def test_slice(self):
        for references in (members(), candles()):
            data = HandledDictList([self._pass], references)
            self.assertIsInstance(data, HandledDictList)

            index = randint(0, len(references) - 1)
            self.assertListEqual(data[0:index], references[0:index])

    def test_str(self):
        for references in (members(), candles()):
            data = HandledDictList([self._pass], references)
            self.assertIsInstance(data, HandledDictList)

            self.assertIsInstance(f"{data}", str)

    def test_print(self):
        for references in (members(), candles()):
            data = HandledDictList([self._pass], references)
            self.assertIsInstance(data, HandledDictList)

            self.assertIsNone(data.print())

    def test_get(self):
        for references in (members(), candles()):
            data = HandledDictList([self._pass], references)
            self.assertIsInstance(data, HandledDictList)

            self.assertIsNotNone(data.get())
            self.assertIsNone(data.get("attr1"))

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
        for references in (members(), candles()):
            data = HandledDictList([self._pass], references)
            self.assertIsInstance(data, HandledDictList)

            self.assertTrue(data.items())
            self.assertIsNone(data.items("attr1"))

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
        for references in (members(), candles()):
            data = HandledDictList([self._pass], references)
            self.assertIsInstance(data, HandledDictList)

            index = randint(0, len(references) - 1)
            key = list(references[index].keys())[0]
            self.assertTrue(data.values(key))
            self.assertTrue(data.values(key, overlap=False, sort=True))

    def test_append(self):
        for references in (members(), candles()):
            data = HandledDictList([self._pass], references)
            self.assertIsInstance(data, HandledDictList)

            self.assertIsNone(data.append({"key": "value"}))
            self.assertEqual(len(data), len(references) + 1)

    def test_insert(self):
        for references in (members(), candles()):
            data = HandledDictList([self._pass], references)
            self.assertIsInstance(data, HandledDictList)

            self.assertRaises(ValueError, data.insert, {"key": "name"})

    def test_extend(self):
        for references in (members(), candles()):
            data = HandledDictList([self._pass], references)
            self.assertIsInstance(data, HandledDictList)

            self.assertIsNone(data.extend(references))
            self.assertEqual(len(data), len(references) * 2)

            self.assertIsNone(data.extend([]))
            self.assertEqual(len(data), len(references) * 2)

    def test_remove(self):
        for references in (members(), candles()):
            data = HandledDictList([self._pass], references)
            self.assertIsInstance(data, HandledDictList)

            index = randint(0, len(references) - 1)
            self.assertRaises(ValueError, data.remove, references[index])

    def test_pop(self):
        for references in (members(), candles()):
            data = HandledDictList([self._pass], references)
            self.assertIsInstance(data, HandledDictList)

            self.assertRaises(ValueError, data.pop)

    def test_clear(self):
        for references in (members(), candles()):
            data = HandledDictList([self._pass], references)
            self.assertIsInstance(data, HandledDictList)

            self.assertRaises(ValueError, data.pop)

    def test_read_write(self):
        with TemporaryDirectory() as directory:
            for type in ("DictList", "csv", "json"):
                path = os.path.join(directory, "file." + type)

                self.assertTrue(HandledDictList([self._pass], members()).write(path))
                self.assertListEqual(HandledDictList([self._pass], path).items(), members())

                path = os.path.join(directory, "file")
                self.assertTrue(HandledDictList([self._pass], members()).write(path, type=type))
                self.assertListEqual(
                    HandledDictList([self._pass], path, type=type).items(), members()
                )

    def test_handle(self):
        data = HandledDictList([self._count_keys], members())
        self.assertIsInstance(data, HandledDictList)

        index = randint(0, len(members()) - 1)
        self.assertEqual(data[index]["count"], len(members()[index].keys()))

    @staticmethod
    def _pass(_: Dict, pipe: Dict) -> Dict:
        return pipe

    @staticmethod
    def _count_keys(element: Dict, pipe: Dict) -> Dict:
        element["count"] = len(element.keys())

        return pipe
