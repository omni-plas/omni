from omni.native_call_frame import plan_call_frame


def test_call_frame_tracks_stack_bytes_and_padding():
    frame=plan_call_frame(1,0)
    assert frame.stack_argument_bytes==8
    assert frame.alignment_padding==8
    assert frame.cleanup_bytes==16
