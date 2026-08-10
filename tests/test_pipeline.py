from omni.pipeline import compile_semantics


def test_pipeline_produces_validated_ir():
    document = {
        "version": "0.1",
        "entity": {"kind": "application", "name": "pipeline-demo"},
        "source": {"language": "future-language"},
        "target": {"platform": "future-os", "architecture": "future-cpu"},
        "semantics": {
            "program": {"entry": "main"},
            "types": {},
            "control_flow": {},
            "data_flow": {},
            "memory_model": {},
            "error_handling": {},
            "io": {},
            "dependencies": [],
            "security": {},
            "performance": {},
            "functions": [{"name": "main", "result": "void", "operations": [{"opcode": "return"}]}],
        },
    }
    result = compile_semantics(document)
    assert result.ok
    assert result.ir.name == "pipeline-demo"
    assert result.ir.functions[0].name == "main"
    assert result.plan.target.identity() == "future-os-future-cpu"
