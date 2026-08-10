"""Semantic IR validation beyond structural dataclass checks."""

from __future__ import annotations

from .ir import FunctionIR, ModuleIR


class SemanticValidationError(ValueError):
    """Raised when executable semantic IR violates its data-flow contract."""


SUPPORTED_REFERENCE_OPCODES = frozenset({"const", "add", "sub", "mul", "div", "return"})


def validate_function(function: FunctionIR) -> None:
    defined = set(function.parameters)
    return_seen = False

    for block in function.blocks:
        for operation in block.operations:
            if operation.opcode not in SUPPORTED_REFERENCE_OPCODES:
                raise SemanticValidationError(f"unsupported reference opcode: {operation.opcode}")
            if return_seen:
                raise SemanticValidationError("operations are not allowed after return")
            for name in operation.inputs:
                if name not in defined:
                    raise SemanticValidationError(f"operation uses undefined value: {name}")
            for name in operation.outputs:
                if name in defined:
                    raise SemanticValidationError(f"operation redefines value: {name}")
                defined.add(name)
            if operation.opcode == "const" and "value" not in operation.attributes:
                raise SemanticValidationError("const requires a value attribute")
            if operation.opcode == "return":
                return_seen = True

    if not return_seen:
        raise SemanticValidationError(f"function has no return: {function.name}")


def validate_module(module: ModuleIR) -> None:
    """Validate both structural IR and executable reference semantics."""
    module.validate()
    for function in module.functions:
        validate_function(function)
