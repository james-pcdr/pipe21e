from functools import reduce
import operator
import subprocess
import itertools
import re
import concurrent.futures

__all__ = [
    'Pipe', 'Map', 'Filter',
    'Reduce', 'MapValues', 'MapKeys',
    'FilterKeys', 'FilterValues', 'FlatMap',
    'KeyBy', 'ValueBy', 'Keys', 'Values',
    'Grep', 'GrepV', 'FilterEqual', 'FilterNotEqual',
    'GroupBy', 'ReadLines', 'ShellArg', 'ShellExec', 'PipeArgs',
    'MapArgs', 'ForEach', 'ThreadMap', 'ProcessMap', 'count',
]

# basic
class B:
    def __init__(self, f=None): self.f = f
class Pipe  (B): __ror__ = lambda self, x: self.f(x)        
class Map   (B): __ror__ = lambda self, x: map   (self.f, x)
class Filter(B): __ror__ = lambda self, x: filter(self.f, x)

# extended
class Reduce        (B): __ror__ = lambda self, x: reduce(self.f, x)
class MapValues     (B): __ror__ = lambda self, it: it | Map(lambda kv: (kv[0], self.f(kv[1])))
class MapKeys       (B): __ror__ = lambda self, it: it | Map(lambda kv: (self.f(kv[0]), kv[1]))
class FilterKeys    (B): __ror__ = lambda self, it: it | Filter(operator.itemgetter(0))
class FilterValues  (B): __ror__ = lambda self, it: it | Filter(operator.itemgetter(1))
class FlatMap       (B): __ror__ = lambda self, it: it | Map(self.f) | Pipe(itertools.chain.from_iterable)
# class FlatMapValues (B): __ror__ = lambda self, it: it | Map(self.f) | Pipe(itertools.chain.from_iterable)
class KeyBy         (B): __ror__ = lambda self, it: it | Map(lambda x: (self.f(x), x))
class ValueBy       (B): __ror__ = lambda self, it: it | Map(lambda x: (x, self.f(x)))
class Keys          (B): __ror__ = lambda self, it: it | Map(operator.itemgetter(0))
class Values        (B): __ror__ = lambda self, it: it | Map(operator.itemgetter(1))
class Grep          (B): __ror__ = lambda self, it: it | Filter(lambda x:     re.search(self.f, x))
class GrepV         (B): __ror__ = lambda self, it: it | Filter(lambda x: not re.search(self.f, x))
class FilterEqual   (B): __ror__ = lambda self, it: it | Filter(lambda x: x == self.f)
class FilterNotEqual(B): __ror__ = lambda self, it: it | Filter(lambda x: x != self.f)
class GroupBy       (B): __ror__ = lambda self, it: itertools.groupby(it, key=self.f)
class ReadLines     (B): __ror__ = lambda self, fn: open(fn).readlines()
class ShellArg      (B): __ror__ = lambda self, x: subprocess.check_output((self.f, x), text=True).splitlines()
class ShellExec     (B): __ror__ = lambda self, x: subprocess.check_output(         x , text=True).splitlines()
class PipeArgs      (B): __ror__ = lambda self, x: self.f(*x)
class MapArgs       (B): __ror__ = lambda self, x: x | Map(lambda y: y | PipeArgs(self.f))
class ForEach(B):
    def __ror__(self, x):
        for e in x: self.f(e)

# flat_map_fn = lambda kv: ((kv[0], x) for x in f(kv[1]))
#         return self.flatMap(flat_map_fn, preservesPartitioning=True)

class ThreadMap(B):
    def __ror__(self, it):
        with concurrent.futures.ThreadPoolExecutor() as pool:
            return pool.map(self.f, it) | Pipe(list)

class ProcessMap(B):
    def __ror__(self, it):
        with concurrent.futures.ProcessPoolExecutor() as pool:
            return pool.map(self.f, it) | Pipe(list)



# class Sorted        (B): __ror__ = lambda self, x: sorted(x, **self.kw)

# shell = lambda x : subprocess.check_output(x, text=True).splitlines()
# argto
count = lambda it: sum(1 for _ in it)
    
# class B:
#     def __init__(self, f=None, **kw):
#         self.f = f
#         self.kw = kw # optional


