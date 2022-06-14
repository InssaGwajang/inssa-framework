from typing import Dict, Callable, Union, Iterable, Any


def kwargs(**kwargs) -> Dict:
    return {key: value for key, value in kwargs.items() if value is not None}


def execute(
    exception: Union[Exception, Iterable[Exception]],
    func: Callable,
    *args,
    **kwargs,
) -> Any:
    try:
        return func(*args, **kwargs)

    except exception:
        pass
