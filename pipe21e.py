import functools
import itertools
import operator
import re
import sys
from typing import TypeVar

T = TypeVar('T')
U = TypeVar('U')

class B(Generic[T, U]):
    def __init__(self, f: Callable[[T], U], ta: Optional[Type[T]] = None):
        self.f = f

class Pipe(B[T, U]):
    def __ror__(self, x: T) -> U:
        return self.f(x)
