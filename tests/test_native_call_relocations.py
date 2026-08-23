from omni.native_call_relocations import CallRelocation, apply_call_rel32


def test_call_relocation():
    code=bytearray(b"\xe8\x00\x00\x00\x00")
    apply_call_rel32(code,(CallRelocation(1,10,5),))
    assert int.from_bytes(code[1:5],"little",signed=True)==5
