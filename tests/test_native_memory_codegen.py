from omni.native_memory_codegen import add_imm64, mov_imm64, mov_mem64, store_mem64


def test_mov_immediate_has_expected_opcode():
    code = mov_imm64(0, 123)
    assert code[:2] == b"\x48\xb8"
    assert len(code) == 10


def test_memory_load_and_store_encode():
    load = mov_mem64(0, 3, 8)
    store = store_mem64(3, 0, 8)
    assert load[-2:] == bytes([0x03, 8])
    assert store[-2:] == bytes([0x03, 8])


def test_add_immediate_encoding_exists():
    assert add_imm64(3, 16)
