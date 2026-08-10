"""Static semantic checks over Omni's executable IR."""

from __future__ import annotations

from dataclasses import dataclass

from .ir import FunctionIR, ModuleIR


@dataclass(frozen=True)
class TypeDiagnostic:
    code: str
    message: str
    function: str | None = None
    block: str | None = None


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
    definitions = set(function.parameters)
    for block in function.blocks:
        for operation in block.operations:
            for name in operation.inputs:
                if name not in definitions:
                    diagnostics.append(TypeDiagnostic("IR002", f"use of undefined value: {name}", function.name, block.name))
            if len(operation.outputs) != len(set(operation.outputs)):
                diagnostics.append(TypeDiagnostic("IR003", f"duplicate operation output: {operation.opcode}", function.name, block.name))
            definitions.update(operation.outputs)
    return diagnostics


def is_valid(module: ModuleIR) -> bool:
    return not check_module(module)
