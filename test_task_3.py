import pytest
from task_3_palindrome import is_palindrome
@pytest.mark.parametrize('value,expected', [
    ("Radar", True),
    ("Annas", False),
    (12321, True),
    (12345, False),
    ("a", True),
    ("Шалаш", True),
    ("", True),
    (None, True),
])
def test_is_palindrome(value, expected):
    assert is_palindrome(value) == expected