from typing import Optional

from .Interface import Interface
from ..library import Trace, KWARGS, LOOP


class Component:
    def __init__(
        self,
        group: Optional[str] = None,
        terminal: Optional[str] = None,
        file: Optional[str] = None,
        interface: Optional[Interface] = None,
    ):
        self._interface = interface

        trace = Trace(type(self).__name__, **KWARGS(group=group, terminal=terminal, file=file))
        self.CRITICAL = trace.CRITICAL
        self.ERROR = trace.ERROR
        self.WARNING = trace.WARNING
        self.INFO = trace.INFO
        self.DEBUG = trace.DEBUG

    def initialize(self) -> None:
        LOOP(  # self.commands
            self._interface.register(command, getattr(self, command))
            for command in getattr(self, "commands", [])
        )  # self.interfaces
        LOOP(
            self._interface.register(interface, getattr(self, interface), internal=True)
            for interface in getattr(self, "interfaces", [])
        )

    def finalize(self) -> None:
        pass

    def call(self, command: str, *args, **kwargs):
        return self._interface.call(command, *args, **kwargs)
