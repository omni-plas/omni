from omni.native_function_frame import emit_frame

def test_function_frame_emits_stack_adjustments():
    frame,pro,epi=emit_frame({'x':0,'y':8},16)
    assert frame.stack_size==16
    assert frame.slots[0].rbp_offset==-8
    assert pro==b'\x48\x81\xec\x10\x00\x00\x00'
    assert epi==b'\x48\x81\xc4\x10\x00\x00\x00'
