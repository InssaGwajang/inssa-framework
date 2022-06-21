from typing import Final, Iterable, Optional
from cmd import Cmd
from threading import Thread
from queue import Queue

from .Component import Component
from .Interface import Interface
from .exception import exception
from ..library import DictList, Trace, KWARGS, LOOP


_TRACE: Final = Trace("console", group="Framework")


def console(
    *,
    components: Iterable[Component] = [],
    group: Optional[str] = None,
    terminal: Optional[str] = None,
    file: Optional[str] = None,
):
    console._interface = Interface(name="console")

    console._request = Queue()
    console._response = Queue()

    components = [
        component(
            interface=console._interface,
            **KWARGS(
                group=group,
                terminal=terminal,
                file=file,
            ),
        )
        for component in components
    ]
    LOOP(component.initialize() for component in components)

    Thread(target=_Prompt().cmdloop).start()
    while True:
        command, args = console._request.get()

        if command == "finalize":
            console._response.put("exit")
            break

        else:
            try:
                res = console._interface.call(command, *args)

            except Exception:
                res = exception()

            console._response.put(res)

    LOOP(component.finalize() for component in components)


def _request(command: str, *args):
    console._request.put((command, args))
    return console._response.get()


class _Prompt(Cmd):
    prompt = f"] ".rjust(60)

    def preloop(self):
        self.INFO = _TRACE.INFO
        self.help()

    def precmd(self, args):
        if len((inputs := args.split())) == 1 and inputs[0] == "exit":
            return _request("finalize")

        elif len(inputs) == 1 and inputs[0] == "help":
            self.help()

        elif len(inputs) > 0:
            self.INFO(f"{' '.join(inputs)} = {_request(inputs[0], *inputs[1:])}")

        return ""

    def help(self):
        console._interface.print(trace=self.INFO)

    def do_exit(self, _):
        return True
