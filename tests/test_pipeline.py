import pytest

from omni.pipeline import compile_semantics
from omni.uir import UIRValidationError


def _base(functions, *, target=None):
    return {
        "version": "0.1",
        "entity": {"kind": "application", "name": "pipeline-demo"},
        "source": {"language": "future-language"},
        "target": target or {"platform": "future-os", "architecture": "future-cpu"},
        "semantics": {
            "program": {"entry": "main"}, "types": {}, "control_flow": {}, "data_flow": {},
            "memory_model": {}, "error_handling": {}, "io": {}, "dependencies": [],
            "security": {}, "performance": {}, "functions": functions,
        },
    }


def test_pipeline_produces_validated_ir():
    result = compile_semantics(_base([{"name": "main", "result": "void", "operations": [{"opcode": "return"}]}]))
    assert result.ok
    assert result.ir.name == "pipeline-demo"
    assert result.ir.functions[0].name == "main"
    assert result.plan.target.identity() == "future-os-future-cpu"


def test_pipeline_surfaces_undefined_ir_values():
    result = compile_semantics(_base([{
        "name": "main", "result": "void", "operations": [{"opcode": "use", "inputs": ["missing"]}],
    }]))
    assert not result.ok
    assert any(d.code == "IR002" and d.severity.value == "error" for d in result.diagnostics)


def test_pipeline_surfaces_semantic_ir_errors():
    result = compile_semantics(_base([{
        "name": "main", "result": "void",
        "operations": [{"opcode": "const", "outputs": ["x"]}, {"opcode": "return", "inputs": ["x"]}],
    }]))
    assert not result.ok
    assert any(d.code == "SEMANTIC_IR" for d in result.diagnostics)


def test_pipeline_preserves_custom_target_capabilities():
    result = compile_semantics(_base([{"name": "main", "result": "void", "operations": [{"opcode": "return"}]}], target={
        "platform": "future-os", "architecture": "future-cpu", "abi": "future-abi",
        "capabilities": {"graphics.v9": True, "memory.tagged": {"mode": "strict"}},
    }))
    assert result.ok
    assert result.plan.target.capability("graphics.v9") is True
    assert result.plan.target.capability("memory.tagged")["mode"] == "strict"


def test_pipeline_rejects_invalid_target_capabilities():
    with pytest.raises(UIRValidationError, match="capabilities"):
        compile_semantics(_base([{"name": "main", "result": "void", "operations": [{"opcode": "return"}]}], target={
            "platform": "future-os", "capabilities": []
        }))
