from omni.ir import BasicBlock, FunctionIR, ModuleIR, Operation
from omni.native_compile_facade import compile_module
from omni.types import TypeKind, TypeRef


def test_compile_facade_returns_elf():
    integer = TypeRef(TypeKind.INTEGER)
    function = FunctionIR(
        "main", {}, integer,
        (BasicBlock("entry", (
            Operation("const", outputs=("answer",), attributes={"value": 42}),
            Operation("return", inputs=("answer",)),
        )),),
    )
    result = compile_module(ModuleIR("facade-test", {}, (function,)))
    assert result.format == "elf-x86_64"
    assert result.payload[:4] == b"\x7fELF"
