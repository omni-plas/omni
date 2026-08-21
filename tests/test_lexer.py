import pytest

from omni.lexer import Token, tokenize


def test_lexer_preserves_source_order_and_spans():
    tokens = tokenize("answer = 42")
    assert [(t.kind, t.text) for t in tokens] == [
        ("identifier", "answer"), ("punctuation", "="), ("number", "42")
    ]
    assert tokens[-1].start == 9
    assert tokens[-1].end == 11


def test_lexer_rejects_unterminated_string():
    with pytest.raises(ValueError):
        tokenize('"unfinished')


def test_lexer_rejects_non_text_input():
    with pytest.raises(TypeError, match="text"):
        tokenize(None)


def test_token_rejects_invalid_span():
    with pytest.raises(ValueError, match="span"):
        Token("identifier", "x", 2, 1)
    with pytest.raises(ValueError, match="empty"):
        Token("identifier", "", 1, 1)


def test_lexer_handles_escaped_quotes():
    tokens = tokenize(r'"a\\"b"')
    assert len(tokens) == 1
    assert tokens[0].kind == "string"


def test_lexer_supports_unicode_identifiers():
    tokens = tokenize("سلام = 7")
    assert tokens[0].text == "سلام"
    assert tokens[0].kind == "identifier"
