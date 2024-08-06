# pipe21e

This is a fork of the wonderful [pipe21](https://github.com/tandav/pipe21) library, with the following goals:

1. Add eager evaluation using `>>`.
2. Add an optional type argument.
3. Maybe omit args and kwargs? Still deciding.
4. Maintain compatibility, unless it violates 1, 2, 3.

### Examples

You can use `>>` to eagerly evaluate `Map`:
```python3
from pipe21e import Map
[3, 5] >> Map(lambda x: x * 2)
## ...is the same as...
[3, 5] | Map(lambda x: x * 2) | Pipe(list)
```

Similarly with `GroupBy`:
```python3
from pipe21e import GroupBy
['ab', 'cd', 'e', 'f', 'gh', 'ij'] >> GroupBy(len)
## ...is the same as...
['ab', 'cd', 'e', 'f', 'gh', 'ij'] | GroupBy(len) | MapValues(list) | Pipe(list)
```

If your editor is not providing proper type-based autocompletions, you can specify the type of the argument, as shown below. The type is only used for static checks and recommendations; it is ignored at runtime.

```python3
from pipe21e import Filter
["bob", "sue"] >> Filter(lambda x: x.startswith("b"), str)
#                                   can specify type  ^^^ 
```

### Docs & Status

In progress. Will probably have some breaking changes for a few months while I decide what I want it to look like, and then will stabilize in mid 2025 ish.

But, generally, you can refer to the [pipe21 docs](https://tandav.github.io/pipe21/reference/).

### Installation

(Will be available before the end of September 2024)
