import pytest

from omni.self_build import (
    SelfBuildError,
    SelfBuildResult,
    SelfBuildSpec,
    SelfBuildStage,
    plan_self_build,
    source_digest,
    validate_self_build_result,
)


def test_source_digest_is_deterministic():
    assert source_digest(b"omni") == source_digest(b"omni")
    assert source_digest(b"omni") != source_digest(b"different")


def test_self_build_plan_records_source_and_target():
    spec = plan_self_build(b"omni source", "linux-x86_64")
    assert spec.source_digest == source_digest(b"omni source")
    assert spec.target == "linux-x86_64"


def test_incomplete_result_is_rejected():
    result = SelfBuildResult(
        SelfBuildSpec("0" * 64, "test"),
        "0" * 64,
        (SelfBuildStage.SOURCE,),
        self_hosted=False,
    )
    with pytest.raises(SelfBuildError):
        validate_self_build_result(result)
