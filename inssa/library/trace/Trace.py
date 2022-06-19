from typing import Final, Dict, List, Optional, Callable
from functools import partial
import logging, os, datetime

from ..builtins.builtins import LOOP


_LEVELS: Final = {
    "CRITICAL": 50,
    "ERROR": 40,
    "WARNING": 30,
    "INFO": 20,
    "DEBUG": 10,
    # NONE: no stream
}


class _Stream:
    def __init__(
        self,
        terminal: Optional[str] = None,
        file: Optional[str] = None,
        file_path: Optional[str] = None,
    ):
        self._terminal = terminal if terminal else "INFO"
        self._file = file if file else "DEBUG"
        self._file_path = (
            file_path
            if file_path
            else os.path.join(
                os.getcwd(),
                "files",
                "traces",
                datetime.datetime.now().strftime("%Y-%m-%d"),
                datetime.datetime.now().strftime("%H-%M-%S.trace"),
            )
        )


class Trace:
    _STREAM: _Stream = _Stream("INFO", "NONE")

    _GROUPS: Dict = {}
    _TRACES: Dict = {}

    _OBJECTS: List = []

    @staticmethod
    def set_stream(
        *,
        terminal: Optional[str] = None,
        file: Optional[str] = None,
        file_path: Optional[str] = None,
    ) -> None:
        terminal and setattr(Trace._STREAM, "_terminal", terminal)
        file and setattr(Trace._STREAM, "_file", file)
        file_path and setattr(Trace._STREAM, "_file_path", file_path)

        LOOP(trace._set_handlers() for trace in Trace._OBJECTS)

    @staticmethod
    def set_trace(
        name: str,
        *,
        terminal: Optional[str] = None,
        file: Optional[str] = None,
    ) -> None:
        Trace._TRACES[name] = _Stream(terminal, file)

        LOOP(trace._set_handlers() for trace in Trace._OBJECTS if trace._name == name)

    @staticmethod
    def set_group(
        name: str,
        *,
        terminal: Optional[str] = None,
        file: Optional[str] = None,
    ) -> None:
        Trace._GROUPS[name] = _Stream(terminal, file)

        LOOP(trace._set_handlers() for trace in Trace._OBJECTS if trace._group == name)

    def __init__(
        self,
        name: str,
        *,
        group: Optional[str] = None,
        terminal: Optional[str] = None,
        file: Optional[str] = None,
    ):
        self._name = name
        self._group = group if group else ""
        self._stream = _Stream(terminal, file)

        self._set_handlers()

        # NOTE: trace functions are exchanged in initialization phase
        LOOP(setattr(self, level, partial(self._TRACE, level)) for level in _LEVELS)

        Trace._OBJECTS.append(self)

    def _set_handlers(self) -> None:
        stream = Trace._TRACES.get(self._name, Trace._GROUPS.get(self._group, self._stream))
        LOOP(
            setattr(
                self,
                f"_{level}S",
                [
                    getattr(_Handler, type)()
                    for type in ("terminal", "file")
                    if getattr(Trace._STREAM, f"_{type}") != "NONE"
                    and _LEVELS[getattr(Trace._STREAM, f"_{type}")] <= _LEVELS[level]
                    and getattr(stream, f"_{type}") != "NONE"
                    and _LEVELS[getattr(stream, f"_{type}")] <= _LEVELS[level]
                ],
            )
            for level in _LEVELS
        )

    def CRITICAL(self, *args) -> True:
        return True

    def ERROR(self, *args) -> True:
        return True

    def WARNING(self, *args) -> True:
        return True

    def INFO(self, *args) -> True:
        return True

    def DEBUG(self, *args) -> True:
        return True

    def _TRACE(self, level: str, *args) -> True:
        for handler in getattr(self, f"_{level}S"):
            message = f"[{self._group:10s}][{self._name:10s}][{level:8s}] {' '.join((str(arg) for arg in args))}"
            handler(message)

        return True


class _Handler:
    _FORMAT = "[%(asctime)s]%(message)s"

    @staticmethod
    def terminal() -> Callable:
        logger = logging.getLogger("terminal")
        logger.setLevel(logging.INFO)

        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(_Handler._FORMAT))
        logger.addHandler(handler)

        logger.propagate = False

        _Handler._terminal = logger.info
        _Handler.terminal = lambda: _Handler._terminal
        return _Handler._terminal

    @staticmethod
    def file() -> Callable:
        logger = logging.getLogger("file")
        logger.setLevel(logging.INFO)

        directory_path = os.path.dirname(os.path.abspath(Trace._STREAM._file_path))
        not os.path.exists(directory_path) and os.makedirs(directory_path)

        handler = logging.FileHandler(Trace._STREAM._file_path)
        handler.setFormatter(logging.Formatter(_Handler._FORMAT))
        logger.addHandler(handler)

        logger.propagate = False

        _Handler._file = logger.info
        _Handler.file = lambda: _Handler._file
        return _Handler._file
