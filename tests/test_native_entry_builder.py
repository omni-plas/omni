from omni.native_entry_builder import build_function_body


def test_function_body_has_frame_and_return():
    code=build_function_body(b'\x90',16)
    assert code.startswith(b'\x48\x89\xe5')
    assert code.endswith(b'\x5d\xc3') or code.endswith(b'\xc3')
