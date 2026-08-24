"""Compile an executable Omni arithmetic expression to native bytes."""
from __future__ import annotations
from .omni_expr_ir import lower_expr
from .native_value_lowering import lower_value_ops

def compile_expression(expr):
    ops=list(lower_expr(expr,'result'))
    ops.append(__import__('omni.ir',fromlist=['Operation']).Operation('return',inputs=('result',)))
    names={n for op in ops for n in (*op.inputs,*op.outputs)}
    regs={name:3+i for i,name in enumerate(sorted(names)) if i<10}
    if len(regs)!=len(names): raise ValueError('expression requires too many virtual registers')
    return lower_value_ops(tuple(ops),regs)
