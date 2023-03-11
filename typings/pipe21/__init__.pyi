__version__: str = ...


from collections.abc import Callable
from typing import Generic
from typing import TypeVar

T = TypeVar('T')
U = TypeVar('U')

class Pipe(Generic[T, U]):
    def __init__(self, f: Callable[[T], U]) -> None:
        ...
        # self.f = f

    def __ror__(self, x: T) -> U: ...


def f(x: int) -> int: ...
# def f(x) -> int: ...
