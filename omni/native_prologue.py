"""Plan native function entry/exit around the shared frame model."""
from __future__ import annotations
from dataclasses import dataclass
from .native_frame_encoding import prologue, epilogue

@dataclass(frozen=True)
class FrameCode:
    stack_size: int
    prologue: bytes
    epilogue: bytes

def build_frame_code(stack_size:int)->FrameCode:
    return FrameCode(stack_size, prologue(stack_size), epilogue(stack_size))
