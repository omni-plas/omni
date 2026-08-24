from omni.native_call_relocation import call_rel32_displacement

def test_rel32_displacement_uses_next_instruction():
    assert call_rel32_displacement(100,20)==75
