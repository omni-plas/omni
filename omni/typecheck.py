"""Static semantic checks over Omni's executable IR."""

from __future__ import annotations

from dataclasses import dataclass

from .ir import FunctionIR, ModuleIR
from .types import TypeKind, TypeRef


@dataclass(frozen=True)
class TypeDiagnostic:
    code: str
    message: str
    function: str | None = None
    block: str | None = None


def _compatible(left: TypeRef, right: TypeRef) -> bool:
    if left.kind == TypeKind.ANY or right.kind == TypeKind.ANY:
        return True
    if left.kind != right.kind or left.nullable != right.nullable:
        return False
    if left.name != right.name or len(left.parameters) != len(right.parameters):
        return False
    return all(_compatible(a, b) for a, b in zip(left.parameters, right.parameters))


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
    for block in function.blocks:
        for operation in block.operations:
            for name in operation.inputs:
                if name not in definitions:
                    diagnostics.append(TypeDiagnostic("IR002", f"use of undefined value: {name}", function.name, block.name))
            if len(operation.outputs) != len(set(operation.outputs)):
                diagnostics.append(TypeDiagnostic("IR003", f"duplicate operation output: {operation.opcode}", function.name, block.name))
            declared = operation.attributes.get("input_types")
            if declared is not None:
                if not isinstance(declared, (list, tuple)) or len(declared) != len(operation.inputs):
                    diagnostics.append(TypeDiagnostic("IR004", "input_types must match operation inputs", function.name, block.name))
                else:
                    for value_name, expected in zip(operation.inputs, declared):
                        if value_name in definitions and isinstance(expected, TypeRef) and not _compatible(definitions[value_name], expected):
                            diagnostics.append(TypeDiagnostic("IR005", f"type mismatch for value: {value_name}", function.name, block.name))
            output_type = operation.attributes.get("output_type")
            if output_type is not None and not isinstance(output_type, TypeRef):
                diagnostics.append(TypeDiagnostic("IR006", "output_type must be a TypeRef", function.name, block.name))
            for output in operation.outputs:
                if output in definitions:
                    diagnostics.append(TypeDiagnostic("IR007", f"redefinition of value: {output}", function.name, block.name))
                elif isinstance(output_type, TypeRef):
                    definitions[output] = output_type
                else:
                    definitions[output] = TypeRef(TypeKind.ANY)
    return diagnostics


def is_valid(module: ModuleIR) -> bool:
    return not check_module(module)
