"""Lower supported Omni IR operations directly to x86-64 machine bytes."""
from __future__ import annotations
from .native_machine_ops import add_rr, sub_rr, imul_rr, cmp_rr, ret

OP_ENCODERS={"add":add_rr,"sub":sub_rr,"mul":imul_rr,"cmp":cmp_rr}

def lower_operation(operation, registers):
    opcode=operation.opcode
    if opcode=="return":
        return ret()
    encoder=OP_ENCODERS.get(opcode)
    if encoder is None:
        raise NotImplementedError(f"unsupported native operation: {opcode}")
    if len(operation.inputs)!=2:
        raise ValueError(f"{opcode} requires two inputs")
    try:
        left=registers[operation.inputs[0]]
        right=registers[operation.inputs[1]]
    except KeyError as exc:
        raise ValueError(f"missing register assignment: {exc.args[0]}") from exc
    return encoder(left,right)

def lower_operations(operations, registers):
    return b"".join(lower_operation(op,registers) for op in operations)
