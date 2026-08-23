from omni.native_ir_emitter import lower_function, emit_lowered
from omni.ir import BasicBlock, FunctionIR, Operation
from omni.types import TypeKind, TypeRef


def test_function_ir_const_add_return_lowers_to_machine_code():
    integer=TypeRef(TypeKind.INTEGER)
    fn=FunctionIR("f", {}, integer, (BasicBlock("entry", (
        Operation("const", outputs=("a",), attributes={"value":2}),
        Operation("const", outputs=("b",), attributes={"value":3}),
        Operation("add", inputs=("a","b"), outputs=("c",)),
        Operation("return", inputs=("c",)),
    )),))
    lowered=lower_function(fn,{"a":3,"b":4,"c":3})
    emitted=emit_lowered(lowered)
    assert emitted.code.endswith(b"\xc3")
    assert len(emitted.code)>10
