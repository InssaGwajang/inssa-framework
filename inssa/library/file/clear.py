from typing import Optional, Iterable, Callable
import os
from shutil import rmtree
from ..trace.Trace import Trace
from ..builtin.builtins import call


def clear(
    root: str = os.getcwd(),
    keywords: Optional[Iterable[str]] = None,
) -> None:
    keywords is None and (
        keywords := (
            "tempCodeRunnerFile.py",  # vscode code-runner cache
            "__pycache__",  # python cache
            ".pytest_cache",  # pytest cache
        )
    )

    TRACE = Trace("clear", group="Library").DEBUG

    TRACE(f"clear")
    TRACE(f"    root: {root}")
    TRACE(f"    keywords: {', '.join(keywords)}")

    directories = [
        os.path.join(top, directory)
        for top, directories, _ in os.walk(root)
        for directory in directories
        for keyword in keywords
        if keyword in directory
    ]
    files = [
        os.path.join(top, file)
        for top, _, files in os.walk(root)
        for file in files
        for keyword in keywords
        if keyword in file
    ]

    TRACE(f"{len(directories)} directories, {len(files)} files from {len(keywords)} keywords")
    any(TRACE(f"    {path}") for path in directories + files)

    any(call(rmtree, FileNotFoundError, directory) for directory in directories)
    any(call(os.remove, FileNotFoundError, file) for file in files)
