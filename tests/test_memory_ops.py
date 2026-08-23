import pytest

from omni.ir import Operation
from omni.memory_ops import validate_memory_operation


def test_alloc_operation_is_validated():
    validate_memory_operation(Operation("alloc", inputs=("size",), outputs=("ptr",), attributes={"size": 16}))


def test_store_requires_pointer_and_value():
    validate_memory_operation(Operation("store", inputs=("ptr", "value"), attributes={"width": 8}))


def test_invalid_load_width_is_rejected():
    with pytest.raises(ValueError, match="load width"):
        validate_memory_operation(Operation("load", inputs=("ptr",), outputs=("value",), attributes={"width": 0}))
