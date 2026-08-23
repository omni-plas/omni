"""Deterministic reference runtime for the portable semantic IR subset."""
from __future__ import annotations
from typing import Any
from .ir import FunctionIR, ModuleIR, Operation
from .memory_model import Memory, MemoryModelError
from .validation import SemanticValidationError, validate_function, validate_module
class RuntimeErrorBase(RuntimeError): pass

def _value(env,name):
    if name not in env: raise RuntimeErrorBase(f"undefined value: {name}")
    return env[name]

def _execute_operation(operation,env,functions=None,memory=None):
    opcode=operation.opcode; args=[_value(env,n) for n in operation.inputs]; attrs=operation.attributes
    if opcode=="const": env[operation.outputs[0]]=attrs["value"]; return None
    if opcode=="move": env[operation.outputs[0]]=args[0]; return None
    if opcode in {"add","sub","mul","div"}:
        if opcode=="div" and args[1]==0: raise RuntimeErrorBase("division by zero")
        env[operation.outputs[0]]={"add":args[0]+args[1],"sub":args[0]-args[1],"mul":args[0]*args[1],"div":args[0]/args[1]}[opcode]; return None
    if opcode=="compare":
        op=attrs.get("operator"); env[operation.outputs[0]]={"eq":args[0]==args[1],"ne":args[0]!=args[1],"lt":args[0]<args[1],"le":args[0]<=args[1],"gt":args[0]>args[1],"ge":args[0]>=args[1]}[op]; return None
    if opcode in {"and","or"}: env[operation.outputs[0]]=(bool(args[0]) and bool(args[1])) if opcode=="and" else (bool(args[0]) or bool(args[1])); return None
    if opcode=="not": env[operation.outputs[0]]=not bool(args[0]); return None
    if opcode in {"alloc","load","store","ptr_add","free"}:
        if memory is None: raise RuntimeErrorBase("memory operation requires runtime memory")
        try:
            if opcode=="alloc": env[operation.outputs[0]]=memory.allocate(int(args[0]),alignment=int(attrs.get("alignment",8))).address
            elif opcode=="load": env[operation.outputs[0]]=memory.load(int(args[0]),int(attrs.get("width",8)),signed=bool(attrs.get("signed",False)))
            elif opcode=="store": memory.store(int(args[0]),int(args[1]),int(attrs.get("width",8)))
            elif opcode=="ptr_add": env[operation.outputs[0]]=int(args[0])+int(args[1])
            elif opcode=="free": pass
            return None
        except (MemoryModelError,ValueError,TypeError) as exc: raise RuntimeErrorBase(str(exc)) from exc
    if opcode=="call":
        if functions is None: raise RuntimeErrorBase("call requires module execution context")
        callee=functions.get(attrs.get("callee"))
        if callee is None: raise RuntimeErrorBase(f"function not found: {attrs.get('callee')}")
        names=list(callee.parameters); result=execute(callee,dict(zip(names,args)),functions,memory)
        env[operation.outputs[0]]=result; return None
    if opcode=="branch": return attrs["true"] if bool(args[0]) else attrs["false"]
    if opcode=="jump": return attrs["target"]
    if opcode=="return": return args[0] if args else None
    raise RuntimeErrorBase(f"unsupported operation: {opcode}")

def execute(function:FunctionIR,arguments=None,functions=None,memory=None):
    try: validate_function(function)
    except SemanticValidationError as exc: raise RuntimeErrorBase(str(exc)) from exc
    env=dict(arguments or {}); memory=memory or Memory(); missing=[n for n in function.parameters if n not in env]
    if missing: raise RuntimeErrorBase(f"missing argument: {missing[0]}")
    blocks={b.name:b for b in function.blocks}; current=function.blocks[0].name
    for _ in range(100_000):
        block=blocks[current]
        for operation in block.operations:
            result=_execute_operation(operation,env,functions,memory)
            if operation.opcode=="return": return result
            if operation.opcode in {"branch","jump"}: current=result; break
        else:
            if not block.successors: raise RuntimeErrorBase(f"function ended without return: {function.name}")
            if len(block.successors)!=1: raise RuntimeErrorBase("non-branch block requires one successor")
            current=block.successors[0]
    raise RuntimeErrorBase("execution step limit exceeded")

def execute_module(module:ModuleIR,entry:str,arguments=None):
    try: validate_module(module)
    except SemanticValidationError as exc: raise RuntimeErrorBase(str(exc)) from exc
    functions={f.name:f for f in module.functions}; function=functions.get(entry)
    if function is None: raise RuntimeErrorBase(f"entry function not found: {entry}")
    return execute(function,arguments,functions)
