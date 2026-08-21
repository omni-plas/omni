import pytest

from omni.ir import BasicBlock, FunctionIR, Operation
from omni.runtime import RuntimeErrorBase, execute
from omni.types import TypeKind, TypeRef


def test_reference_runtime_executes_arithmetic_function():
    integer = TypeRef(TypeKind.INTEGER)
    function = FunctionIR(
        name="main", parameters={"x": integer, "y": integer}, result=integer,
        blocks=(BasicBlock(name="entry", operations=(
            Operation("add", inputs=("x", "y"), outputs=("sum",)),
            Operation("return", inputs=("sum",)),
        )),),
    )
    assert execute(function, {"x": 2, "y": 3}) == 5


def test_reference_runtime_executes_conditional_branch():
    integer = TypeRef(TypeKind.INTEGER)
    boolean = TypeRef(TypeKind.BOOLEAN)
    function = FunctionIR(
        name="max", parameters={"x": integer, "y": integer}, result=integer,
        blocks=(
            BasicBlock(name="entry", operations=(
                Operation("cmp_lt", inputs=("x", "y"), outputs=("is_less",)),
                Operation("branch", inputs=("is_less",), attributes={"true": "less", "false": "not_less"}),
            ), successors=("less", "not_less")),
            BasicBlock(name="less", operations=(Operation("return", inputs=("y",)),)),
            BasicBlock(name="not_less", operations=(Operation("return", inputs=("x",)),)),
        ),
    )
    assert execute(function, {"x": 2, "y": 3}) == 3
    assert execute(function, {"x": 5, "y": 3}) == 5


def test_reference_runtime_rejects_missing_return():
    integer = TypeRef(TypeKind.INTEGER)
    function = FunctionIR(name="main", parameters={}, result=integer, blocks=(BasicBlock(name="entry", operations=()),))
    with pytest.raises(RuntimeErrorBase, match="without return"):
        execute(function)


def test_reference_runtime_rejects_division_by_zero():
    integer = TypeRef(TypeKind.INTEGER)
    function = FunctionIR(
        name="main", parameters={"x": integer, "y": integer}, result=integer,
        blocks=(BasicBlock(name="entry", operations=(
            Operation("div", inputs=("x", "y"), outputs=("result",)),
            Operation("return", inputs=("result",)),
        )),),
    )
    with pytest.raises(RuntimeErrorBase, match="division by zero"):
        execute(function, {"x": 1, "y": 0})
