"""Small deterministic interpreter for executable Omni IR."""

from __future__ import annotations

from .ir import ModuleIR


class OmniRuntimeError(RuntimeError):
    pass


def _compare(operator: str, left: int, right: int) -> bool:
    comparisons = {
        "eq": lambda: left == right,
        "ne": lambda: left != right,
        "lt": lambda: left < right,
        "le": lambda: left <= right,
        "gt": lambda: left > right,
        "ge": lambda: left >= right,
    }
    try:
        return comparisons[operator]()
    except KeyError as exc:
        raise OmniRuntimeError(f"unsupported comparison: {operator}") from exc


def execute_function(module: ModuleIR, function_name: str, arguments: tuple[int, ...] = ()) -> int:
    module.validate()
    matches = [fn for fn in module.functions if fn.name == function_name]
    if len(matches) != 1:
        raise OmniRuntimeError(f"function not found or ambiguous: {function_name}")
    function = matches[0]
    if len(arguments) != len(function.parameters):
        raise OmniRuntimeError(f"expected {len(function.parameters)} arguments, got {len(arguments)}")
    values: dict[str, int | bool] = dict(zip(function.parameters, arguments))
    blocks = {block.name: block for block in function.blocks}
    current = function.blocks[0].name
    visited = 0
    while True:
        visited += 1
        if visited > 1_000_000:
            raise OmniRuntimeError("control-flow execution limit exceeded")
        block = blocks[current]
        jumped = False
        for op in block.operations:
            if op.opcode == "const":
                values[op.outputs[0]] = op.attributes["value"]
            elif op.opcode == "move":
                values[op.outputs[0]] = values[op.inputs[0]]
            elif op.opcode in {"add", "sub", "mul", "div"}:
                left, right = int(values[op.inputs[0]]), int(values[op.inputs[1]])
                if op.opcode == "add": result = left + right
                elif op.opcode == "sub": result = left - right
                elif op.opcode == "mul": result = left * right
                else:
                    if right == 0: raise OmniRuntimeError("division by zero")
                    result = int(left / right)
                values[op.outputs[0]] = result
            elif op.opcode == "compare":
                values[op.outputs[0]] = _compare(op.attributes.get("operator"), int(values[op.inputs[0]]), int(values[op.inputs[1]]))
            elif op.opcode == "jump":
                target = op.attributes.get("target")
                if target not in blocks: raise OmniRuntimeError(f"unknown jump target: {target}")
                current = target; jumped = True; break
            elif op.opcode in {"branch", "cond_branch"}:
                if not op.inputs: raise OmniRuntimeError("branch requires a condition")
                target = op.attributes.get("true") if bool(values[op.inputs[0]]) else op.attributes.get("false")
                if target not in blocks: raise OmniRuntimeError(f"unknown branch target: {target}")
                current = target; jumped = True; break
            elif op.opcode == "return":
                return int(values[op.inputs[0]])
            else:
                raise OmniRuntimeError(f"unsupported runtime operation: {op.opcode}")
        if jumped:
            continue
        if block.successors:
            if len(block.successors) != 1:
                raise OmniRuntimeError(f"implicit multi-way control flow in block: {block.name}")
            current = block.successors[0]
            continue
        raise OmniRuntimeError(f"function has no return: {function_name}")
