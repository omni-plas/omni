"""Lower Omni calls to ABI-level register and return locations."""
from __future__ import annotations
from dataclasses import dataclass
from .abi import ABIError, ABIModel

@dataclass(frozen=True)
class ABIArgument:
    index: int
    register: int | None
    stack_index: int | None

@dataclass(frozen=True)
class ABICallPlan:
    arguments: tuple[ABIArgument, ...]
    return_register: int


def lower_integer_call(abi: ABIModel, count: int) -> ABICallPlan:
    if count < 0: raise ABIError("argument count must be non-negative")
    args = tuple(ABIArgument(i, abi.integer_argument_registers[i] if i < len(abi.integer_argument_registers) else None, None if i < len(abi.integer_argument_registers) else i-len(abi.integer_argument_registers)) for i in range(count))
    return ABICallPlan(args, abi.return_register)
