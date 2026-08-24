from omni.native_spill_frame import build_spill_frame

def test_spill_frame_has_slots_and_machine_code():
    frame=build_spill_frame(('x','y'))
    assert frame['slots']=={'x':0,'y':8}
    assert frame['size']==16
    assert frame['prologue']
    assert frame['epilogue']
