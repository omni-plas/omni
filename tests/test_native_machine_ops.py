from omni.native_machine_ops import add_rr, imul_rr, mov_imm64, mov_rr, sub_rr


def test_basic_x86_64_encoders():
    assert mov_rr(3, 4)
    assert mov_imm64(3, 42)
    assert add_rr(3, 4)
    assert sub_rr(3, 4)
    assert imul_rr(3, 4)
