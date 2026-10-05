import subprocess

from omni.ir import BasicBlock, FunctionIR, ModuleIR, Operation
from omni.native_executable import compile_native_executable, write_native_executable
from omni.targets import TargetDescriptor
from omni.types import TypeKind, TypeRef


def _module():
    integer = TypeRef(TypeKind.INTEGER)
    block = BasicBlock(
        "entry",
        (
            Operation("const", outputs=("a",), attributes={"value": 40}),
            Operation("const", outputs=("b",), attributes={"value": 2}),
            Operation("add", inputs=("a", "b"), outputs=("sum",)),
            Operation("return", inputs=("sum",)),
        ),
    )
    return ModuleIR("answer", {}, (FunctionIR("main", {}, integer, (block,)),))


def test_native_executable_has_elf64_header():
    executable = compile_native_executable(_module(), TargetDescriptor("linux", "x86_64", "sysv", {"native-executable": True}))
    assert executable.format == "elf-x86_64"
    assert executable.payload[:4] == b"\x7fELF"
    assert executable.payload[4] == 2
    assert executable.payload[5] == 1
    assert executable.payload[18:20] == b"\x3e\x00"


def test_native_executable_is_materialized(tmp_path):
    executable = compile_native_executable(_module())
    path = write_native_executable(tmp_path / "answer", executable)
    assert path.read_bytes() == executable.payload
    assert path.stat().st_mode & 0o111


def test_native_executable_runs_and_returns_integer(tmp_path):
    executable = compile_native_executable(_module())
    path = write_native_executable(tmp_path / "answer", executable)
    completed = subprocess.run([str(path)], check=False)
    assert completed.returncode == 42
