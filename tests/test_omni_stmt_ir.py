from omni.omni_expr import IntLiteral
from omni.omni_statements import Assign, Return, Call
from omni.omni_stmt_ir import lower_statements

def test_statement_lowering():
    fn=lower_statements('main',(Assign('x',IntLiteral(4)),Call('foo',(IntLiteral(1),)),Return(IntLiteral(2))))
    assert fn.name=='main'
    assert [op.opcode for op in fn.blocks[0].operations]==['const','const','call','const','return']

def test_call_can_capture_return_value():
    fn=lower_statements('main',(Call('foo',(IntLiteral(1),),'x'),Return(IntLiteral(0))))
    call=fn.blocks[0].operations[1]
    assert call.opcode=='call'
    assert call.outputs==('v_x',)
