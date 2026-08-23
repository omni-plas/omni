from omni.native_symbol_relocations import SymbolCallRelocation, SymbolDataRelocation, apply_symbol_relocations


def test_symbol_call_relocation():
    code=bytearray(b'\xe8\x00\x00\x00\x00')
    apply_symbol_relocations(code,(SymbolCallRelocation(1,5,'foo'),),symbols={'foo':15})
    assert int.from_bytes(code[1:5],'little',signed=True)==10


def test_symbol_data_relocation():
    code=bytearray(b'\x00'*8)
    apply_symbol_relocations(code,data=(SymbolDataRelocation(0,'msg',8),),symbols={'msg':0x1234})
    assert int.from_bytes(code,'little')==0x1234
