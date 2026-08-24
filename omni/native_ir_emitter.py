"""Lower supported FunctionIR into concrete native instructions."""
from __future__ import annotations
from dataclasses import dataclass
from .native_function_emitter import EmittedFunction, emit_function
from .native_binary_lowering import lower_binary

@dataclass(frozen=True)
class LoweredIRFunction:
    name: str
    instructions: tuple[object, ...]
    stack_size: int

def lower_function(fn, locations: dict[str, int], stack_size: int = 0) -> LoweredIRFunction:
    out=[]
    for block in fn.blocks:
        for op in block.operations:
            if op.opcode == 'const':
                if len(op.outputs)!=1: raise ValueError('const requires one output')
                out.append(('imm',(locations[op.outputs[0]],int(op.attributes.get('value',0)))))
            elif op.opcode in {'add','sub','mul'}:
                if len(op.outputs)!=1 or len(op.inputs)!=2: raise ValueError(f'invalid {op.opcode}')
                out.append(lower_binary(op.opcode,locations[op.inputs[0]],locations[op.inputs[1]],locations[op.outputs[0]]))
            elif op.opcode in {'move','mov'}:
                if len(op.inputs)!=1 or len(op.outputs)!=1: raise ValueError('invalid move')
                out.append(('move',(locations[op.outputs[0]],locations[op.inputs[0]])))
            elif op.opcode == 'call':
                target=op.attributes.get('function')
                if not target: raise ValueError('call requires function attribute')
                if op.inputs: raise ValueError('call arguments require ABI call lowering')
                out.append(('call',target))
                if op.outputs:
                    if len(op.outputs)!=1: raise ValueError('call supports one return value')
                    dst=locations[op.outputs[0]]
                    if dst != 0: out.append(('move',(dst,0)))
            elif op.opcode == 'return':
                if len(op.inputs)!=1: raise ValueError('return requires one input')
                src=locations[op.inputs[0]]
                if src != 0: out.append(('move',(0,src)))
            else: raise ValueError(f'unsupported IR opcode: {op.opcode}')
    return LoweredIRFunction(fn.name,tuple(out),stack_size)

def emit_lowered(lowered: LoweredIRFunction) -> EmittedFunction:
    return emit_function(lowered.name,lowered.stack_size,lowered.instructions)
