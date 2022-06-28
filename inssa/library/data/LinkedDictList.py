from typing import Final, List, Dict, Tuple, Union, Optional, Iterable, Callable
from functools import partial, reduce

from ..builtins.builtins import KWARGS, RAISE, LOOP
from ..trace.Trace import Trace
from .DictList import DictList


_TRACE: Final = Trace("Linked", group="Library")

_DATA: Final = 0
_HANDLES: Final = 1
_HANDLED: Final = 2
_PIPE: Final = 3


class LinkedDictList:
    def __init__(
        self,
        key: str,
        links: Dict[DictList, Iterable[Callable[[Dict, Dict], Dict]]],
        handles: Iterable[Callable[[Dict, Dict], Dict]] = None,
        *,
        name: Optional[str] = None,
    ):
        self._prefix = f"{name}/" if name else ""

        self._key = key
        self._links = [[data, handles, 0, {}] for data, handles in links.items()]
        self._handles = handles if handles is not None else []

    def __len__(self) -> int:
        return len(self._links)

    def __iter__(self):
        self._index = 0

        return self

    def __next__(self) -> Dict:
        try:
            link = self._links[self._index][_DATA]
            self._index += 1

            return link

        except IndexError:
            del self._index

            raise StopIteration

    def __getitem__(self, attr: Union[slice, int], /) -> Optional[Union[List, Dict]]:
        return (
            [self._links[attr][_DATA] for attr in range(*attr.indices(len(self)))]
            if isinstance(attr, slice)
            else self._links[attr][_DATA]
        )

    def __str__(self) -> str:
        return f"LinkedDictList({self._prefix}key:{self._key}/links:{len(self)}/handles:{len(self._handles)})"

    def print(self, trace: Optional[Callable] = None) -> None:
        not trace and (trace := _TRACE.INFO)
        trace(self)
        LOOP(
            trace(f"    {index}: {link[_DATA]}/handles:{len(link[_HANDLES])}")
            for index, link in enumerate(self._links)
        )

    def handle(self) -> None:
        for index, element_index, _ in sorted(
            [
                (index, link[_HANDLED] + element_index, element[self._key])
                for index, link in enumerate(self._links)
                for element_index, element in enumerate(link[_DATA][link[_HANDLED] :])
                if element[self._key] <= self._links[-1][_DATA][-1][self._key]
            ],
            key=lambda target: (target[2], target[0]),
        ):
            self._links[index][_PIPE] = reduce(
                lambda pipe, handle: handle(self._links[index][_DATA][element_index], pipe),
                self._links[index][_HANDLES],
                self._links[index - 1][_PIPE] if index else {},
            )
            self._links[index][_HANDLED] += 1

            if index == len(self) - 1 and self._handles:
                reduce(
                    lambda pipe, handle: handle(self._links[index][_DATA][element_index], pipe),
                    self._handles,
                    self._links[index][_PIPE],
                )
