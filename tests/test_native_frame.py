from omni.native_frame import plan_frame


def test_frame_is_abi_aligned():
    frame = plan_frame(24, (3, 12))
    assert frame.stack_size % 16 == 0
    assert frame.saved_registers == (3, 12)
