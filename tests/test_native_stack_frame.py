from omni.native_stack_frame import make_frame, lower_outgoing_stack_args

def test_frame_alignment():
    frame=make_frame(local_size=3,outgoing_size=9,saved_size=2)
    assert frame.size==16

def test_outgoing_stack_argument_lowering():
    code,frame=lower_outgoing_stack_args((10,11),0)
    assert code.startswith(b'\x48\x83\xec')
    assert frame.stack_argument_bytes if hasattr(frame,'stack_argument_bytes') else frame.cleanup_bytes==16
