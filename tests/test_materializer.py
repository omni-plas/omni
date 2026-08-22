import pytest

from omni.artifacts import Artifact
from omni.materializer import MaterializationError, create_materialization_plan
from omni.targets import TargetDescriptor


def test_materialization_accepts_same_target_artifacts():
    target = TargetDescriptor("future-os", "future-cpu")
    plan = create_materialization_plan(target, metadata={"era": "future"})
    plan = plan.add(Artifact("kernel", "kernel", target, "bin"))
    plan = plan.add(Artifact("system-image", "os-image", target, "img"))
    assert len(plan.artifacts) == 2
    assert plan.identities()[0].startswith("kernel:kernel:")


def test_materialization_rejects_cross_target_artifacts():
    target = TargetDescriptor("future-os")
    other = TargetDescriptor("historical-os")
    plan = create_materialization_plan(target)
    with pytest.raises(MaterializationError, match="target"):
        plan.add(Artifact("old", "image", other, "img"))


def test_materialization_rejects_invalid_artifact_values():
    with pytest.raises(TypeError, match="Artifact"):
        create_materialization_plan(TargetDescriptor("os")).add("image")
