"""Target-neutral ABI contracts with a System V AMD64 implementation."""
from __future__ import annotations
from dataclasses import dataclass

class ABIError(ValueError):
    pass

@dataclass(frozen=True)
class ABIModel:
    name: str
    integer_argument_registers: tuple[int, ...]
    return_register: int
    stack_alignment: int
    callee_saved_registers: tuple[int, ...]

SYSV_AMD64 = ABIModel(
    name="sysv-amd64",
    integer_argument_registers=(7, 6, 2, 1, 8, 9),
    return_register=0,
    stack_alignment=16,
    callee_saved_registers=(3, 5, 12, 13, 14, 15),
)

def validate_arity(abi: ABIModel, count: int) -> None:
    if count < 0 or count > len(abi.integer_argument_registers):
        raise ABIError(f"unsupported integer argument count: {count}")
