from typing import Final, List, Dict, Tuple, Union, Optional, Any

from ..builtins.builtins import KWARGS, RAISE
from ..trace.Trace import Trace
from .DictList import DictList


_TRACE: Final = Trace("Ordered", group="Library")


class OrderedDictList(DictList):
    def __init__(
        self,
        key: str,
        initial: Optional[Union[str, List, Tuple]] = None,
        *,
        name: Optional[str] = None,
        type: Optional[str] = None,
        encoding: Optional[str] = None,
        separator: Optional[str] = None,
    ):
        self._trace = _TRACE

        self._key = key
        self._sort = lambda: self._data.sort(key=lambda element: element[self._key])

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
        return f"OrderedDictList({self._prefix}key:{self._key}/count:{len(self)})"

    def get(
        self,
        attr1: Union[str, Dict, List, Tuple] = None,
        attr2: Optional[Any] = None,
        /,
    ) -> Optional[Dict]:
        if attr2 is None and attr1 and not isinstance(attr1, (dict, list, tuple)):
            left, right = 0, len(self._data) - 1
            while left <= right:
                if self._data[(index := (left + right) // 2)][self._key] > attr1:
                    right = index - 1

                elif self._data[index][self._key] < attr1:
                    left = index + 1

                else:
                    return self._data[index]

        else:
            return super().get(attr1, attr2)

    def items(
        self,
        attr1: Union[str, Dict, List, Tuple] = None,
        attr2: Optional[Any] = None,
        /,
    ) -> DictList:
        return (
            DictList([element for element in self._data if element[self._key] == attr1])
            if attr2 is None and attr1 and not isinstance(attr1, (dict, list, tuple))
            else super().items(attr1, attr2)
        )

    def values(
        self,
        key: Optional[str] = None,
        overlap: Optional[bool] = None,
        sort: Optional[bool] = None,
    ) -> List:
        return super().values(key if key else self._key, **KWARGS(overlap=overlap, sort=sort))

    def append(self, element: Dict) -> None:
        super().append(element) or self._sort()

    def extend(self, data: List[Dict]) -> None:
        super().extend(data) or self._sort()

    def insert(self, element: Dict, *, index: int = 0) -> None:
        (
            self.CRITICAL((message := "insert failed, data should be sorted"))
            and RAISE(ValueError, message)
        )
