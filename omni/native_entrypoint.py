"""Generate a minimal Linux process entry sequence."""
from __future__ import annotations
from .native_machine_ops import mov_rr, mov_imm64
from .native_runtime import emit_exit

RAX=0
RDI=7

def emit_exit_with_status(status:int=0)->bytes:
    return mov_imm64(RDI,status)+emit_exit(RDI)

def emit_return_zero()->bytes:
    return mov_imm64(RAX,0)+b"\xc3"
