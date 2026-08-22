import json

from omni.cli import main


def _document():
    return {"version": "0.1", "entity": {"kind": "application", "name": "cli-test"}, "source": {"language": "omni"}, "target": {"platform": "reference-runtime"}, "semantics": {"program": {"entry": "main"}, "types": {}, "functions": [{"name": "main", "parameters": {"x": "integer"}, "result": "integer", "operations": [{"opcode": "const", "outputs": ["one"], "attributes": {"value": 1}}, {"opcode": "add", "inputs": ["x", "one"], "outputs": ["result"]}, {"opcode": "return", "inputs": ["result"]}]}], "control_flow": {}, "data_flow": {}, "memory_model": {}, "error_handling": {}, "io": {}, "dependencies": [], "security": {}, "performance": {}}}


def test_cli_runs_uir_file(tmp_path, capsys):
    path = tmp_path / "program.json"
    path.write_text(json.dumps(_document()), encoding="utf-8")
    assert main(["run", str(path), "--args", '{"x": 41}']) == 0
    assert capsys.readouterr().out.strip() == "42"


def test_cli_validates_without_execution(tmp_path, capsys):
    path = tmp_path / "program.json"
    path.write_text(json.dumps(_document()), encoding="utf-8")
    assert main(["validate", str(path)]) == 0
    assert capsys.readouterr().out.strip() == "valid"


def test_cli_reports_invalid_program(tmp_path, capsys):
    path = tmp_path / "invalid.json"
    path.write_text("{}", encoding="utf-8")
    assert main(["validate", str(path)]) == 2
    assert "omni: error:" in capsys.readouterr().err


def test_cli_rejects_non_object_args(tmp_path, capsys):
    path = tmp_path / "program.json"
    path.write_text(json.dumps(_document()), encoding="utf-8")
    assert main(["run", str(path), "--args", "[]"]) == 2
    assert "--args must be a JSON object" in capsys.readouterr().err


def test_cli_emits_c_source(tmp_path):
    path = tmp_path / "program.json"
    output = tmp_path / "program.c"
    path.write_text(json.dumps(_document()), encoding="utf-8")
    assert main(["emit-c", str(path), str(output)]) == 0
    source = output.read_text(encoding="utf-8")
    assert "int64_t main" in source
    assert "return result;" in source


def test_cli_creates_installation_plan(capsys):
    assert main([
        "install-plan",
        "--target", "future-os",
        "--architecture", "future-cpu",
        "--abi", "future-abi",
        "--kind", "bootable",
        "--format", "future-image",
        "--bootable",
        "--filesystem", "future-fs",
    ]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["identity"] == "bootable:future-os-future-cpu-future-abi:future-image"
    assert payload["filesystem"] == "future-fs"


def test_cli_installation_plan_keeps_future_target_open_world(capsys):
    assert main(["install-plan", "--target", "historical-os", "--format", "legacy-package"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["target"] == "historical-os"
    assert payload["kind"] == "package"


def test_cli_can_render_canonical_installation_manifest(capsys):
    assert main([
        "install-plan", "--target", "future-os", "--architecture", "future-cpu",
        "--kind", "bootable", "--format", "future-image", "--bootable", "--filesystem", "future-fs",
        "--manifest",
    ]) == 0
    document = json.loads(capsys.readouterr().out)
    assert document["schema"] == "omni.installation.v1"
    assert document["target"]["platform"] == "future-os"
    assert document["target"]["architecture"] == "future-cpu"
    assert document["bootable"] is True
