"""Minimal deterministic SSA renaming for operation outputs."""
from __future__ import annotations

def rename_ssa(operations):
    versions={}; renamed=[]
    for op in operations:
        inputs=[]
        for value in op.inputs:
            inputs.append(versions.get(value,value))
        outputs=[]
        for value in op.outputs:
            n=versions.get(value,0)+1
            versions[value]=n
            outputs.append(f'{value}.{n}')
        renamed.append(type(op)(opcode=op.opcode,inputs=tuple(inputs),outputs=tuple(outputs),attributes=op.attributes))
    return tuple(renamed)
