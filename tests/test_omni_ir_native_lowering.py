from omni.omni_ir import IRFunction, IRModule
from omni.omni_ir_native_lowering import lower_function, lower_module


def test_ir_function_lowers_to_validated_function_ir():
    fn=lower_function(IRFunction('main',('x','y')))
    fn.validate()
    assert fn.name=='main'
    assert tuple(fn.parameters)==('x','y')
    assert fn.blocks[0].operations[0].opcode=='return'


def test_ir_module_lowers_all_functions():
    module=IRModule((IRFunction('a',()),IRFunction('b',('x',))) )
    assert [f.name for f in lower_module(module)]==['a','b']
