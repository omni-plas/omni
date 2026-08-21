import pytest

from omni.ir import BasicBlock, FunctionIR, Operation
from omni.runtime import RuntimeErrorBase, execute
from omni.types import TypeKind, TypeRef


def test_reference_runtime_executes_arithmetic_function():
    integer = TypeRef(TypeKind.INTEGER)
    function = FunctionIR("main", {"x": integer, "y": integer}, integer, (BasicBlock("entry", (
        Operation("add", inputs=("x", "y"), outputs=("sum",)), Operation("return", inputs=("sum",)),
    )),))
    assert execute(function, {"x": 2, "y": 3}) == 5


def test_reference_runtime_executes_conditional_branch():
    integer = TypeRef(TypeKind.INTEGER)
    function = FunctionIR("max", {"x": integer, "y": integer}, integer, (
        BasicBlock("entry", (Operation("cmp_lt", inputs=("x", "y"), outputs=("is_less",)), Operation("branch", inputs=("is_less",), attributes={"true": "less", "false": "not_less"})), ("less", "not_less")),
        BasicBlock("less", (Operation("return", inputs=("y",)),)),
        BasicBlock("not_less", (Operation("return", inputs=("x",)),)),
    ))
    assert execute(function, {"x": 2, "y": 3}) == 3
    assert execute(function, {"x": 5, "y": 3}) == 5


def test_reference_runtime_supports_boolean_ops():
    boolean = TypeRef(TypeKind.BOOL)
    function = FunctionIR("predicate", {"x": boolean, "y": boolean}, boolean, (BasicBlock("entry", (
        Operation("and", inputs=("x", "y"), outputs=("both",)),
        Operation("not", inputs=("both",), outputs=("neither",)),
        Operation("return", inputs=("neither",)),
    )),))
    assert execute(function, {"x": True, "y": True}) is False
    assert execute(function, {"x": True, "y": False}) is True


def test_reference_runtime_supports_extended_comparisons():
    integer, boolean = TypeRef(TypeKind.INTEGER), TypeRef(TypeKind.BOOL)
    function = FunctionIR("compare", {"x": integer, "y": integer}, boolean, (BasicBlock("entry", (
        Operation("cmp_ge", inputs=("x", "y"), outputs=("ge",)), Operation("return", inputs=("ge",)),
    )),))
    assert execute(function, {"x": 4, "y": 4}) is True
    assert execute(function, {"x": 3, "y": 4}) is False


def test_reference_runtime_rejects_missing_argument():
    integer = TypeRef(TypeKind.INTEGER)
    function = FunctionIR("main", {"x": integer}, integer, (BasicBlock("entry", (Operation("return", inputs=("x",)),)),))
    with pytest.raises(RuntimeErrorBase, match="missing argument"):
        execute(function)


def test_reference_runtime_rejects_missing_return():
    integer = TypeRef(TypeKind.INTEGER)
    function = FunctionIR("main", {}, integer, (BasicBlock("entry", ()),))
    with pytest.raises(RuntimeErrorBase, match="without return"):
        execute(function)


def test_reference_runtime_rejects_division_by_zero():
    integer = TypeRef(TypeKind.INTEGER)
    function = FunctionIR("main", {"x": integer, "y": integer}, integer, (BasicBlock("entry", (
        Operation("div", inputs=("x", "y"), outputs=("result",)), Operation("return", inputs=("result",)),
    )),))
    with pytest.raises(RuntimeErrorBase, match="division by zero"):
        execute(function, {"x": 1, "y": 0})
