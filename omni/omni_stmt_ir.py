"""Lower executable Omni statements into the existing FunctionIR model."""
from __future__ import annotations
from .omni_statements import Assign, Return, Call, If
from .omni_expr_ir import lower_expr
from .ir import Operation, BasicBlock, FunctionIR

def lower_statements(name, statements):
    ops=[]
    env={}
    for stmt in statements:
        if isinstance(stmt,Assign):
            value=f"v_{stmt.name}"
            ops.extend(lower_expr(stmt.value,value)); env[stmt.name]=value
        elif isinstance(stmt,Return):
            if stmt.value is None: ops.append(Operation('return'))
            else:
                value='return_value'; ops.extend(lower_expr(stmt.value,value)); ops.append(Operation('return',inputs=(value,)))
        elif isinstance(stmt,Call):
            args=[]
            for i,arg in enumerate(stmt.arguments):
                value=f'arg_{i}'; ops.extend(lower_expr(arg,value)); args.append(value)
            ops.append(Operation('call',inputs=tuple(args),attributes={'function':stmt.function}))
        elif isinstance(stmt,If):
            cond='condition'; ops.extend(lower_expr(stmt.condition,cond)); ops.append(Operation('branch',inputs=(cond,),attributes={'then':'then','else':'else'}))
        else: raise TypeError(f'unsupported statement: {type(stmt).__name__}')
    return FunctionIR(name,blocks=(BasicBlock('entry',tuple(ops)),))
