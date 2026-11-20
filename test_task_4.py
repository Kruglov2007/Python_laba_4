import pytest
from task_4_anagrams import are_anagrams

@pytest.mark.parametrize("a, b, expected", [
    ("Listen", "Silent", True),
    ("Triangle", "Integral", True),
    ("Yarik", "yarik", False),
    ("hello", "world", False),
    ("Кот", "Ток", True),
    ("a", "b", False),
    ("", "abc", False),
    ("abs", "", False),
    (None, "abc", False),
])
def test_are_anagrams(a, b, expected):
    assert are_anagrams(a, b) == expected