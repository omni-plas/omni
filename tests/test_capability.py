from omni.capability import CapabilityRequirement, evaluate_capabilities


def test_capability_report_is_complete_when_all_requirements_are_available():
    report = evaluate_capabilities(
        [CapabilityRequirement("frontend.python"), CapabilityRequirement("target.linux")],
        ["frontend.python", "target.linux"],
    )
    assert report.complete
    assert len(report.satisfied) == 2
    assert not report.gaps


def test_capability_report_exposes_missing_future_capability():
    report = evaluate_capabilities(
        [CapabilityRequirement("frontend.future-language")],
        [],
    )
    assert not report.complete
    assert report.gaps[0].requirement.name == "frontend.future-language"
