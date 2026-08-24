"""Lower a small arithmetic IR subset to x86-64 instructions."""
from __future__ import annotations
from .native_machine_ops import mov_imm64, mov_rr, add_rr, sub_rr, imul_rr, ret

def lower_value_ops(ops, register_map):
    out=bytearray()
    for op in ops:
        if op.opcode=='const': out += mov_imm64(register_map[op.outputs[0]],op.attributes['value'])
        elif op.opcode=='mov': out += mov_rr(register_map[op.outputs[0]],register_map[op.inputs[0]])
        elif op.opcode=='add': out += add_rr(register_map[op.outputs[0]],register_map[op.inputs[1]])
        elif op.opcode=='sub': out += sub_rr(register_map[op.outputs[0]],register_map[op.inputs[1]])
        elif op.opcode=='mul': out += imul_rr(register_map[op.outputs[0]],register_map[op.inputs[1]])
        elif op.opcode=='return':
            if op.inputs: out += mov_rr(0,register_map[op.inputs[0]])
            out += ret()
        else: raise ValueError(f'unsupported native value operation: {op.opcode}')
    return bytes(out)
