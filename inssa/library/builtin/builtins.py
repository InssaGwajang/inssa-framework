from typing import Dict, Callable, Union, Iterable


def kwargs(**kwargs) -> Dict:
    return {key: value for key, value in kwargs.items() if value is not None}


def call(func: Callable, passes: Union[Exception, Iterable[Exception]], *args, **kwargs) -> None:
    try:
        func(*args, **kwargs)

    except passes:
        pass
