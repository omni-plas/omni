from omni.native_branch_lowering import jz_rel8,jnz_rel8,jmp_rel8

def test_short_branches():
    assert jz_rel8(4)==b'\x74\x04'
    assert jnz_rel8(-2)==b'\x75\xfe'
    assert jmp_rel8(0)==b'\xeb\x00'
