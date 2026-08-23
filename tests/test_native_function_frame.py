from omni.native_function_frame import build_function_frame


def test_frame_slots_are_rbp_relative():
    frame = build_function_frame({"x": 0, "y": 8}, 16)
    assert [(s.value, s.rbp_offset) for s in frame.slots] == [("x", -8), ("y", -16)]
