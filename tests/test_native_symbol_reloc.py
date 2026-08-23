from omni.native_symbol_reloc import abs32, abs64, call_rel32


def test_symbol_relocation_constructors():
    assert call_rel32(1,'foo',5).kind=='call_rel32'
    assert abs32(2,'data').kind=='abs32'
    assert abs64(3,'data').kind=='abs64'
