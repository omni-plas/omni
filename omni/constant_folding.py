"""Fold constant arithmetic operations in Omni IR."""
from __future__ import annotations
from .ir import Operation

def fold_constants(operations):
    values={}; out=[]
    for op in operations:
        if op.opcode=='const': values[op.outputs[0]]=op.attributes['value']; out.append(op); continue
        if op.opcode in {'add','sub','mul'} and all(v in values for v in op.inputs):
            a,b=(values[v] for v in op.inputs)
            result={'add':a+b,'sub':a-b,'mul':a*b}[op.opcode]
            folded=Operation('const',outputs=op.outputs,attributes={'value':result})
            values[op.outputs[0]]=result; out.append(folded)
        else:
            out.append(op)
    return tuple(out)
