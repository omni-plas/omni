from omni.native_allocating_emitter import prepare_native_function
from omni.ir import BasicBlock, FunctionIR, Operation
from omni.types import TypeKind, TypeRef


def test_native_preparation_builds_frame_from_allocation():
    integer = TypeRef(TypeKind.INTEGER)
    fn = FunctionIR("f", {}, integer, (BasicBlock("entry", (Operation("const", outputs=("x",), attributes={"value": 1}), Operation("return", ("x",)))),))
    prepared = prepare_native_function(fn, (3,))
    assert prepared.allocation.values[0].location.register == 3
    assert prepared.frame.stack_size == 0
