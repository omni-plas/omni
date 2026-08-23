from omni.native_machine_ops import cmp_rr, je_rel8, jne_rel8, jmp_rel8, load_rbp8, store_rbp8


def test_control_flow_encoders():
    assert cmp_rr(3,4)
    assert jmp_rel8(2) == b"\xeb\x02"
    assert je_rel8(2) == b"\x74\x02"
    assert jne_rel8(-2) == b"\x75\xfe"


def test_memory_encoders():
    assert load_rbp8(3,-8)
    assert store_rbp8(-8,3)
