from omni.native_function_prologue import prologue, epilogue

def test_function_frame_bytes():
    assert prologue()==b'\x55\x48\x89\xe5'
    assert epilogue()==b'\x5d\xc3'
