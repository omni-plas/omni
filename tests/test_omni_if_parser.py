from omni.omni_source import If, parse


def test_if_else_parses():
    program = parse('fn main(x) { if (x > 0) { return 1; } else { return 0; } }')
    node = program.functions[0].body[0]
    assert isinstance(node, If)
    assert len(node.then_body) == 1
    assert len(node.else_body) == 1
