from omni.native_allocator_bridge import plan_native_allocation
from omni.ir import BasicBlock, FunctionIR, Operation
from omni.types import TypeKind, TypeRef


def test_native_plan_spills_when_registers_are_exhausted():
    integer = TypeRef(TypeKind.INTEGER)
    ops = tuple(Operation("const", outputs=(name,), attributes={"value": i}) for i, name in enumerate(("a", "b", "c")))
    ops += (Operation("add", ("a", "b"), ("d",)), Operation("add", ("d", "c"), ("e",)), Operation("return", ("e",)))
    fn = FunctionIR("f", {}, integer, (BasicBlock("entry", ops),))
    plan = plan_native_allocation(fn, (3, 4))
    assert plan.stack_size >= 8
