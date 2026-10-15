"""Semantic lowering from textual Omni AST to target-neutral IR."""
from __future__ import annotations
from .ir import BasicBlock, FunctionIR, ModuleIR, Operation
from .omni_source import Assign, Binary, Call, Function, If, Let, Literal, Name, Program, Return, Unary, While
from .types import TypeKind, TypeRef
class OmniLoweringError(ValueError): pass
_INT=TypeRef(TypeKind.INTEGER); _STRING=TypeRef(TypeKind.STRING); _BOOL=TypeRef(TypeKind.BOOL); _VOID=TypeRef(TypeKind.VOID)
_COMPARISONS={"==":"eq","!=":"ne","<":"lt","<=":"le",">":"gt",">=":"ge"}
def _expr(node,env,operations,counter,signatures):
    if isinstance(node,Literal):
        value=node.value; typ=_BOOL if isinstance(value,bool) else _INT if isinstance(value,int) and not isinstance(value,bool) else _STRING if isinstance(value,str) else None
        if typ is None: raise OmniLoweringError(f"unsupported literal: {type(value).__name__}")
        name=f"%v{counter[0]}"; counter[0]+=1; operations.append(Operation("const",outputs=(name,),attributes={"value":value,"type":typ.signature()})); env[name]=typ; return name,typ
    if isinstance(node,Name):
        try:return node.value,env[node.value]
        except KeyError as exc:raise OmniLoweringError(f"undefined name: {node.value}") from exc
    if isinstance(node,Unary):
        value,typ=_expr(node.operand,env,operations,counter,signatures)
        if node.operator.value=="!":
            if typ.kind!=TypeKind.BOOL: raise OmniLoweringError("logical not requires boolean operand")
            name=f"%v{counter[0]}"; counter[0]+=1; operations.append(Operation("not",inputs=(value,),outputs=(name,),attributes={"type":_BOOL.signature()})); env[name]=_BOOL; return name,_BOOL
    if isinstance(node,Binary):
        left,lt=_expr(node.left,env,operations,counter,signatures); right,rt=_expr(node.right,env,operations,counter,signatures); op=node.operator.value
        if op in _COMPARISONS:
            if lt.kind!=TypeKind.INTEGER or rt.kind!=TypeKind.INTEGER: raise OmniLoweringError("comparisons currently require integer operands")
            name=f"%v{counter[0]}"; counter[0]+=1; operations.append(Operation("compare",inputs=(left,right),outputs=(name,),attributes={"operator":_COMPARISONS[op],"type":_BOOL.signature()})); env[name]=_BOOL; return name,_BOOL
        if op in {"&&","||"}:
            if lt.kind!=TypeKind.BOOL or rt.kind!=TypeKind.BOOL: raise OmniLoweringError("logical operators require boolean operands")
            name=f"%v{counter[0]}"; counter[0]+=1; operations.append(Operation("and" if op=="&&" else "or",inputs=(left,right),outputs=(name,),attributes={"type":_BOOL.signature()})); env[name]=_BOOL; return name,_BOOL
        if lt.kind!=TypeKind.INTEGER or rt.kind!=TypeKind.INTEGER: raise OmniLoweringError("arithmetic currently requires integer operands")
        name=f"%v{counter[0]}"; counter[0]+=1; operations.append(Operation({"+":"add","-":"sub","*":"mul","/":"div"}[op],inputs=(left,right),outputs=(name,),attributes={"type":_INT.signature()})); env[name]=_INT; return name,_INT
    if isinstance(node,Call):
        signature=signatures.get(node.callee)
        if signature is None: raise OmniLoweringError(f"undefined function: {node.callee}")
        expected,result_type=signature
        if len(node.arguments)!=expected: raise OmniLoweringError(f"function {node.callee} expects {expected} arguments, got {len(node.arguments)}")
        args=[_expr(argument,env,operations,counter,signatures)[0] for argument in node.arguments]
        name=f"%v{counter[0]}"; counter[0]+=1; operations.append(Operation("call",inputs=tuple(args),outputs=(name,),attributes={"callee":node.callee,"type":result_type.signature()})); env[name]=result_type; return name,result_type
    raise OmniLoweringError(f"unsupported expression node: {type(node).__name__}")
def _function(function,signatures):
    env={name:_INT for name in function.parameters}; counter=[0]; blocks=[]; index=[0]; current=None; result_type=_VOID
    def new(prefix):
        b={"name":f"{prefix}_{index[0]}","operations":[],"successors":[]}; index[0]+=1; blocks.append(b); return b
    current=new("entry")
    def stmt(s):
        nonlocal current,result_type
        if current is None:return
        if isinstance(s,Let):
            value,typ=_expr(s.value,env,current["operations"],counter,signatures)
            if s.name in env: raise OmniLoweringError(f"duplicate local: {s.name}")
            env[s.name]=typ; current["operations"].append(Operation("move",inputs=(value,),outputs=(s.name,),attributes={"type":typ.signature()})); return
        if isinstance(s,Assign):
            if s.name not in env: raise OmniLoweringError(f"undefined assignment target: {s.name}")
            value,typ=_expr(s.value,env,current["operations"],counter,signatures)
            if typ!=env[s.name]: raise OmniLoweringError(f"assignment type mismatch: {s.name}")
            current["operations"].append(Operation("move",inputs=(value,),outputs=(s.name,),attributes={"type":typ.signature()})); return
        if isinstance(s,Return):
            value,result_type=_expr(s.value,env,current["operations"],counter,signatures); current["operations"].append(Operation("return",inputs=(value,))); current=None; return
        if isinstance(s,If):
            cond,typ=_expr(s.condition,env,current["operations"],counter,signatures)
            if typ.kind!=TypeKind.BOOL: raise OmniLoweringError("if condition must be boolean")
            then_b=new("then"); else_b=new("else"); merge=new("merge"); current["operations"].append(Operation("branch",inputs=(cond,),attributes={"true":then_b["name"],"false":else_b["name"]})); current["successors"]=[then_b["name"],else_b["name"]]
            current=then_b
            for child in s.then_body:stmt(child)
            then_cont=current; current=else_b
            for child in s.else_body:stmt(child)
            else_cont=current
            if then_cont is not None:then_cont["successors"]=[merge["name"]]
            if else_cont is not None:else_cont["successors"]=[merge["name"]]
            current=None if then_cont is None and else_cont is None else else_cont if then_cont is None else then_cont if else_cont is None else merge; return
        if isinstance(s,While):
            header=new("while_header"); body=new("while_body"); exit_b=new("while_exit"); current["successors"]=[header["name"]]; current["operations"].append(Operation("jump",attributes={"target":header["name"]})); current=header
            cond,typ=_expr(s.condition,env,current["operations"],counter,signatures)
            if typ.kind!=TypeKind.BOOL: raise OmniLoweringError("while condition must be boolean")
            current["operations"].append(Operation("branch",inputs=(cond,),attributes={"true":body["name"],"false":exit_b["name"]})); current["successors"]=[body["name"],exit_b["name"]]; current=body
            for child in s.body:stmt(child)
            if current is not None: current["successors"]=[header["name"]]; current["operations"].append(Operation("jump",attributes={"target":header["name"]}))
            current=exit_b; return
        raise OmniLoweringError(f"unsupported statement: {type(s).__name__}")
    for s in function.body:stmt(s)
    if current is not None:
        if result_type.kind == TypeKind.VOID:
            # Void functions may finish implicitly; materialize the return so
            # every lowered control-flow path has an explicit terminator.
            current["operations"].append(Operation("return"))
            current = None
        else:
            raise OmniLoweringError(f"function has no return: {function.name}")
    return FunctionIR(function.name,{name:_INT for name in function.parameters},result_type,tuple(BasicBlock(b["name"],tuple(b["operations"]),tuple(b["successors"])) for b in blocks if b["operations"] or b["successors"]))
def lower_program(program:Program,*,module_name="omni_module"):
    if not program.functions:raise OmniLoweringError("program contains no functions")
    signatures={fn.name:(len(fn.parameters),_INT) for fn in program.functions}
    if len(signatures)!=len(program.functions):raise OmniLoweringError("duplicate function name")
    module=ModuleIR(module_name,{},tuple(_function(fn,signatures) for fn in program.functions));module.validate();return module
def lower_source(source:str,*,module_name="omni_module"):
    from .omni_source import parse
    return lower_program(parse(source),module_name=module_name)
