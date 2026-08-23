import pytest

from omni.omni_source import Binary, Function, Literal, Name, OmniSyntaxError, Return, parse, tokenize, TokenKind


def test_tokenize_and_parse_function():
    program = parse('fn main(a, b) { let x = a + b * 2; return x; }')
    assert len(program.functions) == 1
    fn = program.functions[0]
    assert fn.name == 'main'
    assert fn.parameters == ('a', 'b')
    assert isinstance(fn.body[0].value, Binary)
    assert isinstance(fn.body[1], Return)


def test_literals_and_calls():
    program = parse('fn main() { let x = add(1, 2); return x; }')
    call = program.functions[0].body[0].value
    assert call.callee == 'add'
    assert call.arguments == (Literal(1), Literal(2))


def test_precedence_and_names():
    program = parse('fn main(a) { return a + 2 * 3; }')
    expression = program.functions[0].body[0].value
    assert isinstance(expression, Binary)
    assert expression.operator == TokenKind.PLUS
    assert isinstance(expression.left, Name)
    assert isinstance(expression.right, Binary)


def test_invalid_character_is_rejected():
    with pytest.raises(OmniSyntaxError):
        tokenize('fn main() { return @; }')
