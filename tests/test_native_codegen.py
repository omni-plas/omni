import struct

from omni.ir import BasicBlock, FunctionIR, ModuleIR, Operation
from omni.native_codegen import emit_x86_64_elf
from omni.targets import TargetDescriptor
from omni.types import TypeKind, TypeRef


def _module():
    i64 = TypeRef(TypeKind.INT, bits=64)
    return ModuleIR(
        "hello",
        {},
        (FunctionIR(
            "main_value", {}, i64,
            (BasicBlock("entry", (
                Operation("const", outputs=("a",), attributes={"value": 40}),
                Operation("const", outputs=("b",), attributes={"value": 2}),
                Operation("add", inputs=("a", "b"), outputs=("sum",)),
                Operation("return", inputs=("sum",)),
            )),),
        ),),
    )


def test_x86_64_elf_header_and_entry():
    target = TargetDescriptor("linux", "x86_64", "sysv", {"native-executable": True})
    executable = emit_x86_64_elf(_module(), target)
    assert executable.format == "elf-x86_64"
    assert executable.payload[:4] == b"\x7fELF"
    assert executable.payload[4] == 2
    assert executable.payload[5] == 1
    assert struct.unpack_from("<H", executable.payload, 18)[0] == 62
    assert len(executable.payload) > 120


def test_x86_64_output_is_deterministic():
    target = TargetDescriptor("linux", "x86_64", "sysv", {"native-executable": True})
    assert emit_x86_64_elf(_module(), target).payload == emit_x86_64_elf(_module(), target).payload
