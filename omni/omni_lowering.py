"""Semantic lowering from textual Omni AST to target-neutral IR."""
from __future__ import annotations
from .ir import BasicBlock, FunctionIR, ModuleIR, Operation
from .omni_source import Binary, Call, Function, Let, Literal, Name, Program, Return
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
    env={name:_INT for name in function.parameters}; operations=[]; counter=[0]; result=_VOID
    for statement in function.body:
        if isinstance(statement,Let):
            value,typ=_expr(statement.value,env,operations,counter,signatures)
            if statement.name in env: raise OmniLoweringError(f"duplicate local: {statement.name}")
            env[statement.name]=typ; operations.append(Operation("move",inputs=(value,),outputs=(statement.name,),attributes={"type":typ.signature()}))
        elif isinstance(statement,Return): value,result=_expr(statement.value,env,operations,counter,signatures); operations.append(Operation("return",inputs=(value,)))
        else: raise OmniLoweringError(f"unsupported statement: {type(statement).__name__}")
    if result==_VOID: raise OmniLoweringError(f"function has no return: {function.name}")
    return FunctionIR(function.name,{name:_INT for name in function.parameters},result,(BasicBlock("entry",tuple(operations)),))

def lower_program(program:Program,*,module_name="omni_module"):
    if not program.functions:raise OmniLoweringError("program contains no functions")
    signatures={fn.name:(len(fn.parameters),_INT) for fn in program.functions}
    if len(signatures)!=len(program.functions):raise OmniLoweringError("duplicate function name")
    if any(any(type(stmt).__name__=="If" for stmt in fn.body) for fn in program.functions): raise OmniLoweringError("if statements require control-flow lowering")
    module=ModuleIR(module_name,{},tuple(_function(fn,signatures) for fn in program.functions)); module.validate(); return module

def lower_source(source:str,*,module_name="omni_module"): 
    from .omni_source import parse
    return lower_program(parse(source),module_name=module_name)
