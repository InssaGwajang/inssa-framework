from typing import Optional, Iterable, Callable
import os
from shutil import rmtree
from ..trace.Trace import Trace


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
    all(TRACE(f"    {path}") for path in directories + files)

    any(_remove(directory, remove=rmtree) for directory in directories)
    any(_remove(file, remove=os.remove) for file in files)


def _remove(path: str, *, remove: Callable) -> None:
    try:
        remove(path)

    except FileNotFoundError:
        pass
