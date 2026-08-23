"""Recursive runtime for the executable textual Omni IR subset.

Unlike the minimal bootstrap runtime, this interpreter supports calls between
Omni functions and therefore provides a usable execution model for multi-
function programs during compiler bootstrapping.
"""

from __future__ import annotations

from .ir import FunctionIR, ModuleIR


class OmniRuntimeError(RuntimeError):
    pass


def execute_function(module: ModuleIR, function_name: str, arguments: tuple[int, ...] = (), *, max_depth: int = 256) -> int:
    module.validate()
    functions = {function.name: function for function in module.functions}
    if function_name not in functions:
        raise OmniRuntimeError(f"function not found: {function_name}")
    return _execute(functions, function_name, tuple(arguments), max_depth=max_depth, depth=0)


def _execute(functions: dict[str, FunctionIR], function_name: str, arguments: tuple[int, ...], *, max_depth: int, depth: int) -> int:
    if depth >= max_depth:
        raise OmniRuntimeError("maximum call depth exceeded")
    function = functions[function_name]
    if len(arguments) != len(function.parameters):
        raise OmniRuntimeError(f"expected {len(function.parameters)} arguments for {function_name}, got {len(arguments)}")
    values: dict[str, int] = dict(zip(function.parameters, arguments))
    for operation in function.blocks[0].operations:
        if operation.opcode == "const":
            value = operation.attributes.get("value")
            if not isinstance(value, int) or isinstance(value, bool):
                raise OmniRuntimeError("runtime bootstrap only supports integer constants")
            values[operation.outputs[0]] = value
        elif operation.opcode == "move":
            values[operation.outputs[0]] = values[operation.inputs[0]]
        elif operation.opcode in {"add", "sub", "mul", "div"}:
            left, right = values[operation.inputs[0]], values[operation.inputs[1]]
            if operation.opcode == "add": result = left + right
            elif operation.opcode == "sub": result = left - right
            elif operation.opcode == "mul": result = left * right
            else:
                if right == 0:
                    raise OmniRuntimeError("division by zero")
                result = int(left / right)
            values[operation.outputs[0]] = result
        elif operation.opcode == "call":
            callee = operation.attributes.get("callee")
            if not isinstance(callee, str) or callee not in functions:
                raise OmniRuntimeError(f"unknown callee: {callee!r}")
            call_args = tuple(values[name] for name in operation.inputs)
            values[operation.outputs[0]] = _execute(functions, callee, call_args, max_depth=max_depth, depth=depth + 1)
        elif operation.opcode == "return":
            try:
                return values[operation.inputs[0]]
            except KeyError as exc:
                raise OmniRuntimeError("return references an undefined value") from exc
        else:
            raise OmniRuntimeError(f"unsupported runtime operation: {operation.opcode}")
    raise OmniRuntimeError(f"function has no return: {function_name}")
