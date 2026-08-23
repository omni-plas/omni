from omni.native_call_full import emit_full_call


def test_full_call_contains_call_and_cleanup():
    code=emit_full_call('callee',(3,4,5,6,7,8),(99,))
    assert b'\xe8\x00\x00\x00\x00' in code
    assert b'\x48\x83\xc4\x10' in code
