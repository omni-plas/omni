from omni.native_relocations import Relocation, apply_rel8


def test_rel8_relocation():
    code=bytearray(b"\xeb\x00\x90\x90\xc3")
    apply_rel8(code,(Relocation(1,4),))
    assert code[1] == 2
