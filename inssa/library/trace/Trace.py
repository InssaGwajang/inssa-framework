from typing import Final, Dict, List, Optional, Callable, Iterable
from functools import partial
import logging, os, datetime


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
    _TRACES: List = []

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

        any(trace._initialize() for trace in Trace._TRACES)

    @staticmethod
    def set_group(
        name: str,
        *,
        terminal: Optional[str] = None,
        file: Optional[str] = None,
    ) -> None:
        Trace._GROUPS[name] = _Stream(terminal, file)

        any(trace._initialize() for trace in Trace._TRACES if trace._group == name)

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

        self._initialize()
        Trace._TRACES.append(self)

    def _initialize(self) -> None:
        stream = Trace._GROUPS.get(self._group, self._stream)

        for level in _LEVELS:
            if handlers := [
                getattr(_Handler, type)()
                for type in ("terminal", "file")
                if getattr(Trace._STREAM, f"_{type}") != "NONE"
                and _LEVELS[getattr(Trace._STREAM, f"_{type}")] <= _LEVELS[level]
                and getattr(stream, f"_{type}") != "NONE"
                and _LEVELS[getattr(stream, f"_{type}")] <= _LEVELS[level]
            ]:
                setattr(self, f"_{level}s", handlers)
                setattr(self, level, partial(self._trace, level))

            else:
                setattr(self, level, lambda *_: False)

    def _trace(self, level: str, *args) -> bool:
        for handler in getattr(self, f"_{level}s"):
            handler(
                f"[{self._group:10s}][{self._name:10s}][{level:8s}] "
                + " ".join([str(arg) for arg in args])
            )

        return True

    def CRITICAL(self, *_) -> bool:
        return False

    def ERROR(self, *_) -> bool:
        return False

    def WARNING(self, *_) -> bool:
        return False

    def INFO(self, *_) -> bool:
        return False

    def DEBUG(self, *_) -> bool:
        return False


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

        directory_path = os.path.dirname(Trace._STREAM._file_path)
        not os.path.exists(directory_path) and os.makedirs(directory_path)

        handler = logging.FileHandler(Trace._STREAM._file_path)
        handler.setFormatter(logging.Formatter(_Handler._FORMAT))
        logger.addHandler(handler)

        logger.propagate = False

        _Handler._file = logger.info
        _Handler.file = lambda: _Handler._file
        return _Handler._file
