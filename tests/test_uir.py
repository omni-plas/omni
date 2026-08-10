import pytest

from omni.compiler import CompilationError, plan_compilation
from omni.uir import UIRValidationError, validate_uir


VALID = {
    "version": "0.1",
    "entity": {"kind": "application", "name": "hello"},
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
    },
}


def test_uir_accepts_unknown_language_and_target():
    uir = validate_uir(VALID)
    assert uir.source["language"] == "future-language"
    assert uir.target["platform"] == "future-os"


def test_uir_rejects_missing_semantics():
    document = {**VALID, "semantics": {"types": {}}}
    with pytest.raises(UIRValidationError, match="program or behavior"):
        validate_uir(document)


def test_compilation_plan_requires_complete_semantics():
    document = {**VALID, "semantics": {"program": {}}}
    with pytest.raises(CompilationError, match="semantic model is incomplete"):
        plan_compilation(document)


def test_compilation_plan_models_semantic_requirements():
    plan = plan_compilation(VALID)
    assert plan.source_language == "future-language"
    assert plan.target.platform == "future-os"
    assert plan.target.architecture == "future-cpu"
    assert "memory_model" in plan.semantic_requirements
