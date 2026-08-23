"""Bridge target-neutral memory IR to native memory encoders."""
from __future__ import annotations
from dataclasses import dataclass
from .ir import Operation
from .native_memory_codegen import add_rr, mov_mem64, mov_rr, store_mem64, NativeMemoryCodegenError

class MemoryPipelineError(ValueError):
    pass

@dataclass(frozen=True)
class EncodedMemoryOp:
    opcode: str
    machine_code: bytes


def encode_memory_operation(op: Operation, registers: dict[str, int]) -> EncodedMemoryOp:
    try:
        if op.opcode == "load":
            if len(op.inputs) != 1 or len(op.outputs) != 1:
                raise MemoryPipelineError("load requires one input and one output")
            pointer = registers[op.inputs[0]]
            dst = registers[op.outputs[0]]
            if op.attributes.get("size", 8) != 8:
                raise MemoryPipelineError("native bridge currently supports 64-bit loads only")
            return EncodedMemoryOp(op.opcode, mov_mem64(dst, pointer, 0))
        if op.opcode == "store":
            if len(op.inputs) != 2:
                raise MemoryPipelineError("store requires pointer and value")
            pointer = registers[op.inputs[0]]
            value = registers[op.inputs[1]]
            if op.attributes.get("size", 8) != 8:
                raise MemoryPipelineError("native bridge currently supports 64-bit stores only")
            return EncodedMemoryOp(op.opcode, store_mem64(pointer, value, 0))
        if op.opcode == "ptr_add":
            if len(op.inputs) != 2 or len(op.outputs) != 1:
                raise MemoryPipelineError("ptr_add requires pointer and offset")
            pointer = registers[op.inputs[0]]
            offset = registers[op.inputs[1]]
            dst = registers[op.outputs[0]]
            return EncodedMemoryOp(op.opcode, mov_rr(dst, pointer) + add_rr(dst, offset))
        raise MemoryPipelineError(f"unsupported memory operation: {op.opcode}")
    except KeyError as exc:
        raise MemoryPipelineError(f"unknown register value: {exc.args[0]}") from exc
    except NativeMemoryCodegenError as exc:
        raise MemoryPipelineError(str(exc)) from exc
