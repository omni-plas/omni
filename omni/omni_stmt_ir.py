"""Lower executable Omni statements into the existing FunctionIR model."""
from __future__ import annotations
from .omni_statements import Assign, Return, Call, If
from .omni_expr_ir import lower_expr
from .ir import Operation, BasicBlock, FunctionIR
from .types import TypeKind, TypeRef

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
            outputs=() if stmt.result is None else (f'v_{stmt.result}',)
            ops.append(Operation('call',inputs=tuple(args),outputs=outputs,attributes={'callee':stmt.function}))
            if stmt.result is not None: env[stmt.result]=outputs[0]
        elif isinstance(stmt,If):
            cond='condition'; ops.extend(lower_expr(stmt.condition,cond)); ops.append(Operation('branch',inputs=(cond,),attributes={'then':'then','else':'else'}))
        else: raise TypeError(f'unsupported statement: {type(stmt).__name__}')
    has_value_return = any(isinstance(stmt, Return) and stmt.value is not None for stmt in statements)
    result_type = TypeRef(TypeKind.INTEGER) if has_value_return else TypeRef(TypeKind.VOID)
    return FunctionIR(name, parameters={}, result=result_type, blocks=(BasicBlock('entry',tuple(ops)),))
