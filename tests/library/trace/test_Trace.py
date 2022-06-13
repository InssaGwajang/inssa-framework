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

if __name__ == "__main__":
    pytest.main([os.path.realpath(__file__).replace(os.getcwd(), "")[1:]])


from tempfile import TemporaryDirectory
import logging
from inssa.library import Trace


class TestTrace(TestCase):
    @classmethod
    def setUpClass(cls):
        cls._directory = TemporaryDirectory()
        Trace.set_stream(file_path=os.path.join(cls._directory.name, "trace.trace"))

    @classmethod
    def tearDownClass(cls):
        logging.shutdown()
        cls._directory.cleanup()

    def tearDown(self):
        Trace.set_stream(terminal="INFO", file="NONE")
        Trace._GROUPS.clear()
        Trace._TRACES.clear()

    def test_init(self):
        self.assertIsInstance(Trace("a"), Trace)
        self.assertIsInstance(Trace("b", group="Z"), Trace)
        self.assertIsInstance(Trace("c", group="Z", terminal="ERROR"), Trace)
        self.assertIsInstance(Trace("d", group="X", file="INFO"), Trace)
        self.assertIsInstance(Trace("e", group="X", terminal="INFO", file="INFO"), Trace)
        self.assertIsInstance(Trace("f", terminal="CRITICAL"), Trace)
        self.assertIsInstance(Trace("f", terminal="INFO", file="CRITICAL"), Trace)

    def test_set_stream(self):
        a = Trace("a", terminal="CRITICAL")
        b = Trace("b", terminal="ERROR")
        c = Trace("c", terminal="WARNING")
        d = Trace("d")
        e = Trace("e", terminal="DEBUG")
        f = Trace("f", terminal="DEBUG", file="INFO")

        self.assertIsInstance(a, Trace)
        self.assertIsInstance(b, Trace)
        self.assertIsInstance(c, Trace)
        self.assertIsInstance(d, Trace)
        self.assertIsInstance(e, Trace)
        self.assertIsInstance(f, Trace)

        self.assertTrue(a.CRITICAL("CRITICAL"))
        self.assertTrue(b.ERROR("ERROR"))
        self.assertFalse(b.INFO("INFO"))
        self.assertTrue(c.WARNING("WARNING"))
        self.assertTrue(d.INFO("INFO"))
        self.assertTrue(e.INFO("INFO"))
        self.assertFalse(f.DEBUG("DEBUG"))

        self.assertIsNone(Trace.set_stream(terminal="DEBUG"))
        self.assertTrue(a.CRITICAL("CRITICAL"))
        self.assertTrue(b.ERROR("ERROR"))
        self.assertFalse(b.INFO("INFO"))
        self.assertTrue(c.WARNING("WARNING"))
        self.assertTrue(d.INFO("INFO"))
        self.assertTrue(e.INFO("INFO"))
        self.assertTrue(f.DEBUG("DEBUG"))

        self.assertIsNone(Trace.set_stream(terminal="WARNING", file="DEBUG"))
        self.assertTrue(a.CRITICAL("CRITICAL"))
        self.assertTrue(b.ERROR("ERROR"))
        self.assertTrue(b.INFO("INFO"))
        self.assertTrue(c.WARNING("WARNING"))
        self.assertTrue(d.INFO("INFO"))
        self.assertTrue(e.INFO("INFO"))
        self.assertFalse(f.DEBUG("DEBUG"))

        self.assertIsNone(Trace.set_stream(terminal="NONE", file="NONE"))
        self.assertFalse(a.CRITICAL("CRITICAL"))
        self.assertFalse(b.ERROR("ERROR"))
        self.assertFalse(b.INFO("INFO"))
        self.assertFalse(c.WARNING("WARNING"))
        self.assertFalse(d.INFO("INFO"))
        self.assertFalse(e.INFO("INFO"))
        self.assertFalse(f.DEBUG("DEBUG"))

    def test_set_group(self):
        self.assertIsNone(Trace.set_stream(terminal="INFO", file="DEBUG"))

        a = Trace("a", group="Trace", terminal="WARNING", file="DEBUG")
        b = Trace("b", group="Trace", terminal="CRITICAL", file="WARNING")

        self.assertIsInstance(a, Trace)
        self.assertIsInstance(b, Trace)

        self.assertTrue(a.CRITICAL("CRITICAL"))
        self.assertTrue(a.ERROR("ERROR"))
        self.assertTrue(a.WARNING("WARNING"))
        self.assertTrue(a.INFO("INFO"))
        self.assertTrue(a.DEBUG("DEBUG"))
        self.assertTrue(b.CRITICAL("CRITICAL"))
        self.assertTrue(b.ERROR("ERROR"))
        self.assertTrue(b.WARNING("WARNING"))
        self.assertFalse(b.INFO("INFO"))
        self.assertFalse(b.DEBUG("DEBUG"))

        self.assertIsNone(Trace.set_group("Trace", terminal="WARNING", file="CRITICAL"))

        self.assertTrue(a.CRITICAL("CRITICAL"))
        self.assertTrue(a.ERROR("ERROR"))
        self.assertTrue(a.WARNING("WARNING"))
        self.assertFalse(a.INFO("INFO"))
        self.assertFalse(a.DEBUG("DEBUG"))
        self.assertTrue(b.CRITICAL("CRITICAL"))
        self.assertTrue(b.ERROR("ERROR"))
        self.assertTrue(b.WARNING("WARNING"))
        self.assertFalse(b.INFO("INFO"))
        self.assertFalse(b.DEBUG("DEBUG"))
