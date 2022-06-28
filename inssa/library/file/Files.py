from typing import Final, Optional, List, Dict, Any, Callable
from functools import reduce
from importlib import import_module
import os, json

from ..builtins.builtins import RAISE
from ..data.OrderedDictList import OrderedDictList
from ..trace.Trace import Trace


_TRACE: Final = Trace("Files", group="Library")


class Files:
    def __init__(self, root: str, *, name: Optional[str] = None):
        self._prefix = f"{name}/" if name else ""

        root = os.path.realpath(root)
        modules = os.getcwd() in root

        self._files = OrderedDictList(
            key="file",
            initial=[
                {
                    "file": (
                        os.path.join(path, file).replace(root, "")[1:]
                        if not (extension := os.path.splitext(file)[1])
                        else os.path.join(path, file).replace(root, "")[1:].replace(extension, "")
                    ).replace(os.path.sep, "."),
                    "path": os.path.join(path, file),
                    "modules": (
                        os.path.join(path, file)
                        .replace(os.getcwd(), "")[1:][:-3]
                        .replace(os.path.sep, ".")
                        if modules
                        else ""
                    ),
                }
                for path, _, files in os.walk(root)
                for file in files
            ],
            name=f"Files" + (f".{name}" if name else ""),
        )

    def __str__(self) -> str:
        return f"Files({self._prefix}count:{len(self._files)})"

    def print(self, trace: Optional[Callable] = None) -> None:
        not trace and (trace := _TRACE.INFO)
        trace(self)
        self._files.print(trace=trace, all=True)

    def files(self) -> List[str]:
        return self._files.values()

    def module(self, file: str, module: str) -> Any:
        (
            not (f := self._files.get(file))
            and _TRACE.CRITICAL((message := f"module failed, {file} is not exist"))
            and not self.print(_TRACE.CRITICAL)
            and RAISE(ValueError, message)
        )

        isinstance(f["modules"], str) and f.update({"modules": import_module(f["modules"])})
        return getattr(f["modules"], module)

    def json(self, file: str, *, encoding: str = "UTF-8-sig") -> Any:
        (
            not (f := self._files.get(file))
            and _TRACE.CRITICAL((message := f"json failed, {file} is not exist"))
            and not self.print(_TRACE.CRITICAL)
            and RAISE(ValueError, message)
        )

        with open(f["path"], "r", encoding="UTF-8-sig") as file:
            return json.load(file)
