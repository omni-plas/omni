from omni.native_spill_emitter import emit_spill, emit_reload

def test_spill_and_reload_emit_machine_bytes():
    spill=emit_spill(0, -8)
    reload=emit_reload(1, -8)
    assert spill and reload

def test_large_displacement_is_rejected():
    try:
        emit_spill(0, -129)
    except ValueError:
        pass
    else:
        raise AssertionError('expected displacement validation')
