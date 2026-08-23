from omni.native_call_lowering import lower_call, move_arguments


def test_six_integer_arguments_use_registers():
    plan=lower_call("foo",(10,11,12,13,14,15))
    assert not plan.stack_arguments
    assert move_arguments(plan)


def test_extra_arguments_are_preserved_as_stack_arguments():
    plan=lower_call("foo",(10,11,12,13,14,15,3))
    assert plan.stack_arguments==(3,)
