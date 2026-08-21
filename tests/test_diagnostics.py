import pytest

from omni.diagnostics import Diagnostic, Severity, format_diagnostics


def test_diagnostic_formats_source_location():
    diagnostic = Diagnostic("E100", Severity.ERROR, "bad token", path="main.omni", line=4, column=7)
    assert diagnostic.format() == "main.omni:4:7: error E100: bad token"


def test_diagnostic_serializes_location_fields():
    data = Diagnostic("W1", Severity.WARNING, "future target", source="stdin").to_dict()
    assert data["source"] == "stdin"
    assert data["line"] is None


def test_diagnostics_are_rendered_in_order():
    values = [Diagnostic("E1", Severity.ERROR, "first"), Diagnostic("E2", Severity.ERROR, "second")]
    assert format_diagnostics(values).splitlines() == ["<unknown>: error E1: first", "<unknown>: error E2: second"]


def test_invalid_diagnostic_rejected():
    with pytest.raises(ValueError, match="code"):
        Diagnostic("", Severity.ERROR, "message")
