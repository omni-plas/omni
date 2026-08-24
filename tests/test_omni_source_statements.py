from omni.omni_expr import IntLiteral
from omni.omni_statements import Return
from omni.omni_source_statements import compile_function

def test_compile_structured_function():
    fn=compile_function('main',(Return(IntLiteral(0)),))
    assert fn.name=='main'
    assert fn.blocks[0].operations[-1].opcode=='return'
