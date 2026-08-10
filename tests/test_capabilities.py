from omni.capabilities import match


def test_capability_matching_reports_future_target_gaps():
    report = match({"graphics": "ray-v2", "compute": "*"}, {"compute": "gpu"})
    assert report.satisfied == ("compute",)
    assert len(report.missing) == 1
    assert report.missing[0].capability == "graphics"
    assert not report.is_satisfied
