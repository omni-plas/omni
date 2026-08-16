from omni.diagnostics import Diagnostic, Severity
from omni.validation_report import report


def test_validation_report_classifies_diagnostics():
    result = report([
        Diagnostic("E1", Severity.ERROR, "bad type", "main:x"),
        Diagnostic("W1", Severity.WARNING, "unused value"),
    ])
    assert not result.valid
    assert len(result.errors) == 1
    assert len(result.warnings) == 1
    payload = result.to_dict()
    assert payload["valid"] is False
    assert payload["errors"][0]["code"] == "E1"
