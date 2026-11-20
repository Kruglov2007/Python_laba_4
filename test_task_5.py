import pytest
from task_5_dicts import combine_dicts
@pytest.mark.parametrize("d1, d2, expected", [
    ({'a': 1, 'b': 2}, {'b': 9, 'c': 4}, {'a': 1, 'b': 9, 'c': 4}),
    ({'x': 1}, {'y': 2}, {'x': 1, 'y': 2}),
    ({}, {'a': 1}, {'a': 1}),
    ({'a': 1}, {}, {'a': 1}),
    ({}, {}, {}),
    (None, {'a': 1}, {'a': 1}),
])
def test_combine_dicts(d1, d2, expected):
    d1_original = d1.copy() if d1 is not None else None
    d2_original = d2.copy() if d2 is not None else None
    result = combine_dicts(d1, d2)
    assert result == expected
    if d1 is not None:
        assert d1 == d1_original
    if d2 is not None:
        assert d2 == d2_original