from typing import Optional, Final, Callable, List, Any
from functools import partial

from ..library import OrderedDictList, Trace, LOOP, RAISE


_TRACE: Final = Trace("Interface", group="Framework")


class Interface:
    def __init__(self, *, name=Optional[str]):
        self._name = name if name else "-"

        self.CRITICAL = partial(_TRACE.CRITICAL, f"[{self._name}]")
        self.DEBUG = partial(_TRACE.DEBUG, f"[{self._name}]")

        self._interfaces = OrderedDictList("command", name=f"Interfaces.{self._name}")

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
