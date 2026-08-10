import pytest

from omni.construct import plan_construction
from omni.digital import DigitalSpec


def test_digital_spec_is_open_world():
    spec = DigitalSpec(
        kind="future-digital-artifact",
        name="new-thing",
        behavior={"unknown_future_behavior": {"enabled": True}},
        interfaces=("future-interface",),
    )
    plan = plan_construction(spec)
    assert plan.steps == ("validate", "model", "lower", "materialize", "verify")
    assert plan.artifact.kind == "future-digital-artifact"


def test_digital_spec_rejects_empty_identity():
    with pytest.raises(ValueError):
        plan_construction({"kind": "", "name": "x"})
