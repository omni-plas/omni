import json

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


def test_materialization_manifest_is_target_bound_and_deterministic():
    target = TargetDescriptor("future-os", "future-cpu", "future-abi", {"boot": "next"})
    plan = create_materialization_plan(target, metadata={"channel": "future"})
    plan = plan.add(Artifact("kernel", "kernel", target, "bin"))
    plan = plan.add(Artifact("rootfs", "rootfs", target, "img"))
    document = json.loads(plan.manifest())
    assert document["schema"] == "omni.materialization.v1"
    assert document["target"] == target.identity()
    assert document["target_descriptor"]["schema"] == "omni.target.v1"
    assert len(document["artifacts"]) == 2
    assert plan.manifest() == plan.manifest()


def test_materialization_manifest_contains_content_identity():
    target = TargetDescriptor("os")
    plan = create_materialization_plan(target).add(Artifact("kernel", "kernel", target, "bin"))
    entry = json.loads(plan.manifest())["artifacts"][0]
    assert entry["identity"] == plan.artifacts[0].identity()
    assert len(entry["digest"]) == 64
