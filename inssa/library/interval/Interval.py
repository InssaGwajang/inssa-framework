from typing import Union, Final, Optional
from functools import partial
import time

from ..trace.Trace import Trace


_TRACE: Final = Trace("Interval", group="Library")


class Interval:
    def __init__(
        self,
        interval: Union[float, int],
        *,
        name: Optional[str] = None,
    ):
        self._name = name if name else "-"
        self._interval = interval

        self.DEBUG = partial(_TRACE.DEBUG, f"[{self._name}]") if name else _TRACE.DEBUG

        self._record = time.time() - 86400  # 24 hours * 60 minutes * 60 seconds

    def start(self) -> float:
        (
            (delay := self._interval - (time.time() - self._record)) > 0
            and self.DEBUG(f"interval delay {delay} seconds")
            and time.sleep(delay)
        )
        self._record = time.time()

        return delay if delay > 0 else 0
