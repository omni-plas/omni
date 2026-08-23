import struct

import pytest

from omni.ir import BasicBlock, FunctionIR, ModuleIR, Operation
from omni.native_codegen import NativeCodegenError, emit_x86_64_elf
from omni.targets import TargetDescriptor
from omni.types import TypeKind, TypeRef


def _module():
    integer = TypeRef(TypeKind.INTEGER)
    return ModuleIR(
        "hello",
        {},
        (FunctionIR(
            "main_value", {}, integer,
            (BasicBlock("entry", (
                Operation("const", outputs=("a",), attributes={"value": 40}),
                Operation("const", outputs=("b",), attributes={"value": 2}),
                Operation("add", inputs=("a", "b"), outputs=("sum",)),
                Operation("return", inputs=("sum",)),
            )),),
        ),),
    )


def _parameter_module(parameter_count: int = 2):
    integer = TypeRef(TypeKind.INTEGER)
    names = tuple((f"p{i}", integer) for i in range(parameter_count))
    parameters = dict(names)
    operations = (
        Operation("add", inputs=("p0", "p1"), outputs=("sum",)),
        Operation("return", inputs=("sum",)),
    )
    return ModuleIR("params", {}, (FunctionIR("main_value", parameters, integer, (BasicBlock("entry", operations),)),))


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


def test_x86_64_accepts_integer_parameters():
    executable = emit_x86_64_elf(_parameter_module())
    assert executable.payload[:4] == b"\x7fELF"


def test_x86_64_rejects_more_than_six_parameters():
    with pytest.raises(NativeCodegenError, match="at most six"):
        emit_x86_64_elf(_parameter_module(7))


def test_x86_64_rejects_non_integer_parameter():
    string_type = TypeRef(TypeKind.STRING)
    integer = TypeRef(TypeKind.INTEGER)
    module = ModuleIR(
        "invalid",
        {},
        (FunctionIR("main", {"value": string_type}, integer, (BasicBlock("entry", (
            Operation("return", inputs=("value",)),
        )),)),),
    )
    with pytest.raises(NativeCodegenError, match="unsupported parameter type"):
        emit_x86_64_elf(module)
