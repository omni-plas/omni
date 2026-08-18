from omni.entity_factory import DigitalBlueprint, digital_spec_from_blueprint, entity_from_blueprint


def test_factory_accepts_entity_kind_that_did_not_exist_in_catalog():
    blueprint = DigitalBlueprint(
        kind="future.website-builder",
        name="next-web-platform",
        structure={"pages": "dynamic"},
        behavior={"generates": "websites"},
        interfaces=("publish",),
    )
    spec = digital_spec_from_blueprint(blueprint)
    entity = entity_from_blueprint(blueprint)
    assert spec.kind == "future.website-builder"
    assert entity.kind == "future.website-builder"
    assert entity.inputs == ("publish",)
