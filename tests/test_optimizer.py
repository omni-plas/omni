from omni.ir import BasicBlock, FunctionIR, ModuleIR, Operation
from omni.optimize import optimize_module
from omni.types import TypeKind, TypeRef


def test_constant_folding_reduces_arithmetic():
    integer = TypeRef(TypeKind.INTEGER)
    fn = FunctionIR("main", {}, integer, (BasicBlock("entry", (
        Operation("const", outputs=("a",), attributes={"value": 20}),
        Operation("const", outputs=("b",), attributes={"value": 22}),
        Operation("add", inputs=("a", "b"), outputs=("sum",)),
        Operation("return", inputs=("sum",)),
    )),))
    result = optimize_module(ModuleIR("fold", {}, (fn,)))
    ops = result.functions[0].blocks[0].operations
    assert ops[-2].opcode == "const"
    assert ops[-2].attributes["value"] == 42
    assert ops[-1].opcode == "return"


def test_unreachable_block_is_removed():
    integer = TypeRef(TypeKind.INTEGER)
    fn = FunctionIR("main", {}, integer, (
        BasicBlock("entry", (Operation("const", outputs=("x",), attributes={"value": 1}), Operation("return", inputs=("x",)))),
        BasicBlock("dead", (Operation("return", inputs=("x",)),)),
    ))
    result = optimize_module(ModuleIR("reach", {}, (fn,)))
    assert [b.name for b in result.functions[0].blocks] == ["entry"]
