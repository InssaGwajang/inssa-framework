from typing import Final, List, Dict, Tuple, Union, Optional, Iterable, Callable
from functools import reduce

from ..builtins.builtins import KWARGS, RAISE, LOOP
from ..trace.Trace import Trace
from .DictList import DictList


_TRACE: Final = Trace("Handled", group="Library")


class HandledDictList(DictList):
    def __init__(
        self,
        handles: Iterable[Callable[[Dict, Dict], Dict]],
        initial: Optional[Union[str, List, Tuple]] = None,
        *,
        name: Optional[str] = None,
        type: Optional[str] = None,
        encoding: Optional[str] = None,
        separator: Optional[str] = None,
    ):
        self._trace = _TRACE

        self._handles = handles
        self._handled = 0

        super().__init__(
            **KWARGS(
                initial=initial,
                name=name,
                type=type,
                encoding=encoding,
                separator=separator,
            )
        )

    def __str__(self) -> str:
        return f"HandledDictList({self._prefix}handles:{len(self._handles)}/count:{len(self)})"

    def _handle(self) -> None:
        LOOP(
            reduce(lambda pipe, handle: handle(self._data[index], pipe), self._handles, {})
            for index in range(self._handled, len(self))
        )
        self._handled = len(self)

    def append(self, element: Dict) -> None:
        super().append(element) or self._handle()

    def extend(self, data: List[Dict]) -> None:
        super().extend(data) or self._handle()

    def insert(self, element: Dict, *, index: int = 0) -> None:
        (
            self.CRITICAL((messages := "insert is not possible, data can not be handled"))
            and RAISE(ValueError, messages)
        )

    def remove(self, element: Dict) -> None:
        (
            self.CRITICAL((messages := "remove is not possible, data can not be handled"))
            and RAISE(ValueError, messages)
        )

    def pop(self, index: Optional[int] = 0) -> Dict:
        (
            self.CRITICAL((messages := "pop is not possible, data can not be handled"))
            and RAISE(ValueError, messages)
        )

    def clear(self) -> None:
        (
            self.CRITICAL((messages := "clear is not possible, data can not be handled"))
            and RAISE(ValueError, messages)
        )
