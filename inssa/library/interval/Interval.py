from typing import Union
import time


class Interval:
    def __init__(self, interval: Union[float, int]):
        self._interval = interval
        self._record = time.time() - 86400  # 24 hours * 60 minutes * 60 seconds

    def start(self) -> float:
        (delay := self._interval - (time.time() - self._record)) > 0 and time.sleep(delay)
        self._record = time.time()

        return delay if delay > 0 else 0
