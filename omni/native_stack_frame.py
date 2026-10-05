"""Concrete x86-64 stack allocation and outgoing argument stores."""
from __future__ import annotations
from dataclasses import dataclass
from .native_call_frame import plan_call_frame

RSP = 4
RBP = 5

@dataclass(frozen=True)
class StackFrame:
    size: int
    local_size: int
    outgoing_size: int
    saved_size: int

    @property
    def cleanup_bytes(self) -> int:
        return self.size

def make_frame(local_size: int = 0, outgoing_size: int = 0, saved_size: int = 0) -> StackFrame:
    if min(local_size, outgoing_size, saved_size) < 0:
        raise ValueError("frame sizes must be non-negative")
    raw = local_size + outgoing_size + saved_size
    size = (raw + 15) & ~15
    return StackFrame(size, local_size, outgoing_size, saved_size)

def sub_rsp(amount: int) -> bytes:
    if amount < 0 or amount > 127: raise ValueError("unsupported stack allocation")
    return b"\x48\x83\xec" + bytes([amount])

def add_rsp(amount: int) -> bytes:
    if amount < 0 or amount > 127: raise ValueError("unsupported stack cleanup")
    return b"\x48\x83\xc4" + bytes([amount])

def store_reg_rsp8(src: int, offset: int) -> bytes:
    if not 0 <= src <= 15 or not 0 <= offset <= 127 or offset % 8:
        raise ValueError("invalid stack store")
    rex = 0x48 | ((src >> 3) << 2)
    return bytes([rex, 0x89, 0x44 | ((src & 7) << 3), 0x24, offset])

def lower_outgoing_stack_args(stack_registers, current_alignment=0):
    frame = plan_call_frame(len(stack_registers), current_alignment)
    out = bytearray(sub_rsp(frame.cleanup_bytes))
    for i, reg in enumerate(stack_registers):
        out += store_reg_rsp8(reg, frame.alignment_padding + i * 8)
    return bytes(out), frame
