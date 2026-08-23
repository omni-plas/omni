from omni.native_allocator_codegen import allocate_function
from omni.ir import BasicBlock, FunctionIR, Operation
from omni.types import TypeKind, TypeRef


def test_allocate_function_uses_shared_allocator():
    integer = TypeRef(TypeKind.INTEGER)
    fn = FunctionIR("f", {}, integer, (BasicBlock("entry", (Operation("const", outputs=("x",), attributes={"value": 1}), Operation("return", ("x",)))),))
    result = allocate_function(fn, (3,))
    assert result.values[0].name == "x"
    assert result.values[0].location.register == 3
