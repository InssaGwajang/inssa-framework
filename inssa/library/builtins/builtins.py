from typing import Dict, Callable, Union, Iterable, Any, Optional


def KWARGS(**kwargs) -> Dict:
    return {key: value for key, value in kwargs.items() if value is not None}


def PARAMS(**kwargs) -> Optional[Dict]:
    return (
        params
        if (params := {key: value for key, value in kwargs.items() if value is not None})
        else None
    )


def GETATTR(o, n: str, f: Callable, *args, **kwargs) -> Any:
    not hasattr(o, n) and setattr(o, n, f(*args, **kwargs))

    return getattr(o, n)


def CALL(
    func: Callable,
    *args,
    passes: Union[Exception, Iterable[Exception]] = [],
    **kwargs,
) -> Any:
    try:
        return func(*args, **kwargs)

    except passes:
        pass


def RAISE(exception: Exception, message: str):
    raise exception(message)


def LOOP(iterable: Iterable):
    for _ in iterable:
        pass
