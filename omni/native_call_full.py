"""Compose outgoing arguments, call, and stack cleanup."""
from __future__ import annotations
from .native_call_sequence import build_call_sequence
from .native_stack_args_real import push_arguments
from .native_call_frame import plan_call_frame
from .native_call_emitter import emit_call
from .native_call_cleanup import add_rsp

def emit_full_call(target:str, register_args:tuple[int,...]=(), stack_values:tuple[int,...]=()):
    sequence=build_call_sequence(target,register_args+tuple(stack_values))
    stack=push_arguments(stack_values)
    frame=plan_call_frame(len(stack_values))
    call,_=emit_call(target)
    cleanup=add_rsp(frame.cleanup_bytes)
    return sequence.moves+stack+call+cleanup
