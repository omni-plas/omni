from omni.native_runtime import emit_exit, emit_write


def test_exit_runtime_emits_syscall():
    assert emit_exit(3).endswith(b"\x0f\x05")


def test_write_runtime_emits_syscall():
    assert emit_write(7,6,2).endswith(b"\x0f\x05")
