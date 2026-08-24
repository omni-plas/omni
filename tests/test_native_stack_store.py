from omni.native_stack_store import add_rsp8, store_rsp8, sub_rsp8

def test_rsp_stack_adjustment_and_store():
    assert sub_rsp8(16)==b'\x48\x83\xec\x10'
    assert add_rsp8(16)==b'\x48\x83\xc4\x10'
    assert store_rsp8(0,8).startswith(b'\x48\x89')
