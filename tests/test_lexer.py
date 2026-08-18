import pytest

from omni.lexer import tokenize


def test_lexer_preserves_source_order_and_spans():
    tokens = tokenize("answer = 42")
    assert [(t.kind, t.text) for t in tokens] == [
        ("identifier", "answer"), ("punctuation", "="), ("number", "42")
    ]
    assert tokens[-1].start == 9


def test_lexer_rejects_unterminated_string():
    with pytest.raises(ValueError):
        tokenize('"unfinished')
