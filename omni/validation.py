"""Semantic IR validation beyond structural dataclass checks."""

from __future__ import annotations

from .ir import FunctionIR, ModuleIR


class SemanticValidationError(ValueError):
    """Raised when executable semantic IR violates its data-flow contract."""


SUPPORTED_REFERENCE_OPCODES = frozenset({
    "const", "add", "sub", "mul", "div", "cmp_eq", "cmp_lt", "cmp_ge",
    "and", "or", "not", "branch", "return",
})
_TERMINATORS = frozenset({"branch", "return"})
_BINARY_OPS = frozenset({"add", "sub", "mul", "div", "cmp_eq", "cmp_lt", "cmp_ge", "and", "or"})


def validate_function(function: FunctionIR) -> None:
    defined = set(function.parameters)
    return_seen = False

    for block in function.blocks:
        block_terminated = False
        for operation in block.operations:
            if operation.opcode not in SUPPORTED_REFERENCE_OPCODES:
                raise SemanticValidationError(f"unsupported reference opcode: {operation.opcode}")
            if block_terminated:
                raise SemanticValidationError("operations are not allowed after a terminator")
            for name in operation.inputs:
                if name not in defined:
                    raise SemanticValidationError(f"operation uses undefined value: {name}")
            for name in operation.outputs:
                if name in defined:
                    raise SemanticValidationError(f"operation redefines value: {name}")
                defined.add(name)

            if operation.opcode == "const" and (len(operation.outputs) != 1 or "value" not in operation.attributes):
                raise SemanticValidationError("const requires one output and a value")
            if operation.opcode in _BINARY_OPS and (len(operation.inputs) != 2 or len(operation.outputs) != 1):
                raise SemanticValidationError(f"{operation.opcode} requires two inputs and one output")
            if operation.opcode == "not" and (len(operation.inputs) != 1 or len(operation.outputs) != 1):
                raise SemanticValidationError("not requires one input and one output")
            if operation.opcode == "return" and len(operation.inputs) > 1:
                raise SemanticValidationError("return accepts at most one input")
            if operation.opcode == "branch":
                if len(operation.inputs) != 1:
                    raise SemanticValidationError("branch requires one condition input")
                if set(operation.attributes) != {"true", "false"}:
                    raise SemanticValidationError("branch requires true and false targets")
                if not all(isinstance(operation.attributes[key], str) and operation.attributes[key].strip() for key in ("true", "false")):
                    raise SemanticValidationError("branch targets must be non-empty strings")

            if operation.opcode in _TERMINATORS:
                block_terminated = True

        if block_terminated and block.operations[-1].opcode == "branch":
            if len(block.successors) != 2:
                raise SemanticValidationError("branch block requires exactly two successors")
            expected = {block.operations[-1].attributes["true"], block.operations[-1].attributes["false"]}
            if set(block.successors) != expected:
                raise SemanticValidationError("branch successors must match branch targets")
        elif block_terminated and block.operations[-1].opcode == "return":
            return_seen = True

    if not return_seen:
        raise SemanticValidationError(f"function has no return: {function.name}")


def validate_module(module: ModuleIR) -> None:
    """Validate both structural IR and executable reference semantics."""
    module.validate()
    for function in module.functions:
        validate_function(function)
