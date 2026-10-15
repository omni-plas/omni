from omni.native_pipeline import compile_function_module
from omni.ir import BasicBlock, FunctionIR, Operation
from omni.types import TypeKind, TypeRef


def test_function_module_pipeline_produces_elf():
    function = FunctionIR("main", {}, TypeRef(TypeKind.VOID), (BasicBlock("entry", (Operation("return"),)),))
    result = compile_function_module((function,), entry="main")
    assert result.executable[:4] == b"\x7fELF"
    assert result.symbols == {"main": 0}
