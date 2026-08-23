"""Semantic lowering from textual Omni AST to the target-neutral IR."""

from __future__ import annotations

from .ir import BasicBlock, FunctionIR, ModuleIR, Operation
from .omni_source import Binary, Call, Function, Let, Literal, Name, Program, Return
from .types import TypeKind, TypeRef


class OmniLoweringError(ValueError):
    pass


_INT = TypeRef(TypeKind.INTEGER)
_STRING = TypeRef(TypeKind.STRING)
_BOOL = TypeRef(TypeKind.BOOL)
_VOID = TypeRef(TypeKind.VOID)


def _expr(node: object, env: dict[str, TypeRef], operations: list[Operation], counter: list[int]) -> tuple[str, TypeRef]:
    if isinstance(node, Literal):
        value = node.value
        if isinstance(value, bool): typ = _BOOL
        elif isinstance(value, int): typ = _INT
        elif isinstance(value, str): typ = _STRING
        else: raise OmniLoweringError(f"unsupported literal: {type(value).__name__}")
        name = f"%v{counter[0]}"; counter[0] += 1
        operations.append(Operation("const", outputs=(name,), attributes={"value": value, "type": typ.signature()}))
        env[name] = typ
        return name, typ
    if isinstance(node, Name):
        try: return node.value, env[node.value]
        except KeyError as exc: raise OmniLoweringError(f"undefined name: {node.value}") from exc
    if isinstance(node, Binary):
        left, lt = _expr(node.left, env, operations, counter)
        right, rt = _expr(node.right, env, operations, counter)
        if lt.kind != TypeKind.INTEGER or rt.kind != TypeKind.INTEGER:
            raise OmniLoweringError("arithmetic currently requires integer operands")
        opcode = {"+": "add", "-": "sub", "*": "mul", "/": "div"}[node.operator.value]
        name = f"%v{counter[0]}"; counter[0] += 1
        operations.append(Operation(opcode, inputs=(left, right), outputs=(name,), attributes={"type": _INT.signature()}))
        env[name] = _INT
        return name, _INT
    if isinstance(node, Call):
        args = []
        for argument in node.arguments:
            value, typ = _expr(argument, env, operations, counter)
            args.append(value)
        name = f"%v{counter[0]}"; counter[0] += 1
        operations.append(Operation("call", inputs=tuple(args), outputs=(name,), attributes={"callee": node.callee}))
        env[name] = TypeRef(TypeKind.ANY)
        return name, env[name]
    raise OmniLoweringError(f"unsupported expression node: {type(node).__name__}")


def _function(function: Function) -> FunctionIR:
    env: dict[str, TypeRef] = {name: _INT for name in function.parameters}
    operations: list[Operation] = []
    counter = [0]
    result = _VOID
    for statement in function.body:
        if isinstance(statement, Let):
            value, typ = _expr(statement.value, env, operations, counter)
            if statement.name in env: raise OmniLoweringError(f"duplicate local: {statement.name}")
            env[statement.name] = typ
            operations.append(Operation("move", inputs=(value,), outputs=(statement.name,), attributes={"type": typ.signature()}))
        elif isinstance(statement, Return):
            value, result = _expr(statement.value, env, operations, counter)
            operations.append(Operation("return", inputs=(value,)))
        else:
            raise OmniLoweringError(f"unsupported statement: {type(statement).__name__}")
    if result == _VOID:
        raise OmniLoweringError(f"function has no return: {function.name}")
    return FunctionIR(function.name, {name: _INT for name in function.parameters}, result, (BasicBlock("entry", tuple(operations)),))


def lower_program(program: Program, *, module_name: str = "omni_module") -> ModuleIR:
    if not program.functions: raise OmniLoweringError("program contains no functions")
    module = ModuleIR(module_name, {}, tuple(_function(function) for function in program.functions))
    module.validate()
    return module


def lower_source(source: str, *, module_name: str = "omni_module") -> ModuleIR:
    from .omni_source import parse
    return lower_program(parse(source), module_name=module_name)
