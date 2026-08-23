from omni.native_ir_executable import compile_function_to_elf
from omni.ir import BasicBlock, FunctionIR, Operation
from omni.types import TypeKind, TypeRef


def test_ir_compiles_to_native_code():
    integer=TypeRef(TypeKind.INTEGER)
    fn=FunctionIR("f", {}, integer, (BasicBlock("entry", (
        Operation("const", outputs=("a",), attributes={"value":2}),
        Operation("const", outputs=("b",), attributes={"value":3}),
        Operation("add", inputs=("a","b"), outputs=("c",)),
        Operation("return", inputs=("c",)),
    )),))
    code=compile_function_to_elf(fn,(3,4,5))
    assert code.endswith(b"\xc3")
    assert len(code)>10
