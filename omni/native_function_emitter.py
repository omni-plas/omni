"""Assemble prepared frame and arithmetic machine operations."""
from __future__ import annotations
from dataclasses import dataclass
from .native_prologue import build_frame_code
from .native_binary_lowering import BinaryLowering, encode_binary
from .native_machine_ops import mov_imm64

@dataclass(frozen=True)
class EmittedFunction:
    name: str
    code: bytes
    stack_size: int

def emit_function(name:str, stack_size:int, instructions=())->EmittedFunction:
    frame=build_frame_code(stack_size)
    body=bytearray()
    for instruction in instructions:
        if isinstance(instruction,BinaryLowering): body += encode_binary(instruction)
        elif isinstance(instruction,tuple) and len(instruction)==2 and instruction[0]=="imm": body += mov_imm64(*instruction[1])
        else: raise ValueError("unsupported native instruction")
    return EmittedFunction(name, frame.prologue+bytes(body)+frame.epilogue, stack_size)
