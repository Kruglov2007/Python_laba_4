import pytest
from task_1_words import count_words

@pytest.mark.parametrize("sentence, expected",[
("Hello world", 2),
("   Hello    world   ", 2),
("", 0),
("          ", 0),
("Yarik", 1),
("One two three four five", 5),
(None, 0),
])
def test_count_words(sentence, expected):
    assert count_words(sentence) == expected