from omni.ir import BasicBlock, FunctionIR, ModuleIR, Operation
from omni.register_alloc import allocate, compute_intervals
from omni.types import TypeKind, TypeRef


def test_intervals_cover_uses_and_definitions():
    integer = TypeRef(TypeKind.INTEGER)
    fn = FunctionIR("f", {}, integer, (BasicBlock("entry", (
        Operation("const", outputs=("a",), attributes={"value": 1}),
        Operation("const", outputs=("b",), attributes={"value": 2}),
        Operation("add", inputs=("a", "b"), outputs=("c",)),
        Operation("return", inputs=("c",)),
    )),))
    intervals = {item.value: item for item in compute_intervals(fn)}
    assert intervals["a"].start == 0 and intervals["a"].end == 2
    assert intervals["c"].start == 2 and intervals["c"].end == 3


def test_allocator_spills_when_registers_are_exhausted():
    integer = TypeRef(TypeKind.INTEGER)
    fn = FunctionIR("f", {}, integer, (BasicBlock("entry", (
        Operation("const", outputs=("a",), attributes={"value": 1}),
        Operation("const", outputs=("b",), attributes={"value": 2}),
        Operation("add", inputs=("a", "b"), outputs=("c",)),
        Operation("return", inputs=("c",)),
    )),))
    result = allocate(fn, (1, 2))
    assert result.spills
    assert result.stack_size >= 8
