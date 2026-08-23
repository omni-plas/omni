import pytest

from omni.ir import BasicBlock, FunctionIR, ModuleIR, Operation
from omni.native_codegen import emit_x86_64_elf
from omni.native_validation import validate_x86_64_elf
from omni.types import TypeKind, TypeRef


def _module():
    i64 = TypeRef(TypeKind.INT, bits=64)
    block = BasicBlock("entry", (
        Operation("const", outputs=("v",), attributes={"value": 42}),
        Operation("return", inputs=("v",)),
    ))
    return ModuleIR("main", {}, (FunctionIR("main", {}, i64, (block,)),))


def test_valid_native_elf_passes():
    executable = emit_x86_64_elf(_module())
    validate_x86_64_elf(executable)


def test_invalid_magic_is_rejected():
    executable = emit_x86_64_elf(_module())
    broken = type(executable)(executable.target, b"BAD" + executable.payload[3:])
    with pytest.raises(ValueError, match="magic"):
        validate_x86_64_elf(broken)
