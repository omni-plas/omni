from omni.native_prologue import build_frame_code


def test_frame_code_is_emitted():
    frame = build_frame_code(16)
    assert frame.prologue
    assert frame.epilogue
