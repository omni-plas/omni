from omni.abi import SYSV_AMD64
from omni.abi_lowering_v2 import lower_integer_call


def test_lowering_maps_registers_then_stack():
    plan = lower_integer_call(SYSV_AMD64, 8)
    assert [a.register for a in plan.arguments[:6]] == [7, 6, 2, 1, 8, 9]
    assert plan.arguments[6].stack_index == 0
    assert plan.arguments[7].stack_index == 1
