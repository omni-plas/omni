"""Assemble prepared frame, arithmetic operations and symbolic calls."""
from __future__ import annotations
from dataclasses import dataclass
from .native_prologue import build_frame_code
from .native_binary_lowering import BinaryLowering, encode_binary
from .native_machine_ops import mov_imm64, mov_rr, call_rel32
from .native_call_linker import NativeCallSite
from .elf64 import build_elf64

@dataclass(frozen=True)
class EmittedFunction:
    name: str
    code: bytes
    stack_size: int
    call_sites: tuple[NativeCallSite,...] = ()

def emit_function(name: str, stack_size: int, instructions=()) -> EmittedFunction:
    frame = build_frame_code(stack_size)
    body = bytearray()
    call_sites=[]
    for instruction in instructions:
        if isinstance(instruction, BinaryLowering):
            body += encode_binary(instruction)
        elif isinstance(instruction, tuple) and len(instruction) == 2 and instruction[0] == "imm":
            body += mov_imm64(*instruction[1])
        elif isinstance(instruction, tuple) and len(instruction) == 2 and instruction[0] == "move":
            body += mov_rr(*instruction[1])
        elif isinstance(instruction, tuple) and len(instruction) == 2 and instruction[0] == "call":
            target=instruction[1]
            immediate_offset=len(frame.prologue)+len(body)+1
            body += call_rel32(0)
            call_sites.append(NativeCallSite(immediate_offset, immediate_offset+4, target))
        elif hasattr(instruction, "dst") and hasattr(instruction, "src"):
            body += mov_rr(instruction.dst, instruction.src)
        else:
            raise ValueError(f"unsupported native instruction: {instruction!r}")
    return EmittedFunction(name, frame.prologue + bytes(body) + frame.epilogue, stack_size, tuple(call_sites))

def emit_elf64(name: str, stack_size: int, instructions=(), entry_offset: int = 0) -> bytes:
    emitted = emit_function(name, stack_size, instructions)
    return build_elf64(emitted.code, entry_offset)
