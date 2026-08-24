"""Unified lowering for a small executable Omni IR subset."""
from __future__ import annotations
from .native_machine_ops import mov_imm64,mov_rr,add_rr,sub_rr,imul_rr
from .native_function_prologue import prologue,epilogue
from .register_allocator import allocate
from .spill_allocator import allocate_spill_slots

def emit_function(operations, registers=(0,1,2,3,4,5)):
    values=tuple(v for op in operations for v in (*op.inputs,*op.outputs))
    allocation=allocate(values,registers)
    _,frame_size=allocate_spill_slots(allocation.spills)
    if frame_size: raise ValueError('spilled functions require stack-frame lowering')
    code=bytearray(prologue())
    for op in operations:
        if op.opcode=='const': code+=mov_imm64(allocation.registers[op.outputs[0]],op.attributes['value'])
        elif op.opcode=='mov': code+=mov_rr(allocation.registers[op.outputs[0]],allocation.registers[op.inputs[0]])
        elif op.opcode=='add': code+=add_rr(allocation.registers[op.outputs[0]],allocation.registers[op.inputs[1]])
        elif op.opcode=='sub': code+=sub_rr(allocation.registers[op.outputs[0]],allocation.registers[op.inputs[1]])
        elif op.opcode=='mul': code+=imul_rr(allocation.registers[op.outputs[0]],allocation.registers[op.inputs[1]])
        elif op.opcode=='return':
            if op.inputs and allocation.registers[op.inputs[0]]!=0: code+=mov_rr(0,allocation.registers[op.inputs[0]])
            code+=epilogue()
        else: raise ValueError(f'unsupported opcode: {op.opcode}')
    if not operations or operations[-1].opcode!='return': code+=epilogue()
    return bytes(code)
