from omni.native_abi import move_integer_args, move_return_value


def test_return_moves_into_rax():
    assert move_return_value(3)
    assert move_return_value(0) == b""


def test_integer_arguments_use_sysv_registers():
    assert move_integer_args((3,4))
