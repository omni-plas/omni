import json

from omni.cli import main


def _document():
    return {
        "version": "0.1",
        "entity": {"kind": "application", "name": "cli-test"},
        "source": {"language": "omni"},
        "target": {"platform": "reference-runtime"},
        "semantics": {
            "program": {"entry": "main"},
            "types": {}, "functions": [{
                "name": "main", "parameters": {"x": "integer"}, "result": "integer",
                "operations": [
                    {"opcode": "const", "outputs": ["one"], "attributes": {"value": 1}},
                    {"opcode": "add", "inputs": ["x", "one"], "outputs": ["result"]},
                    {"opcode": "return", "inputs": ["result"]},
                ],
            }],
            "control_flow": {}, "data_flow": {}, "memory_model": {}, "error_handling": {},
            "io": {}, "dependencies": [], "security": {}, "performance": {},
        },
    }


def test_cli_runs_uir_file(tmp_path, capsys):
    path = tmp_path / "program.json"
    path.write_text(json.dumps(_document()), encoding="utf-8")
    assert main(["run", str(path), "--args", '{"x": 41}']) == 0
    assert capsys.readouterr().out.strip() == "42"


def test_cli_reports_invalid_program(tmp_path, capsys):
    path = tmp_path / "invalid.json"
    path.write_text("{}", encoding="utf-8")
    assert main(["run", str(path)]) == 2
    assert "omni: error:" in capsys.readouterr().err
