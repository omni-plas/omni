from omni.self_host_manifest import SELF_HOST_UNITS, validate_manifest


def test_self_host_manifest_is_complete():
    validate_manifest(SELF_HOST_UNITS)
    assert {u.role for u in SELF_HOST_UNITS} >= {"frontend", "semantic", "ir", "optimizer", "backend", "runtime", "stdlib", "driver"}
