import pytest

from omni.native_spill_codegen import NativeSpillCodegenError, load_rbp, store_rbp


def test_rbp_spill_load_store_encode():
    load = load_rbp(0, -8)
    store = store_rbp(-16, 1)
    assert load.startswith(b"\x48\x8b")
    assert store.startswith(b"\x48\x89")


def test_spill_encoder_rejects_unaligned_offsets():
    with pytest.raises(NativeSpillCodegenError):
        load_rbp(0, -7)
