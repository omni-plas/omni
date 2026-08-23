from omni.ir import BasicBlock, FunctionIR, ModuleIR, Operation
from omni.native_codegen import emit_x86_64_elf
from omni.targets import TargetDescriptor
from omni.types import TypeKind, TypeRef


def test_native_codegen_emits_elf_for_add_sub_mul():
    i64 = TypeRef(TypeKind.INT, bits=64)
    block = BasicBlock("entry", (
        Operation("const", outputs=("a",), attributes={"value": 7}),
        Operation("const", outputs=("b",), attributes={"value": 5}),
        Operation("add", inputs=("a", "b"), outputs=("sum",)),
        Operation("sub", inputs=("sum", "b"), outputs=("diff",)),
        Operation("mul", inputs=("diff", "b"), outputs=("result",)),
        Operation("return", inputs=("result",)),
    ))
    module = ModuleIR("arith", {}, (FunctionIR("main", {}, i64, (block,)),))
    executable = emit_x86_64_elf(module, TargetDescriptor("linux", "x86_64", "sysv"))
    assert executable.payload.startswith(b"\x7fELF")
    assert len(executable.payload) > 64 + 56
