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
import os

from inssa.library import clear


class TestClear(TestCase):
    def setUp(self):
        self._directory = TemporaryDirectory()
        self._root = self._directory.name

    def tearDown(self):
        self._directory.cleanup()

    def test_clear(self):
        cache_directories = (
            os.path.join(self._root, "__pycache__"),
            os.path.join(self._root, "__pycache__", "files"),
            os.path.join(self._root, "__pycache__", "__pycache__"),
            os.path.join(self._root, ".pytest_cache"),
        )
        cache_files = (
            os.path.join(self._root, "tempCodeRunnerFile.py"),
            os.path.join(self._root, "__pycache__", "tempCodeRunnerFile.py"),
            os.path.join(self._root, "__pycache__", "file.file"),
            os.path.join(self._root, ".pytest_cache", "file.file"),
        )

        directories = (
            os.path.join(self._root, "files"),
            os.path.join(self._root, "files", "traces"),
        )
        files = (
            os.path.join(self._root, "trace.file"),
            os.path.join(self._root, "files", "store.file"),
        )

        for path in cache_directories + directories:
            os.makedirs(path)

        for path in cache_files + files:
            with open(path, "w"):
                pass

        clear(self._root)

        for path in cache_directories + cache_files:
            self.assertFalse(os.path.exists(path))

        for path in directories + files:
            self.assertTrue(os.path.exists(path))

    def test_clear_keywords(self):
        cache_directories = (
            os.path.join(self._root, "__cache__"),
            os.path.join(self._root, "__cache__", "files"),
            os.path.join(self._root, "__cache__", "__cache__"),
            os.path.join(self._root, ".cache"),
        )
        cache_files = (
            os.path.join(self._root, "temporary.file"),
            os.path.join(self._root, "__cache__", "cache.py"),
            os.path.join(self._root, "__cache__", "file.file"),
            os.path.join(self._root, ".cache", "file.file"),
        )

        directories = (
            os.path.join(self._root, "files"),
            os.path.join(self._root, "files", "traces"),
        )
        files = (
            os.path.join(self._root, "trace.file"),
            os.path.join(self._root, "files", "store.file"),
        )

        for path in cache_directories + directories:
            os.makedirs(path)

        for path in cache_files + files:
            with open(path, "w"):
                pass

        clear(self._root, ("cache", "temporary.file"))

        for path in cache_directories + cache_files:
            self.assertFalse(os.path.exists(path))

        for path in directories + files:
            self.assertTrue(os.path.exists(path))
