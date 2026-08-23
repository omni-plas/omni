from omni.ir import BasicBlock, FunctionIR, ModuleIR, Operation
from omni.types import TypeKind, TypeRef
from omni.runtime import execute


def test_runtime_alloc_store_load_round_trip():
    i = TypeRef(TypeKind.INTEGER)
    ops = (
        Operation("const", outputs=("size",), attributes={"value": 8}),
        Operation("alloc", inputs=("size",), outputs=("ptr",)),
        Operation("const", outputs=("value",), attributes={"value": 12345}),
        Operation("store", inputs=("ptr", "value"), attributes={"width": 8}),
        Operation("load", inputs=("ptr",), outputs=("result",), attributes={"width": 8}),
        Operation("return", inputs=("result",)),
    )
    fn = FunctionIR("main", {}, i, (BasicBlock("entry", ops),))
    assert execute(fn) == 12345
