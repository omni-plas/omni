from omni.native_frame_emitter import allocate_stack, cleanup_stack

def test_stack_frame_emission():
    assert allocate_stack(16)==b'\x48\x81\xec\x10\x00\x00\x00'
    assert cleanup_stack(16)==b'\x48\x81\xc4\x10\x00\x00\x00'
    assert allocate_stack(0)==b''
