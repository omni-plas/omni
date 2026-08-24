"""Lower executable Omni expressions to IR operations."""
from __future__ import annotations
from .omni_expr import IntLiteral, Variable, Binary
from .ir import Operation

def lower_expr(expr, output='v0'):
    if isinstance(expr,IntLiteral):
        return (Operation('const',outputs=(output,),attributes={'value':expr.value}),)
    if isinstance(expr,Variable):
        return (Operation('load',outputs=(output,),attributes={'name':expr.name}),)
    if isinstance(expr,Binary):
        left=output+'_l'; right=output+'_r'
        ops=list(lower_expr(expr.left,left)); ops.extend(lower_expr(expr.right,right))
        opcode={'+':'add','-':'sub','*':'mul','/':'div'}.get(expr.op)
        if opcode is None: raise ValueError(f'unknown binary operator: {expr.op}')
        ops.append(Operation(opcode,inputs=(left,right),outputs=(output,)))
        return tuple(ops)
    raise TypeError(f'unknown expression: {type(expr).__name__}')
