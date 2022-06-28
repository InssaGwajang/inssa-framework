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
from random import choice
import datetime

from inssa.library import KRX


class TestKRX(TestCase):
    def test_init(self):
        self.assertIsInstance(KRX(), KRX)

    def test_markets(self):
        self.assertTrue(KRX.markets())

    def test_codes(self):
        self.assertTrue(KRX.codes())
        self.assertTrue(KRX.codes("KOSPI"))
        self.assertTrue(KRX.codes("KOSPI", active=False))

    def test_asset(self):
        self.assertEqual(KRX.asset("005930")["name"], "삼성전자")
        self.assertIsNone(KRX.asset("005050"))

    def test_assets(self):
        self.assertNotEqual(len(KRX.assets()), 0)
        self.assertNotEqual(len(KRX.assets("KOSDAQ")), 0)
        self.assertNotEqual(len(KRX.assets("KOSDAQ", active=True)), 0)

    def test_market_quotations(self):
        self.assertNotEqual(
            len(
                KRX.market_quotations(
                    choice(KRX.markets()),
                    target=datetime.datetime(2016, 3, 4),
                )
            ),
            0,
        )

    def test_asset_quotations(self):
        self.assertNotEqual(
            len(
                KRX.asset_quotations(
                    "005930",
                    start=datetime.datetime(2010, 1, 1),
                    end=datetime.datetime(2010, 2, 15),
                )
            ),
            0,
        )
