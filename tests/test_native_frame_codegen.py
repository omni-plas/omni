from omni.native_spill_codegen import epilogue, prologue


def test_frame_prologue_and_epilogue():
    p = prologue(16)
    e = epilogue(16)
    assert p[:4] == b"\x55\x48\x89\xe5"
    assert e[-2:] == b"\x5d\xc3"
