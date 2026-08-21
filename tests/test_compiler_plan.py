import pytest

from omni.compiler import CompilationError, plan_compilation


def base_document():
    return {
        "version": "0.1",
        "entity": {"kind": "application", "name": "compiler-plan"},
        "source": {"language": "future-language"},
        "target": {
            "platform": "future-os",
            "architecture": "future-cpu",
            "abi": "future-abi",
            "capabilities": {"graphics": {"api": "future-gfx", "version": 2}},
        },
        "semantics": {
            "program": {}, "types": {}, "control_flow": {}, "data_flow": {},
            "memory_model": {}, "error_handling": {}, "io": {}, "dependencies": [],
            "security": {}, "performance": {}, "functions": [],
        },
    }


def test_plan_preserves_open_world_target_and_source():
    plan = plan_compilation(base_document())
    assert plan.source_language == "future-language"
    assert plan.target_identity() == "future-os-future-cpu-future-abi"
    assert plan.target.capability("graphics")["api"] == "future-gfx"
    assert plan.requires("program")


def test_plan_rejects_missing_semantic_contract():
    document = base_document()
    del document["semantics"]["security"]
    with pytest.raises(CompilationError, match="security"):
        plan_compilation(document)


def test_plan_rejects_invalid_capability_container():
    document = base_document()
    document["target"]["capabilities"] = "invalid"
    with pytest.raises(ValueError, match="capabilities"):
        plan_compilation(document)


def test_plan_requirement_query_rejects_blank_name():
    plan = plan_compilation(base_document())
    with pytest.raises(ValueError, match="non-empty"):
        plan.requires(" ")
