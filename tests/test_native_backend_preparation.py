from omni.native_backend import prepare_native_function_for_backend
from omni.ir import BasicBlock, FunctionIR, Operation
from omni.types import TypeKind, TypeRef


def test_backend_exposes_shared_allocator_preparation():
    integer = TypeRef(TypeKind.INTEGER)
    fn = FunctionIR("f", {}, integer, (BasicBlock("entry", (Operation("const", outputs=("x",), attributes={"value": 1}), Operation("return", ("x",)))),))
    prepared = prepare_native_function_for_backend(fn, (3,))
    assert prepared.values[0].location.register == 3
