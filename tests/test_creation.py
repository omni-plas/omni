from omni.creation import plan_creation
from omni.digital import DigitalSpec


def test_creation_planner_supports_unknown_entity_kinds():
    spec = DigitalSpec(
        kind="future.digital-tool-builder",
        name="next-generator",
        behavior={"builds": "future-entities"},
        interfaces=("generate",),
        data={"schema": "future"},
        requirements={"target": "future-os"},
    )
    plan = plan_creation(spec)
    assert plan.executable
    assert plan.steps[0].action == "define-entity"
    assert plan.steps[-1].action == "materialize"
    assert any(step.action == "define-behavior" for step in plan.steps)
