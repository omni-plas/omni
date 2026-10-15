"""Static semantic checks over Omni's executable IR."""

from __future__ import annotations

from dataclasses import dataclass

from .ir import BasicBlock, FunctionIR, ModuleIR, Operation
from .types import TypeKind, TypeRef


@dataclass(frozen=True)
class TypeDiagnostic:
    code: str
    message: str
    function: str | None = None
    block: str | None = None
    value: str | None = None


def _compatible(left: TypeRef, right: TypeRef) -> bool:
    if left.kind == TypeKind.ANY or right.kind == TypeKind.ANY:
        return True
    if left.kind != right.kind or left.nullable != right.nullable:
        return False
    if left.name != right.name or left.bits != right.bits or left.signed != right.signed or len(left.parameters) != len(right.parameters):
        return False
    if set(left.fields) != set(right.fields):
        return False
    return all(_compatible(a, b) for a, b in zip(left.parameters, right.parameters)) and all(
        _compatible(left.fields[name], right.fields[name]) for name in left.fields
    )


def _diag(code: str, message: str, function: FunctionIR, block: BasicBlock, value: str | None = None) -> TypeDiagnostic:
    return TypeDiagnostic(code, message, function.name, block.name, value)


def check_module(module: ModuleIR) -> tuple[TypeDiagnostic, ...]:
    diagnostics: list[TypeDiagnostic] = []
    try:
        module.validate()
    except ValueError as exc:
        diagnostics.append(TypeDiagnostic("IR001", str(exc)))
        return tuple(diagnostics)
    for function in module.functions:
        diagnostics.extend(_check_function(function))
    return tuple(diagnostics)


def _check_function(function: FunctionIR) -> list[TypeDiagnostic]:
    diagnostics: list[TypeDiagnostic] = []
    definitions = dict(function.parameters)
    terminated = False
    for block in function.blocks:
        terminated = False
        for operation in block.operations:
            if terminated:
                diagnostics.append(_diag("IR008", "operation appears after a terminator", function, block))
                continue
            for name in operation.inputs:
                if name not in definitions:
                    diagnostics.append(_diag("IR002", f"use of undefined value: {name}", function, block, name))
            if len(operation.outputs) != len(set(operation.outputs)):
                diagnostics.append(_diag("IR003", f"duplicate operation output: {operation.opcode}", function, block))
            declared = operation.input_types or operation.attributes.get("input_types")
            if declared is not None:
                if not isinstance(declared, (list, tuple)) or len(declared) != len(operation.inputs):
                    diagnostics.append(_diag("IR004", "input_types must match operation inputs", function, block))
                else:
                    for value_name, expected in zip(operation.inputs, declared):
                        if value_name in definitions and isinstance(expected, TypeRef) and not _compatible(definitions[value_name], expected):
                            diagnostics.append(_diag("IR005", f"type mismatch for value: {value_name}", function, block, value_name))
            output_type = operation.attributes.get("output_type")
            if output_type is not None and not isinstance(output_type, TypeRef):
                diagnostics.append(_diag("IR006", "output_type must be a TypeRef", function, block))
            for index, output in enumerate(operation.outputs):
                if output in definitions and operation.opcode == "move":
                    # move is the assignment operation for mutable locals; keep
                    # the original definition contract and refresh its inferred
                    # type from the assigned value when known.
                    if len(operation.inputs) == 1 and operation.inputs[0] in definitions:
                        source_type = definitions[operation.inputs[0]]
                        target_type = definitions[output]
                        if target_type.kind != TypeKind.ANY and source_type.kind != TypeKind.ANY and not _compatible(target_type, source_type):
                            diagnostics.append(_diag("IR005", f"type mismatch for assignment: {output}", function, block, output))
                        definitions[output] = source_type
                    continue
                if output in definitions:
                    diagnostics.append(_diag("IR007", f"redefinition of value: {output}", function, block, output))
                else:
                    inferred_type = output_type
                    if inferred_type is None and operation.output_types:
                        inferred_type = operation.output_types[index]
                    definitions[output] = inferred_type if isinstance(inferred_type, TypeRef) else TypeRef(TypeKind.ANY)
            if operation.opcode in {"return", "branch", "jump"}:
                terminated = True
    return diagnostics


def is_valid(module: ModuleIR) -> bool:
    return not check_module(module)
