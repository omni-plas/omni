from omni.native_spill_codegen_v3 import emit_spill_sequence, emit_reload_sequence

def test_spill_reload_sequences():
    spill,slots,size=emit_spill_sequence(('x',),{'x':0})
    assert spill and slots['x']==0 and size==8
    reload=emit_reload_sequence(('x',),{'x':1},slots)
    assert reload
