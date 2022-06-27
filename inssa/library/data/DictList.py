from typing import Final, List, Dict, Tuple, Union, Optional, Callable, Iterable, Any
from functools import partial, reduce
from collections import OrderedDict
import os, pickle, csv, json

from ..builtins.builtins import KWARGS, LOOP
from ..trace.Trace import Trace


_TRACE: Final = Trace("DictList", group="Library")

_TYPES: Final = ("DictList", "csv", "json")


class DictList:
    def __init__(
        self,
        initial: Optional[Union[str, List, Tuple]] = None,
        *,
        name: Optional[str] = None,
        type: Optional[str] = None,
        encoding: Optional[str] = None,
        separator: Optional[str] = None,
    ):
        trace = getattr(self, "_trace", _TRACE)
        self.CRITICAL = partial(trace.CRITICAL, f"[{name}]") if name else trace.CRITICAL
        self.WARNING = partial(trace.WARNING, f"[{name}]") if name else trace.WARNING
        self.INFO = partial(trace.INFO, f"[{name}]") if name else trace.INFO
        self.DEBUG = partial(trace.DEBUG, f"[{name}]") if name else trace.DEBUG
        self._prefix = f"{name}/" if name else ""

        self._data = []

        (
            isinstance(initial, str)
            and self.DEBUG(f"init from file, {initial}")
            and self.read(
                initial,
                **KWARGS(type=type, encoding=encoding, separator=separator),
            )
        )
        (
            isinstance(initial, (list, tuple))
            and self.DEBUG(f"init from data, count is {len(initial)}")
            and self.extend(initial)
        )

    def __len__(self) -> int:
        return len(self._data)

    def __iter__(self):
        self._index = 0

        return self

    def __next__(self) -> Dict:
        try:
            element = self[self._index]
            self._index += 1

            return element

        except IndexError:
            del self._index

            raise StopIteration

    def __getitem__(self, attr: Union[slice, int], /) -> Optional[Union[List, Dict]]:
        return (
            [self._data[attr] for attr in range(*attr.indices(len(self)))]
            if isinstance(attr, slice)
            else self._data[attr]
        )

    def __str__(self) -> str:
        return f"DictList({self._prefix}count:{len(self)})"

    def print(self, trace: Optional[Callable] = None) -> None:
        not trace and (trace := self.INFO)
        trace(self)

        if len(self) <= 6:
            LOOP(trace(f"    {index}: {element}") for index, element in enumerate(self))

        else:
            LOOP(trace(f"    {index}: {self[index]}") for index in (0, 1, 2))
            trace("    ...")
            LOOP(trace(f"    {len(self) + index}: {self[index]}") for index in (-3, -2, -1))

    def get(
        self,
        attr1: Union[str, Dict, List, Tuple] = None,
        attr2: Optional[Any] = None,
        /,
    ) -> Optional[Dict]:
        if attr1 is None:
            return self._data[-1] if len(self._data) else None

        elif attr2 is not None:  # attr1: key, attr2: value
            for element in self._data:
                if attr1 in element and element[attr1] == attr2:
                    return element

        elif isinstance(attr1, dict):  # attr1: queries: Dict[str, Any]
            for element in self._data:
                if all([(k in element and element[k] == v) for k, v in attr1.items()]):
                    return element

        elif isinstance(attr1, (list, tuple)):  # attr1: queries: Iterable[List[str, Any]]
            for element in self._data:
                if all([(k in element and element[k] == v) for k, v in attr1]):
                    return element

    def items(
        self,
        attr1: Union[str, Dict, List, Tuple] = None,
        attr2: Optional[Any] = None,
        /,
    ):  # -> DictList
        if attr1 is None:
            return DictList(self._data)

        elif attr2 is not None:  # attr1: key, attr2: value
            return DictList([e for e in self._data if attr1 in e and e[attr1] == attr2])

        elif isinstance(attr1, dict):  # attr1: queries: Dict[str, Any]
            return DictList(
                [
                    element
                    for element in self._data
                    if all([(k in element and element[k] == v) for k, v in attr1.items()])
                ]
            )

        elif isinstance(attr1, (list, tuple)):  # attr1: queries: Iterable[List[str, Any]]
            return DictList(
                [
                    element
                    for element in self._data
                    if all([(k in element and element[k] == v) for k, v in attr1])
                ]
            )

        return DictList()

    def values(self, key: str, *, overlap: bool = True, sort: bool = False) -> List:
        values = [element[key] for element in self._data if key in element]

        not overlap and (values := list(OrderedDict.fromkeys(values)))
        sort and values.sort()

        return values

    def append(self, element: Dict) -> None:
        self._data.append(element)

    def extend(self, data: List[Dict]) -> None:
        self._data.extend(data)

    def insert(self, element: Dict, *, index: int = 0) -> None:
        self._data.insert(index, element)

    def remove(self, element: Dict) -> None:
        self._data.remove(element)

    def pop(self, index: Optional[int] = 0) -> Dict:
        return self._data.pop(index)

    def clear(self) -> None:
        self._data.clear()

    def read(
        self,
        source: str,
        *,
        type: Optional[str] = None,  # DictList, json, csv
        encoding: str = "UTF-8-sig",
        separator: str = ",",
    ) -> bool:
        if (not os.path.exists(source) and self.WARNING(f"read failed, no source, {source}")) or (
            (type := type if type else os.path.splitext(source)[1][1:]) not in _TYPES
            and self.WARNING(f"read failed, invalid type, {type}")
        ):
            return False

        if type == "DictList":
            with open(source, "rb") as file:
                self.extend(pickle.load(file))

        elif type == "json":
            with open(source, "r", encoding=encoding) as file:
                self.extend(json.load(file))

        elif type == "csv":
            with open(source, "r", encoding=encoding) as file:
                (
                    len(data := [line for line in csv.reader(file, delimiter=separator)]) > 1
                    and (keys := [value for value in data[0]])
                    and self.extend(
                        [
                            {key: line[index] for index, key in enumerate(keys) if line[index]}
                            for line in data[1:]
                        ]
                    )
                )

        (
            (
                (exist := len(self) != 0)
                and self.DEBUG(f"read success from {source}, {len(self)} elements")
            )
            or self.WARNING(f"read failed, no data")
        )
        return exist

    def write(
        self,
        target: str,
        *,
        type: Optional[str] = None,  # DictList, json, csv
        encoding: str = "UTF-8-sig",
    ) -> bool:
        if (not len(self) and self.WARNING(f"write failed, no data")) or (
            (type := type if type else os.path.splitext(target)[1][1:]) not in _TYPES
            and self.WARNING(f"write failed, invalid type, {type}")
        ):
            return False

        (
            not os.path.exists((path := os.path.dirname(os.path.abspath(target))))
            and self.DEBUG(f"make directory, {path}")
            and os.makedirs(path)
        )

        if type == "DictList":
            with open(target, "wb") as file:
                pickle.dump(self._data, file)

        elif type == "json":
            with open(target, "w", encoding=encoding) as file:
                json.dump(self._data, file, ensure_ascii=False, indent="\t\t")

        elif type == "csv":
            with open(target, "w", encoding=encoding, newline="\n") as file:
                csv_writer = csv.DictWriter(
                    file,
                    reduce(
                        lambda keys, element: list(
                            OrderedDict.fromkeys(keys + list(element.keys()))
                        ),
                        self._data,
                        [],
                    ),
                )
                csv_writer.writeheader()
                csv_writer.writerows(self._data)

        self.DEBUG(f"write success {len(self)} elements to {target}")
        return True
