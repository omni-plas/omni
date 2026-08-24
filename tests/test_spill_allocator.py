from omni.spill_allocator import allocate_spill_slots

def test_spills_get_deterministic_slots():
    slots,size=allocate_spill_slots(('a','b','a'))
    assert slots=={'a':0,'b':8}
    assert size==16
