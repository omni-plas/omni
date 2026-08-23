from omni.native_memory_lowering import encode_memory, load_stack, store_stack


def test_stack_memory_ops():
    assert encode_memory(load_stack(3,-8))
    assert encode_memory(store_stack(3,-8))
