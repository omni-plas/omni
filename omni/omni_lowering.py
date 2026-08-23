"""Semantic lowering from textual Omni AST to target-neutral IR."""
from __future__ import annotations

from .ir import BasicBlock, FunctionIR, ModuleIR, Operation
from .omni_source import Binary, Call, Function, If, Let, Literal, Name, Program, Return
from .types import TypeKind, TypeRef

class OmniLoweringError(ValueError): pass
_INT=TypeRef(TypeKind.INTEGER); _STRING=TypeRef(TypeKind.STRING); _BOOL=TypeRef(TypeKind.BOOL); _VOID=TypeRef(TypeKind.VOID)
_COMPARISONS={"==":"eq","!=":"ne","<":"lt","<=":"le",">":"gt",">=":"ge"}


def _expr(node,env,operations,counter,signatures):
    if isinstance(node,Literal):
        value=node.value; typ=_BOOL if isinstance(value,bool) else _INT if isinstance(value,int) else _STRING if isinstance(value,str) else None
        if typ is None: raise OmniLoweringError(f"unsupported literal: {type(value).__name__}")
        name=f"%v{counter[0]}"; counter[0]+=1; operations.append(Operation("const",outputs=(name,),attributes={"value":value,"type":typ.signature()})); env[name]=typ; return name,typ
    if isinstance(node,Name):
        try:return node.value,env[node.value]
        except KeyError as exc:raise OmniLoweringError(f"undefined name: {node.value}") from exc
    if isinstance(node,Binary):
        left,lt=_expr(node.left,env,operations,counter,signatures); right,rt=_expr(node.right,env,operations,counter,signatures)
        if node.operator.value in _COMPARISONS:
            if lt.kind!=TypeKind.INTEGER or rt.kind!=TypeKind.INTEGER: raise OmniLoweringError("comparisons currently require integer operands")
            name=f"%v{counter[0]}"; counter[0]+=1; operations.append(Operation("compare",inputs=(left,right),outputs=(name,),attributes={"operator":_COMPARISONS[node.operator.value],"type":_BOOL.signature()})); env[name]=_BOOL; return name,_BOOL
        if lt.kind!=TypeKind.INTEGER or rt.kind!=TypeKind.INTEGER: raise OmniLoweringError("arithmetic currently requires integer operands")
        name=f"%v{counter[0]}"; counter[0]+=1; operations.append(Operation({"+":"add","-":"sub","*":"mul","/":"div"}[node.operator.value],inputs=(left,right),outputs=(name,),attributes={"type":_INT.signature()})); env[name]=_INT; return name,_INT
    if isinstance(node,Call):
        signature=signatures.get(node.callee)
        if signature is None: raise OmniLoweringError(f"undefined function: {node.callee}")
        expected,result_type=signature
        if len(node.arguments)!=expected: raise OmniLoweringError(f"function {node.callee} expects {expected} arguments, got {len(node.arguments)}")
        args=[]
        for argument in node.arguments: args.append(_expr(argument,env,operations,counter,signatures)[0])
        name=f"%v{counter[0]}"; counter[0]+=1; operations.append(Operation("call",inputs=tuple(args),outputs=(name,),attributes={"callee":node.callee,"type":result_type.signature()})); env[name]=result_type; return name,result_type
    raise OmniLoweringError(f"unsupported expression node: {type(node).__name__}")


def _function(function,signatures):
    env={name:_INT for name in function.parameters}; counter=[0]; blocks=[]; block_index=[0]

    def new_block(prefix):
        name=f"{prefix}_{block_index[0]}"; block_index[0]+=1
        blocks.append({"name":name,"operations":[],"successors":[]})
        return blocks[-1]

    current=new_block("entry")
    result_type=_VOID

    def emit_statement(stmt):
        nonlocal current,result_type
        if current is None: return
        if isinstance(stmt,Let):
            value,typ=_expr(stmt.value,env,current["operations"],counter,signatures)
            if stmt.name in env: raise OmniLoweringError(f"duplicate local: {stmt.name}")
            env[stmt.name]=typ; current["operations"].append(Operation("move",inputs=(value,),outputs=(stmt.name,),attributes={"type":typ.signature()})); return
        if isinstance(stmt,Return):
            value,result_type=_expr(stmt.value,env,current["operations"],counter,signatures); current["operations"].append(Operation("return",inputs=(value,))); current=None; return
        if isinstance(stmt,If):
            cond,typ=_expr(stmt.condition,env,current["operations"],counter,signatures)
            if typ.kind!=TypeKind.BOOL: raise OmniLoweringError("if condition must be boolean")
            then_block=new_block("then"); else_block=new_block("else"); merge_block=new_block("merge")
            current["operations"].append(Operation("branch",inputs=(cond,),attributes={"true":then_block["name"],"false":else_block["name"]}))
            current["successors"]=[then_block["name"],else_block["name"]]
            saved=current
            current=then_block
            for child in stmt.then_body: emit_statement(child)
            then_cont=current
            current=else_block
            for child in stmt.else_body: emit_statement(child)
            else_cont=current
            if then_cont is not None: then_cont["successors"]=[merge_block["name"]]
            if else_cont is not None: else_cont["successors"]=[merge_block["name"]]
            if then_cont is None and else_cont is None:
                current=None
            elif then_cont is None:
                current=else_cont
            elif else_cont is None:
                current=then_cont
            else:
                current=merge_block
            return
        raise OmniLoweringError(f"unsupported statement: {type(stmt).__name__}")

    for stmt in function.body: emit_statement(stmt)
    if current is not None:
        raise OmniLoweringError(f"function has no return: {function.name}")
    ir_blocks=tuple(BasicBlock(b["name"],tuple(b["operations"]),tuple(b["successors"])) for b in blocks if b["operations"] or b["successors"])
    return FunctionIR(function.name,{name:_INT for name in function.parameters},result_type,ir_blocks)


def lower_program(program:Program,*,module_name="omni_module"):
    if not program.functions:raise OmniLoweringError("program contains no functions")
    signatures={fn.name:(len(fn.parameters),_INT) for fn in program.functions}
    if len(signatures)!=len(program.functions):raise OmniLoweringError("duplicate function name")
    module=ModuleIR(module_name,{},tuple(_function(fn,signatures) for fn in program.functions)); module.validate(); return module


def lower_source(source:str,*,module_name="omni_module"):
    from .omni_source import parse
    return lower_program(parse(source),module_name=module_name)
