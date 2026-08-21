import pytest

from omni.entities import EntitySpec
from omni.materialize import MaterializedArtifact, validate_materialized_artifact


def test_unknown_entity_kind_is_validatable():
    entity = EntitySpec(
        kind="future-digital-entity",
        name="prototype",
        structure={"nodes": 3},
        behavior={"entry": "start"},
        inputs=({"name": "input", "type": "bytes"},),
        outputs=({"name": "output", "type": "artifact"},),
    )
    entity.validate()
    assert entity.to_dict()["kind"] == "future-digital-entity"


def test_entity_rejects_unnamed_port():
    entity = EntitySpec(kind="thing", name="x", inputs=({"type": "bytes"},))
    with pytest.raises(ValueError, match="non-empty name"):
        entity.validate()


def test_entity_rejects_wrong_kind_and_name_types():
    with pytest.raises(ValueError, match="kind"):
        EntitySpec(kind=None, name="x").validate()
    with pytest.raises(ValueError, match="name"):
        EntitySpec(kind="thing", name=None).validate()


def test_entity_rejects_scalar_structure_and_execution():
    with pytest.raises(ValueError, match="structure"):
        EntitySpec(kind="thing", name="x", structure=1).validate()
    with pytest.raises(ValueError, match="execution"):
        EntitySpec(kind="thing", name="x", execution=1).validate()


def test_entity_rejects_non_mapping_ports():
    with pytest.raises(ValueError, match="inputs"):
        EntitySpec(kind="thing", name="x", inputs=("bad",)).validate()
    with pytest.raises(ValueError, match="outputs"):
        EntitySpec(kind="thing", name="x", outputs=(1,)).validate()


def test_materialized_artifact_is_validated():
    entity = EntitySpec(kind="thing", name="x")
    artifact = MaterializedArtifact(entity, "opaque", b"data")
    validate_materialized_artifact(artifact)
