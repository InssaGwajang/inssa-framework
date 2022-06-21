from typing import Optional, Final, Callable, List, Any
from functools import partial

from ..library import OrderedDictList, Trace, LOOP, RAISE


_TRACE: Final = Trace("Interface", group="Framework")


class Interface:
    def __init__(self, *, name: Optional[str] = None):
        self._name = name if name else "-"

        self.CRITICAL = partial(_TRACE.CRITICAL, f"[{self._name}]")
        self.INFO = partial(_TRACE.INFO, f"[{self._name}]")

        self._interfaces = OrderedDictList("command", name=f"Interfaces.{self._name}")

    def __str__(self) -> str:
        return f"Interface({self._name}/count:{len(self._interfaces)})"
        LOOP(trace(f"    - {index}: {element}") for index, element in enumerate(self))

    def print(self, trace: Optional[Callable] = None) -> None:
        not trace and (trace := self.INFO)
        trace(self)
        LOOP(trace(f"    {interface['command']}") for interface in self._interfaces)

    def commands(self) -> List[str]:
        return self._interfaces.values()

    def register(self, command: str, func: Callable) -> None:
        (
            self._interfaces.get(command)
            and self.CRITICAL((messages := f"register failed, {command} is already registered"))
            and RAISE(ValueError, messages)
        )

        self._interfaces.append({"command": command, "func": func})

    def remove(self, command: str) -> None:
        (
            not (interface := self._interfaces.get(command))
            and self.CRITICAL((messages := f"remove failed, {command} is not registered"))
            and RAISE(ValueError, messages)
        )

        self._interfaces.remove(interface)

    def call(self, command: str, *args, **kwargs) -> Any:
        (
            not (interface := self._interfaces.get(command))
            and self.CRITICAL((messages := f"call failed, {command} is not registered"))
            and RAISE(ValueError, messages)
        )

        return interface["func"](*args, **kwargs)
