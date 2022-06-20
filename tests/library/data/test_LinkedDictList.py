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

from test_references import candles, half_day_candles
from inssa.library import LinkedDictList, DictList


class TestLinkedDictList(TestCase):
    def test_init(self):
        self.assertIsInstance(LinkedDictList("datetime", {DictList(): []}), LinkedDictList)
        self.assertIsInstance(
            LinkedDictList(
                "datetime",
                {
                    DictList(candles()): [],
                    DictList(half_day_candles()): [],
                },
            ),
            LinkedDictList,
        )
        self.assertIsInstance(
            LinkedDictList(
                "datetime",
                {
                    DictList(candles()): [],
                    DictList(half_day_candles()): [],
                },
                [],
            ),
            LinkedDictList,
        )

    def test_len(self):
        links = LinkedDictList(
            "datetime",
            {
                DictList(candles()): [],
                DictList(half_day_candles()): [],
            },
        )
        self.assertIsInstance(links, LinkedDictList)
        self.assertEqual(len(links), 2)

    def test_iter(self):
        for link in LinkedDictList(
            "datetime",
            {
                DictList(candles()): [],
                DictList(half_day_candles()): [],
            },
        ):
            self.assertIsInstance(link, DictList)

    def test_index(self):
        links = LinkedDictList(
            "datetime",
            {
                DictList(candles()): [],
                DictList(half_day_candles()): [],
            },
        )
        self.assertIsInstance(links, LinkedDictList)

        index = randint(0, len(links) - 1)
        data = candles() if not index else half_day_candles()

        element_index = randint(0, len(data) - 1)
        self.assertEqual(links[index][element_index], data[element_index])

    def test_slice(self):
        links = LinkedDictList(
            "datetime",
            {
                DictList(candles()): [],
                DictList(half_day_candles()): [],
            },
        )
        self.assertIsInstance(links, LinkedDictList)
        self.assertListEqual(links[0:][0].items(), candles())

    def test_str(self):
        links = LinkedDictList(
            "datetime",
            {
                DictList(candles()): [],
                DictList(half_day_candles()): [],
            },
        )
        self.assertIsInstance(links, LinkedDictList)
        self.assertIsInstance(f"{links}", str)

    def test_print(self):
        links = LinkedDictList(
            "datetime",
            {
                DictList(candles()): [],
                DictList(half_day_candles()): [],
            },
        )
        self.assertIsInstance(links, LinkedDictList)
        self.assertIsNone(links.print())

    def test_linked(self):
        candle_data = DictList()
        half_day_candle_data = DictList()

        class _Average:
            def __init__(self, key: str):
                self._key = key
                self._values = []

            def handle(self, element: Dict, pipe: Dict):
                self._values.append(element[self._key])
                average = sum(self._values) / len(self._values)

                element["average"] = average
                return {**pipe, **{"average": average}}

        links = LinkedDictList(
            "datetime",
            {
                candle_data: [_Average("close").handle],
                half_day_candle_data: [_Average("close").handle],
            },
        )
        self.assertIsNone(links.handle())

        self.assertIsNone(candle_data.extend(candles()[:2]))
        self.assertIsNone(half_day_candle_data.extend(half_day_candles()[:4]))
        self.assertIsNone(links.handle())

        closes = [candle["close"] for candle in candles()[:2]]
        average = sum(closes) / len(closes)
        self.assertEqual(candle_data[-1]["average"], average)

        closes = [candle["close"] for candle in half_day_candles()[:4]]
        average = sum(closes) / len(closes)
        self.assertEqual(half_day_candle_data[-1]["average"], average)

        self.assertIsNone(candle_data.extend(candles()[2:]))
        self.assertIsNone(half_day_candle_data.extend(half_day_candles()[4:]))
        self.assertIsNone(links.handle())

        self.assertIsNone(candle_data[-1].get("average"))

        closes = [candle["close"] for candle in half_day_candles()]
        average = sum(closes) / len(closes)
        self.assertEqual(half_day_candle_data[-1]["average"], average)
