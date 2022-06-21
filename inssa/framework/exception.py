from typing import Final
import sys, os

from ..library import Trace, LOOP


_TRACE: Final = Trace("exception", group="Framework")


def exception(*, terminate: bool = False) -> None:
    TRACE = _TRACE.CRITICAL

    exc_type, exc_value, exc_traceback = sys.exc_info()
    ts = []
    while exc_traceback is not None:
        ts.append(exc_traceback)
        exc_traceback = exc_traceback.tb_next

    stacks = [
        [
            str(t.tb_frame.f_code.co_name),
            str(os.path.basename(t.tb_frame.f_code.co_filename)),
            str(t.tb_lineno),
        ]
        for i, t in enumerate(reversed(ts))
    ]
    widths = (
        max([len(stack[0]) for stack in stacks]) + 2,
        max([len(stack[1]) for stack in stacks]),
        max([len(stack[2]) for stack in stacks]),
    )

    TRACE(f"exception {exc_type.__name__} raised for {exc_value}")
    TRACE(f"call stack:")
    LOOP(
        TRACE(
            ("   --" if not index else "     "),
            (stack[0] + "()").ljust(widths[0]),
            "from",
            stack[1].ljust(widths[1]) + ",",
            stack[2].ljust(widths[2]) + " line",
            ("--" if not index else ""),
        )
        for index, stack in enumerate(stacks)
    )

    if terminate:
        sys.exit()
