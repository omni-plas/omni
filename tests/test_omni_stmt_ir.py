from omni.omni_expr import IntLiteral
from omni.omni_statements import Assign, Return, Call
from omni.omni_stmt_ir import lower_statements

def test_statement_lowering():
    fn=lower_statements('main',(Assign('x',IntLiteral(4)),Call('foo',(IntLiteral(1),)),Return(IntLiteral(2))))
    assert fn.name=='main'
    assert [op.opcode for op in fn.blocks[0].operations]==['const','const','call','const','return']
