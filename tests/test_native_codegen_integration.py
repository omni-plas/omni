from omni.native_codegen_integration import build_spill_sequence


def test_spill_sequence_contains_store_and_reload_code():
    seq = build_spill_sequence("x", 0, -8)
    assert seq.store_code.startswith(b"\x48\x89")
    assert seq.reload_code.startswith(b"\x48\x8b")
