from omni.native_value_locations import resolve_function
from omni.ir import BasicBlock, FunctionIR, Operation
from omni.types import TypeKind, TypeRef


def test_resolver_exposes_register_location():
    integer=TypeRef(TypeKind.INTEGER)
    fn=FunctionIR("f", {}, integer, (BasicBlock("entry", (Operation("const", outputs=("x",), attributes={"value":1}), Operation("return", ("x",)))),))
    values=resolve_function(fn,(3,))
    assert values[0].register == 3
