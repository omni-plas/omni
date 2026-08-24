from omni.native_call_frame_lowering import lower_outgoing_frame, cleanup_outgoing_frame

def test_outgoing_frame_for_overflow_arguments():
    regs={f'a{i}':i for i in range(8)}
    code,frame=lower_outgoing_frame(tuple(regs),regs)
    assert frame.size==16
    assert code.startswith(b'\x48\x83\xec\x10')
    assert cleanup_outgoing_frame(frame)==b'\x48\x83\xc4\x10'
