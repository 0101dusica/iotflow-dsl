import time
from functools import wraps
from typing import Callable, TypeVar, ParamSpec, Tuple

T = TypeVar("T")
P = ParamSpec("P")


def timed(func: Callable[P, T]) -> Callable[P, Tuple[T, float]]:
    """
    Decorator that measures execution time.
    Returns: (original_result, duration_seconds)
    """

    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> Tuple[T, float]:
        start = time.perf_counter()
        result = func(*args, **kwargs)
        duration = time.perf_counter() - start
        return result, duration

    return wrapper
