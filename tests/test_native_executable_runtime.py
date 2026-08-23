import os
import subprocess

from omni.ir import BasicBlock, FunctionIR, ModuleIR, Operation
from omni.native_executable import compile_native_executable, write_native_executable
from omni.types import TypeKind, TypeRef


def test_generated_elf_runs_without_external_toolchain(tmp_path):
    i64 = TypeRef(TypeKind.INT, bits=64)
    module = ModuleIR(
        "runtime_smoke",
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
    executable = compile_native_executable(module)
    path = write_native_executable(tmp_path / "runtime_smoke", executable)
    if os.name != "posix":
        return
    completed = subprocess.run([str(path)], check=False, capture_output=True, timeout=5)
    assert completed.returncode == 42
    assert completed.stdout == b""
