from omni.native_pipeline import prepare_module
from omni.ir import BasicBlock, FunctionIR, IRModule, Operation
from omni.types import TypeKind, TypeRef


def test_prepare_module_validates_and_allocates_functions():
    integer = TypeRef(TypeKind.INTEGER)
    fn = FunctionIR("f", {}, integer, (BasicBlock("entry", (Operation("const", outputs=("x",), attributes={"value": 1}), Operation("return", ("x",)))),))
    module = IRModule((fn,))
    prepared = prepare_module(module, (3,))
    assert len(prepared.functions) == 1
    assert prepared.functions[0].allocation.values[0].location.register == 3
