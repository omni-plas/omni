from omni.ir import Operation
from omni.native_operation_lowering import lower_operation


def test_return_lowers_to_ret():
    assert lower_operation(Operation('return'),{})==b'\xc3'


def test_add_lowers_to_machine_instruction():
    code=lower_operation(Operation('add',('a','b')),{'a':0,'b':3})
    assert code


def test_unknown_operation_is_rejected():
    try: lower_operation(Operation('future_op'),{})
    except NotImplementedError: pass
    else: raise AssertionError('unsupported operation must be rejected')
