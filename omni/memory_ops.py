"""Helpers for validating target-neutral memory operations."""

from __future__ import annotations

from .ir import Operation


MEMORY_OPS = frozenset({"alloc", "load", "store", "ptr_add", "free"})


def validate_memory_operation(operation: Operation) -> None:
    operation.validate()
    if operation.opcode not in MEMORY_OPS:
        raise ValueError(f"not a memory operation: {operation.opcode}")
    if operation.opcode == "alloc":
        if len(operation.inputs) != 1 or len(operation.outputs) != 1:
            raise ValueError("alloc requires size input and pointer output")
        size = operation.attributes.get("size")
        if size is not None and (not isinstance(size, int) or size < 0):
            raise ValueError("alloc size must be a non-negative integer")
    elif operation.opcode == "load":
        if len(operation.inputs) != 1 or len(operation.outputs) != 1:
            raise ValueError("load requires pointer input and value output")
        width = operation.attributes.get("width")
        if width is not None and (not isinstance(width, int) or width <= 0):
            raise ValueError("load width must be positive")
    elif operation.opcode == "store":
        if len(operation.inputs) != 2 or operation.outputs:
            raise ValueError("store requires pointer and value inputs")
        width = operation.attributes.get("width")
        if width is not None and (not isinstance(width, int) or width <= 0):
            raise ValueError("store width must be positive")
    elif operation.opcode == "ptr_add":
        if len(operation.inputs) != 2 or len(operation.outputs) != 1:
            raise ValueError("ptr_add requires pointer and offset inputs")
    elif operation.opcode == "free":
        if len(operation.inputs) != 1 or operation.outputs:
            raise ValueError("free requires one pointer input")
