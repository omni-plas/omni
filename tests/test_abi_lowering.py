from omni.abi import SYSV_AMD64
from omni.abi_lowering import lower_integer_call


def test_integer_call_uses_sysv_register_order():
    plan = lower_integer_call(SYSV_AMD64, 8)
    assert tuple(a.register for a in plan.arguments[:6]) == (7, 6, 2, 1, 8, 9)
    assert plan.arguments[6].stack_index == 0
    assert plan.return_register == 0
