"""Lower a supported FunctionIR subset into concrete native instructions."""
from __future__ import annotations
from dataclasses import dataclass
from .native_function_emitter import EmittedFunction, emit_function
from .native_binary_lowering import lower_binary
from .native_machine_ops import mov_imm64, mov_rr

@dataclass(frozen=True)
class LoweredIRFunction:
    name: str
    instructions: tuple[object, ...]
    stack_size: int

def lower_function(fn, locations: dict[str, int], stack_size: int = 0) -> LoweredIRFunction:
    out=[]
    for block in fn.blocks:
        for op in block.operations:
            if op.opcode == "const":
                if len(op.outputs)!=1: raise ValueError("const requires one output")
                dst=locations[op.outputs[0]]
                out.append(("imm", (dst, int(op.attributes.get("value", 0)))))
            elif op.opcode in {"add","sub","mul"}:
                if len(op.outputs)!=1 or len(op.inputs)!=2: raise ValueError(f"invalid {op.opcode}")
                out.append(lower_binary(op.opcode, locations[op.inputs[0]], locations[op.inputs[1]], locations[op.outputs[0]]))
            elif op.opcode == "move":
                if len(op.inputs)!=1 or len(op.outputs)!=1: raise ValueError("invalid move")
                out.append(("move", (locations[op.outputs[0]], locations[op.inputs[0]])))
            elif op.opcode == "return":
                if len(op.inputs)!=1: raise ValueError("return requires one input")
                out.append(("return", (locations[op.inputs[0]],)))
            else:
                raise ValueError(f"unsupported IR opcode: {op.opcode}")
    return LoweredIRFunction(fn.name, tuple(out), stack_size)

def emit_lowered(lowered: LoweredIRFunction) -> EmittedFunction:
    body=[]
    for ins in lowered.instructions:
        if isinstance(ins, tuple) and ins[0] == "imm": body.append(ins)
        elif isinstance(ins, tuple) and ins[0] == "move": body.append(ins)
        elif hasattr(ins, "opcode"): body.append(ins)
        elif isinstance(ins, tuple) and ins[0] == "return":
            # ABI return register is RAX (0).
            src=ins[1][0]
            if src != 0: body.append(("move", (0, src)))
    # Normalize move tuples into a supported machine instruction representation.
    normalized=[]
    for ins in body:
        if isinstance(ins, tuple) and ins[0] == "move":
            normalized.append(_Move(ins[1][0], ins[1][1]))
        else: normalized.append(ins)
    return emit_function(lowered.name, lowered.stack_size, tuple(normalized))

@dataclass(frozen=True)
class _Move:
    dst: int
    src: int
