from omni.native_syscalls import syscall6


def test_syscall_instruction_is_emitted():
    code=syscall6(60,(3,))
    assert code.endswith(b"\x0f\x05")
    assert len(code)>10
