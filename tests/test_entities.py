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
    with pytest.raises(ValueError, match="ports"):
        entity.validate()


def test_materialized_artifact_is_validated():
    entity = EntitySpec(kind="thing", name="x")
    artifact = MaterializedArtifact(entity, "opaque", b"data")
    validate_materialized_artifact(artifact)
