from typing import Dict, Union, Final, Optional
from functools import partial
import os, time

from ..trace.Trace import Trace
from ..data.DictList import DictList


_TRACE: Final = Trace("Intervals", group="Library")


class Intervals:
    def __init__(
        self,
        intervals: Dict[Union[int, float], int],
        file: Union[bool, str] = False,
        *,
        name: Optional[str] = None,
    ):
        self.DEBUG = partial(_TRACE.DEBUG, f"[{name}]") if name else _TRACE.DEBUG

        self._file = (
            os.path.join(
                os.getcwd(),
                "files",
                "intervals",
                "Intervals" + (f".{name}" if name else "") + ".DictList",
            )
            if isinstance(file, bool) and file
            else file
        )

        self._intervals = DictList(name="Intervals" + (f".{name}" if name else ""))
        self._file and self._intervals.read(self._file, type="DictList")
        not self._intervals and self._intervals.extend(
            [
                {"interval": interval, "count": count, "records": []}
                for interval, count in intervals.items()
            ]
        )

    def leave(self) -> float:
        total = 0
        for interval in self._intervals:
            interval["records"] = [
                record
                for record in interval["records"]
                if interval["interval"] - (time.time() - record) > 0
            ]
            (
                len(interval["records"]) == interval["count"]
                and (delay := interval["interval"] - (time.time() - interval["records"].pop(0))) > 0
                and (total := total + delay)
            )
            interval["records"].append(time.time())

        total and self.DEBUG(f"intervals delay total {total} seconds") and time.sleep(total)
        self._file and self._intervals.write(self._file, type="DictList")

        return total
