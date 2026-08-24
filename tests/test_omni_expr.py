from omni.omni_expr import Binary, IntLiteral, Variable, evaluate

def test_arithmetic_expression():
    expr=Binary('*',Binary('+',IntLiteral(2),IntLiteral(3)),IntLiteral(4))
    assert evaluate(expr)==20

def test_variable_expression():
    assert evaluate(Binary('+',Variable('x'),IntLiteral(2)),{'x':5})==7
