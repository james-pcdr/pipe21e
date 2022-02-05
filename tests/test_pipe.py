import hypothesis.strategies as st
import pytest
from hypothesis import given

from pipe21 import *


def is_even(x):
    return x % 2 == 0


@given(st.lists(st.integers() | st.characters() | st.floats() | st.booleans() | st.binary()))
def test_pipe(it):
    assert it | Pipe(list) == list(it)


@given(st.lists(st.integers() | st.characters() | st.floats() | st.booleans() | st.binary()))
def test_map(it):
    assert it | Map(str) | Pipe(list) == list(map(str, it))


@given(st.lists(st.integers()))
def test_filter(it):
    assert it | Filter(is_even) | Pipe(list) == list(filter(is_even, it))


@given(st.lists(st.integers()))
def test_filter_false(it):
    assert it | FilterFalse(is_even) | Pipe(list) == list(filter(lambda x: not is_even(x), it))


def test_value_by():
    assert range(2) | ValueBy(str) | Pipe(list) == [(0, '0'), (1, '1')]


def test_append():
    assert [(0,), (1,)] | Append(lambda x: str(x[0])) | Pipe(list) == [(0, '0'), (1, '1')]
    assert [(0, '0'), (1, '1')] | Append(lambda x: str(x[0] * 10)) | Pipe(list) == [(0, '0', '0'), (1, '1', '10')]


@pytest.mark.parametrize('seq, key, expected', (
    ([0, 1, 1, 2], None, [0, 1, 2]),
    ('0112', int, ['0', '1', '2']),
    (range(10), lambda x: x % 3, [0, 1, 2])
))
def test_unique(seq, key, expected):
    assert seq | Unique(key) | Pipe(list) == expected


@pytest.mark.parametrize('seq, key, expected', (
    ([0, 1, 2, 3], None, True),
    ([0, 1, 1, 3], None, False),
    ('0123', int, True),
    ('0113', int, False),
))
def test_is_unique(seq, key, expected):
    assert seq | IsUnique(key) == expected


@pytest.mark.parametrize('it, n, expected', (
    (range(5), 3, (0, 1, 2)),
    (range(5), 1, (0,)),
    (range(5), 0, ()),
    (range(5), 10, (0, 1, 2, 3, 4)),
))
def test_take(it, n, expected):
    assert it | Take(n) == expected


@pytest.mark.parametrize('it, expected', (
    (range(5), 5),
    ('abc', 3),
    ({1, 2, 3}, 3),
    ({'a': 1, 'b': 2}, 2),
))
def test_count(it, expected):
    assert it | Count() == expected


@pytest.mark.parametrize('it, n, expected', (
    (range(5), 5, [(0, 1, 2, 3, 4)]),
    (range(5), 4, [(0, 1, 2, 3), (4,)]),
    (range(5), 3, [(0, 1, 2), (3, 4)]),
    (range(5), 2, [(0, 1), (2, 3), (4,)]),
    (range(5), 1, [(0,), (1,), (2,), (3,), (4,)]),
    (range(5), 0, []),
))
def test_chunked(it, n, expected):
    assert it | Chunked(n) | Pipe(list) == expected


@pytest.mark.parametrize('it, kw', (
    ([3, 5, 1, 0], {}),
    ([3, 5, 1, 0], {'reverse': True}),
    ('3510', {'key': int}),
    ('3510', {'key': int, 'reverse': True}),
    ('9j8xy2m#98g%^xd$', {'key': ord, 'reverse': True}),
    ('9j8xy2m#98g%^xd$', {'key': ord, 'reverse': False}),
))
def test_sorted(it, kw):
    assert it | Sorted(**kw) == sorted(it, **kw)
