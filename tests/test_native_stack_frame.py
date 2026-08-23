from omni.native_stack_frame import make_frame

def test_frame_alignment():
    frame=make_frame(local_size=3,outgoing_size=9,saved_size=2)
    assert frame.size==16
