"""Build a concrete internal-call byte sequence including stack arguments."""
from __future__ import annotations
from dataclasses import dataclass
from .native_call_lowering import move_call_arguments, emit_direct_call, move_return_value
from .native_call_frame import plan_call_frame
from .native_stack_frame import lower_outgoing_stack_args, add_rsp
from .native_calling_convention import ARG_REGISTERS

@dataclass(frozen=True)
class CallSequence:
    moves: bytes
    stack_values: tuple[int, ...]
    target: str

def build_call_sequence(target: str, values: tuple[int, ...]) -> CallSequence:
    register_values = tuple(values[:len(ARG_REGISTERS)])
    register_map = {index: value for index, value in enumerate(register_values)}
    moves = bytearray()
    for index, source in enumerate(register_values):
        destination = ARG_REGISTERS[index]
        if source != destination:
            from .native_machine_ops import mov_rr
            moves += mov_rr(destination, source)
    return CallSequence(bytes(moves), tuple(values[len(ARG_REGISTERS):]), target)

def lower_internal_call(values, register_map, rel32, result_register=None, current_alignment=0):
    register_values = values[:len(ARG_REGISTERS)]
    stack_values = values[len(ARG_REGISTERS):]
    code = bytearray()
    frame = None
    if stack_values:
        stack_regs = tuple(register_map[v] for v in stack_values)
        stack_code, frame = lower_outgoing_stack_args(stack_regs, current_alignment)
        code += stack_code
    code += move_call_arguments(register_values, register_map)
    code += emit_direct_call(rel32)
    if frame is not None:
        code += add_rsp(frame.cleanup_bytes)
    if result_register is not None:
        code += move_return_value(result_register)
    return bytes(code), frame
