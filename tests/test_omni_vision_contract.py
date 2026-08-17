from omni.digital import DigitalSpec
from omni.entities import EntitySpec


def test_open_world_digital_entity_can_be_described_without_fixed_catalog():
    entity = EntitySpec(
        name="future-digital-entity",
        kind="future.entity.kind",
        properties={"purpose": "user-defined", "version": 1},
    )
    assert entity.kind == "future.entity.kind"
    assert entity.properties["purpose"] == "user-defined"


def test_digital_spec_preserves_open_world_kind():
    spec = DigitalSpec(
        name="future-platform",
        kind="future.platform",
        requirements={"execution_model": "future-runtime"},
    )
    assert spec.kind == "future.platform"
    assert spec.requirements["execution_model"] == "future-runtime"
