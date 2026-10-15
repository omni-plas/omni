"""Semantic IR validation beyond structural dataclass checks."""

from __future__ import annotations

from .ir import FunctionIR, ModuleIR


class SemanticValidationError(ValueError):
    """Raised when executable semantic IR violates its data-flow contract."""


# This is the executable subset understood by the deterministic reference
# runtime. Keep this contract aligned with runtime._execute_operation.
SUPPORTED_REFERENCE_OPCODES = frozenset({
    "const", "move", "add", "sub", "mul", "div", "compare",
    "cmp_eq", "cmp_lt", "cmp_ge", "cmp_le", "cmp_gt", "cmp_ne",
    "and", "or", "not", "branch", "jump", "call", "return",
})
_TERMINATORS = frozenset({"branch", "jump", "return"})
_BINARY_OPS = frozenset({
    "add", "sub", "mul", "div", "compare", "cmp_eq", "cmp_lt",
    "cmp_ge", "cmp_le", "cmp_gt", "cmp_ne", "and", "or",
})


def validate_function(function: FunctionIR) -> None:
    defined = set(function.parameters)
    return_seen = False

    for block in function.blocks:
        block_terminated = False
        for operation in block.operations:
            opcode = operation.opcode
            if opcode not in SUPPORTED_REFERENCE_OPCODES:
                raise SemanticValidationError(f"unsupported reference opcode: {opcode}")
            if block_terminated:
                raise SemanticValidationError("operations are not allowed after a terminator")

            # Check opcode shape before mutating the definition set so malformed
            # operations report their actual contract violation first.
            if opcode == "const":
                if len(operation.outputs) != 1 or operation.inputs or "value" not in operation.attributes:
                    raise SemanticValidationError("const requires one output, no inputs, and a value")
            elif opcode == "move":
                if len(operation.inputs) != 1 or len(operation.outputs) != 1:
                    raise SemanticValidationError("move requires one input and one output")
            elif opcode in _BINARY_OPS:
                if len(operation.inputs) != 2 or len(operation.outputs) != 1:
                    raise SemanticValidationError(f"{opcode} requires two inputs and one output")
                if opcode == "compare" and operation.attributes.get("operator") not in {
                    "eq", "ne", "lt", "le", "gt", "ge"
                }:
                    raise SemanticValidationError("compare requires a supported operator")
            elif opcode == "not":
                if len(operation.inputs) != 1 or len(operation.outputs) != 1:
                    raise SemanticValidationError("not requires one input and one output")
            elif opcode == "call":
                if not isinstance(operation.attributes.get("callee"), str) or not operation.attributes["callee"].strip():
                    raise SemanticValidationError("call requires a non-empty callee")
                if len(operation.outputs) > 1:
                    raise SemanticValidationError("call accepts at most one output")
            elif opcode == "return":
                if len(operation.inputs) > 1 or operation.outputs:
                    raise SemanticValidationError("return accepts at most one input and no outputs")
            elif opcode == "branch":
                if len(operation.inputs) != 1 or operation.outputs:
                    raise SemanticValidationError("branch requires one condition input and no outputs")
                if set(operation.attributes) != {"true", "false"}:
                    raise SemanticValidationError("branch requires true and false targets")
                if not all(
                    isinstance(operation.attributes[key], str) and operation.attributes[key].strip()
                    for key in ("true", "false")
                ):
                    raise SemanticValidationError("branch targets must be non-empty strings")
            elif opcode == "jump":
                target = operation.attributes.get("target")
                if operation.inputs or operation.outputs or not isinstance(target, str) or not target.strip():
                    raise SemanticValidationError("jump requires a non-empty target and no inputs or outputs")

            for name in operation.inputs:
                if name not in defined:
                    raise SemanticValidationError(f"operation uses undefined value: {name}")
            for name in operation.outputs:
                # 'move' is the reference runtime's assignment operation, so it
                # may update an existing mutable local. Other operations define
                # new values and must not silently overwrite prior definitions.
                if name in defined and opcode != "move":
                    raise SemanticValidationError(f"operation redefines value: {name}")
                defined.add(name)

            if opcode in _TERMINATORS:
                block_terminated = True

        if block_terminated and block.operations[-1].opcode == "branch":
            branch = block.operations[-1]
            if len(block.successors) != 2:
                raise SemanticValidationError("branch block requires exactly two successors")
            expected = {branch.attributes["true"], branch.attributes["false"]}
            if set(block.successors) != expected:
                raise SemanticValidationError("branch successors must match branch targets")
        elif block_terminated and block.operations[-1].opcode == "jump":
            target = block.operations[-1].attributes["target"]
            if tuple(block.successors) != (target,):
                raise SemanticValidationError("jump successor must match jump target")
        elif block_terminated and block.operations[-1].opcode == "return":
            return_seen = True

    if not return_seen:
        raise SemanticValidationError(f"function has no return: {function.name}")


def validate_module(module: ModuleIR) -> None:
    """Validate executable semantics before structural CFG checks for precise diagnostics."""
    # Semantic validation first gives branch-target mismatches a useful,
    # deterministic error even when a mismatched target is not a declared block.
    for function in module.functions:
        validate_function(function)
    module.validate()
