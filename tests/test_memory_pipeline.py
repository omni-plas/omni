import pytest

from omni.ir import Operation
from omni.memory_pipeline import MemoryPipelineError, encode_memory_operation


def test_load_and_store_encode_to_machine_code():
    load = encode_memory_operation(Operation("load", inputs=("p",), outputs=("v",), attributes={"size": 8}), {"p": 3, "v": 0})
    store = encode_memory_operation(Operation("store", inputs=("p", "v"), attributes={"size": 8}), {"p": 3, "v": 0})
    assert load.opcode == "load" and load.machine_code
    assert store.opcode == "store" and store.machine_code


def test_pointer_add_uses_runtime_offset_register():
    result = encode_memory_operation(Operation("ptr_add", inputs=("p", "n"), outputs=("q",)), {"p": 3, "n": 1, "q": 2})
    assert result.machine_code


def test_rejects_unsupported_native_width():
    with pytest.raises(MemoryPipelineError):
        encode_memory_operation(Operation("load", inputs=("p",), outputs=("v",), attributes={"size": 4}), {"p": 3, "v": 0})
