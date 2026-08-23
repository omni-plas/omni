from omni.native_memory_ops import load_rbp, store_rbp


def test_rbp_spill_reload_encoding():
    assert store_rbp(-8, 3)
    assert load_rbp(3, -8)
