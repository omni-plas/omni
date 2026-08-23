"""Explicit runtime contract for memory ownership operations."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class AllocationRequest:
    size: int
    alignment: int = 8

@dataclass(frozen=True)
class AllocationResult:
    address: int
    size: int
    alignment: int

class MemoryRuntimeError(RuntimeError): pass

def validate_request(request: AllocationRequest) -> None:
    if request.size < 0: raise MemoryRuntimeError("allocation size must be non-negative")
    if request.alignment <= 0 or request.alignment & (request.alignment-1): raise MemoryRuntimeError("alignment must be a power of two")

def validate_result(result: AllocationResult, request: AllocationRequest) -> None:
    validate_request(request)
    if result.address < 0 or result.address % request.alignment: raise MemoryRuntimeError("allocator returned misaligned address")
    if result.size < request.size: raise MemoryRuntimeError("allocator returned insufficient storage")
