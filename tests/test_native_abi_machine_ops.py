from omni.native_machine_ops import call_rel32, ret


def test_call_and_return_encoding():
    assert call_rel32(0) == b"\xe8\x00\x00\x00\x00"
    assert ret() == b"\xc3"
