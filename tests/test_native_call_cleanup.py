from omni.native_call_cleanup import add_rsp


def test_small_cleanup_uses_short_encoding():
    assert add_rsp(16)==b'\x48\x83\xc4\x10'


def test_large_cleanup_uses_long_encoding():
    assert add_rsp(256).startswith(b'\x48\x81\xc4')
