"""Small deterministic interpreter for the textual Omni IR bootstrap subset."""

from __future__ import annotations

from .ir import ModuleIR


class OmniRuntimeError(RuntimeError):
    pass


def execute_function(module: ModuleIR, function_name: str, arguments: tuple[int, ...] = ()) -> int:
    module.validate()
    matches = [fn for fn in module.functions if fn.name == function_name]
    if len(matches) != 1:
        raise OmniRuntimeError(f"function not found or ambiguous: {function_name}")
    function = matches[0]
    if len(arguments) != len(function.parameters):
        raise OmniRuntimeError(f"expected {len(function.parameters)} arguments, got {len(arguments)}")
    values: dict[str, int] = dict(zip(function.parameters, arguments))
    for op in function.blocks[0].operations:
        if op.opcode == "const":
            values[op.outputs[0]] = op.attributes["value"]
        elif op.opcode == "move":
            values[op.outputs[0]] = values[op.inputs[0]]
        elif op.opcode in {"add", "sub", "mul", "div"}:
            left, right = values[op.inputs[0]], values[op.inputs[1]]
            if op.opcode == "add": result = left + right
            elif op.opcode == "sub": result = left - right
            elif op.opcode == "mul": result = left * right
            else:
                if right == 0: raise OmniRuntimeError("division by zero")
                result = int(left / right)
            values[op.outputs[0]] = result
        elif op.opcode == "return":
            return values[op.inputs[0]]
        else:
            raise OmniRuntimeError(f"unsupported runtime operation: {op.opcode}")
    raise OmniRuntimeError(f"function has no return: {function_name}")
