from omni.self_build_validation import SelfBuildResult, validate_self_build


def test_valid_self_host_result():
    result=validate_self_build(SelfBuildResult(True,True,True))
    assert result.self_hosted
