from omni.native_allocator_bridge import plan_native_allocation
from omni.ir import BasicBlock, FunctionIR, Operation
from omni.types import TypeKind, TypeRef


def test_native_plan_exposes_registers_and_stack():
    integer = TypeRef(TypeKind.INTEGER)
    fn = FunctionIR("f", {"x": integer}, integer, (BasicBlock("entry", (Operation("return", ("x",)),)),))
    plan = plan_native_allocation(fn, (3, 4))
    assert plan.registers["x"] == 3
    assert plan.stack_size == 0
