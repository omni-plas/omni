import subprocess

from omni.ir import BasicBlock, FunctionIR, ModuleIR, Operation
from omni.native_executable import compile_native_executable, write_native_executable
from omni.source_compiler import compile_source
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


def test_multi_function_native_call_runs(tmp_path):
    result = compile_source(
        "fn add(a, b) { return a + b; } fn main() { return add(40, 2); }",
        origin="call.oi",
    )
    assert result.ok and result.ir is not None
    path = write_native_executable(tmp_path / "call", compile_native_executable(result.ir))
    completed = subprocess.run([str(path)], check=False)
    assert completed.returncode == 42


def test_native_branch_from_oi_source_runs(tmp_path):
    result = compile_source(
        "fn main() { let x = 40; if (x == 40) { return 42; } else { return 1; } }",
        origin="branch.oi",
    )
    assert result.ok and result.ir is not None
    path = write_native_executable(tmp_path / "branch", compile_native_executable(result.ir))
    completed = subprocess.run([str(path)], check=False)
    assert completed.returncode == 42


def test_native_while_loop_from_oi_source_runs(tmp_path):
    result = compile_source(
        "fn main() { let x = 3; while (x > 0) { x = x - 1; } return x; }",
        origin="loop.oi",
    )
    assert result.ok and result.ir is not None
    path = write_native_executable(tmp_path / "loop", compile_native_executable(result.ir))
    completed = subprocess.run([str(path)], check=False)
    assert completed.returncode == 0
