"""Validate and plan native call frames before instruction emission."""
from __future__ import annotations
from .native_calling_convention import assign_arguments
from .native_call_frame import CallFrame

def plan_call_frame(argument_count, local_bytes=0):
    _,stack_args=assign_arguments(argument_count)
    frame=CallFrame(stack_args*8, local_bytes)
    return frame
