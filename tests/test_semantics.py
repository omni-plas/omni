from omni.semantics import SemanticModel


def test_semantic_model_covers_required_conversion_dimensions():
    model = SemanticModel(
        ownership={"mode": "borrowed"},
        lifetime={"policy": "scoped"},
        concurrency={"model": "actor"},
        execution_model={"kind": "native"},
        platform_constraints={"sandbox": True},
    )
    data = model.as_dict()
    assert data["ownership"]["mode"] == "borrowed"
    assert data["concurrency"]["model"] == "actor"
    assert data["execution_model"]["kind"] == "native"
    assert data["platform_constraints"]["sandbox"] is True
