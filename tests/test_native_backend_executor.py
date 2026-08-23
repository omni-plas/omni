from omni.native_backend_executor import prepare_function
from omni.ir import BasicBlock, FunctionIR, Operation
from omni.types import TypeKind, TypeRef


def test_prepare_function_maps_values():
    integer = TypeRef(TypeKind.INTEGER)
    fn = FunctionIR("f", {}, integer, (BasicBlock("entry", (Operation("const", outputs=("x",), attributes={"value": 1}), Operation("return", ("x",)))),))
    prepared = prepare_function(fn, (3,))
    assert prepared.values[0].name == "x"
    assert prepared.values[0].register == 3
