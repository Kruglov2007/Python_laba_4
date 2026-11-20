import pytest
from task_2_unique import find_unique

@pytest.mark.parametrize("items, expected",[
    ([1, 2, 3, 2, 1, 4], [3, 4]),
    (['a', 'b', 'a', 'c', 'b', 'd'], ['c', 'd']),
    ([], []),
    ([1, 1, 2, 2], []),
    ([5, 6, 7], [5, 6, 7]),
    ([5, 'a', 5, 'b'], ['a', 'b']),
    (None, []),
])
def test_find_unique(items, expected):
    assert find_unique(items) == expected