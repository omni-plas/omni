import pytest

from omni.emitters import EmitterError, emit_c
from omni.ir import BasicBlock, FunctionIR, ModuleIR, Operation
from omni.targets import TargetDescriptor
from omni.types import TypeKind, TypeRef


def _module():
    integer = TypeRef(TypeKind.INTEGER)
    function = FunctionIR(
        name="main",
        parameters={},
        result=integer,
        blocks=(
            BasicBlock(
                name="entry",
                operations=(
                    Operation("const", outputs=("x",), attributes={"value": 40}),
                    Operation("const", outputs=("y",), attributes={"value": 2}),
                    Operation("add", inputs=("x", "y"), outputs=("result",)),
                    Operation("return", inputs=("result",)),
                ),
            ),
        ),
    )
    return ModuleIR("demo", {}, (function,))


def test_c_emitter_produces_real_translation_unit():
    payload = emit_c(_module(), TargetDescriptor("portable-c"))
    source = payload.decode("utf-8")
    assert "int64_t main(void)" in source
    assert "return result;" in source
    assert "printf" in source


def test_c_emitter_rejects_unrepresentable_operation():
    module = ModuleIR(
        "bad",
        {},
        (FunctionIR("main", {}, TypeRef(TypeKind.INTEGER), (BasicBlock("entry", (Operation("unknown"),)),)),),
    )
    with pytest.raises(EmitterError, match="unsupported C operation"):
        emit_c(module)
