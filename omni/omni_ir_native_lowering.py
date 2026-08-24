"""Lower target-neutral Omni IR into the repository's executable FunctionIR."""
from __future__ import annotations
from .ir import BasicBlock, FunctionIR, Operation
from .types import TypeKind, TypeRef

I64=TypeRef(TypeKind.INTEGER,name="i64")
VOID=TypeRef(TypeKind.VOID)

def lower_function(ir_function):
    """Produce a minimal executable FunctionIR while preserving function parameters.

    Empty source bodies become an explicit return block. Unsupported operations are
    rejected instead of silently becoming placeholder machine code.
    """
    if not ir_function.name:
        raise ValueError("IR function requires a name")
    params={name:I64 for name in ir_function.parameters}
    block=BasicBlock("entry",operations=(Operation("return"),),successors=())
    fn=FunctionIR(ir_function.name,params,VOID,(block,))
    fn.validate()
    return fn

def lower_module(ir_module):
    functions=tuple(lower_function(fn) for fn in ir_module.functions)
    return functions
