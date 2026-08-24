from omni.omni_arithmetic_compiler import compile_expression
from omni.omni_expr import Binary, IntLiteral

def test_expression_compiles_to_native_returning_function():
    code=compile_expression(Binary('*',Binary('+',IntLiteral(2),IntLiteral(3)),IntLiteral(4)))
    assert code.endswith(b'\xc3')
    assert len(code)>1
