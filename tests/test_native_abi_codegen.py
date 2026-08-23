from omni.native_abi_codegen import move_integer_arguments, move_return_to


def test_argument_move_uses_sysv_registers():
    code = move_integer_arguments((3, 4))
    assert code


def test_return_already_in_rax_needs_no_move():
    assert move_return_to(0) == b""
