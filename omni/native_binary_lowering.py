"""Lower binary arithmetic using resolved register/spill locations."""
from __future__ import annotations
from dataclasses import dataclass
from .native_machine_ops import add_rr, sub_rr, imul_rr
from .native_memory_ops import load_rbp, store_rbp

@dataclass(frozen=True)
class BinaryLowering:
    opcode: str
    left_register: int
    right_register: int
    destination_register: int

def lower_binary(opcode:str,left:int,right:int,destination:int)->BinaryLowering:
    if opcode not in {"add","sub","mul"}: raise ValueError("unsupported binary opcode")
    return BinaryLowering(opcode,left,right,destination)

def encode_binary(op:BinaryLowering)->bytes:
    if op.destination_register != op.left_register:
        code = _move(op.destination_register, op.left_register)
    else: code=b""
    if op.opcode=="add": return code+add_rr(op.destination_register,op.right_register)
    if op.opcode=="sub": return code+sub_rr(op.destination_register,op.right_register)
    return code+imul_rr(op.destination_register,op.right_register)

def _move(dst,src):
    from .native_machine_ops import mov_rr
    return mov_rr(dst,src)
