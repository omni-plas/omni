from omni.omni_expr import Binary, IntLiteral
from omni.omni_expr_ir import lower_expr

def test_expression_lowers_to_operations():
    ops=lower_expr(Binary('+',IntLiteral(2),IntLiteral(3)))
    assert [op.opcode for op in ops]==['const','const','add']
