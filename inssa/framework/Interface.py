from typing import Optional, Final, Callable, List, Any

from ..library import OrderedDictList, Trace, LOOP, RAISE


_TRACE: Final = Trace("Interface", group="Framework")


class Interface:
    def __init__(self, *, name: Optional[str] = None):
        self._prefix = f"{name}/" if name else ""

        self._interfaces = OrderedDictList(
            "command",
            name="Interfaces" + (f".{name}" if name else ""),
        )

    def __str__(self) -> str:
        return f"Interface({self._prefix}count:{len(self._interfaces)})"

    def print(self, trace: Optional[Callable] = None) -> None:
        not trace and (trace := _TRACE.INFO)
        trace(self)
        LOOP(
            trace(f"    - {interface['command']}")
            for interface in self._interfaces
            if not interface["internal"]
        )

    def commands(self) -> List[str]:
        return self._interfaces.values()

    def register(self, command: str, func: Callable, *, internal: bool = False) -> None:
        (
            self._interfaces.get(command)
            and _TRACE.CRITICAL((message := f"register failed, {command} is already registered"))
            and not self.print(_TRACE.CRITICAL)
            and RAISE(ValueError, message)
        )

        self._interfaces.append({"command": command, "func": func, "internal": internal})

    def remove(self, command: str) -> None:
        (
            not (interface := self._interfaces.get(command))
            and _TRACE.CRITICAL((message := f"remove failed, {command} is not registered"))
            and not self.print(_TRACE.CRITICAL)
            and RAISE(ValueError, message)
        )

        self._interfaces.remove(interface)

    def call(self, command: str, *args, **kwargs) -> Any:
        (
            not (interface := self._interfaces.get(command))
            and _TRACE.CRITICAL((message := f"call failed, {command} is not registered"))
            and not self.print(_TRACE.CRITICAL)
            and RAISE(ValueError, message)
        )

        return interface["func"](*args, **kwargs)
