import pytest

from omni.compiler import CompilationError, plan_compilation
from omni.uir import UIRValidationError, validate_uir


VALID = {
    "version": "0.1",
    "entity": {
        "kind": "application",
        "name": "hello",
        "structure": {"components": []},
        "behavior": {"entry": "main"},
        "inputs": [],
        "outputs": [],
        "execution_model": {"mode": "native"},
    },
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
    assert uir.entity_kind == "application"
    assert uir.entity_name == "hello"


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


def test_entity_name_is_optional_but_validated_when_present():
    document = {**VALID, "entity": {"kind": "unnamed-entity"}}
    assert validate_uir(document).entity_name is None
    document["entity"] = {"kind": "x", "name": " "}
    with pytest.raises(UIRValidationError, match="entity.name"):
        validate_uir(document)


def test_entity_structure_and_execution_model_are_formalized():
    uir = validate_uir(VALID)
    assert uir.entity["structure"]["components"] == []
    assert uir.entity["execution_model"]["mode"] == "native"


def test_entity_extension_fields_remain_open_world():
    document = {**VALID, "entity": {**VALID["entity"], "future_property": {"x": 1}}}
    assert validate_uir(document).entity["future_property"]["x"] == 1


def test_entity_structural_fields_reject_scalars():
    document = {**VALID, "entity": {**VALID["entity"], "structure": 42}}
    with pytest.raises(UIRValidationError, match="entity.structure"):
        validate_uir(document)


def test_entity_inputs_and_outputs_accept_arrays():
    uir = validate_uir(VALID)
    assert uir.entity["inputs"] == []
    assert uir.entity["outputs"] == []
