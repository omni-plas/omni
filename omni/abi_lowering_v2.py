"""Corrected ABI call lowering implementation."""
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
    if count < 0:
        raise ABIError("argument count must be non-negative")
    n = len(abi.integer_argument_registers)
    args = tuple(ABIArgument(i, abi.integer_argument_registers[i] if i < n else None, None if i < n else i-n) for i in range(count))
    return ABICallPlan(args, abi.return_register)
