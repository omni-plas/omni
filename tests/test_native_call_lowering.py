from omni.native_call_lowering import emit_call, lower_call, move_arguments

def test_register_argument_moves_and_call():
    plan=lower_call('foo',(3,4))
    code=move_arguments(plan)+emit_call(0)
    assert code.endswith(b'\xe8\x00\x00\x00\x00')

def test_extra_arguments_are_preserved_as_stack_arguments():
    plan=lower_call('foo',(10,11,12,13,14,15,3))
    assert plan.stack_arguments==(3,)
