"""Compose function frame code around lowered body bytes."""
from __future__ import annotations
from .native_prologue import build_frame_code

def build_function_body(body:bytes, stack_size:int=0)->bytes:
    frame=build_frame_code(stack_size)
    return frame.prologue + bytes(body) + frame.epilogue
