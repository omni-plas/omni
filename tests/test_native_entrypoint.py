from omni.native_entrypoint import emit_exit_with_status, emit_return_zero


def test_exit_entrypoint():
    code=emit_exit_with_status(0)
    assert code.endswith(b"\x0f\x05")


def test_return_zero():
    assert emit_return_zero().endswith(b"\xc3")
