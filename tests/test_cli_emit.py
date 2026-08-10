import json

from omni.cli import main


def test_cli_emits_c99(tmp_path):
    document = {
        "version": "0.1",
        "entity": {"kind": "application", "name": "emit-test"},
        "source": {"language": "omni"},
        "target": {"platform": "portable-c"},
        "semantics": {
            "program": {"entry": "main"},
            "types": {},
            "functions": [{
                "name": "main",
                "parameters": {},
                "result": "integer",
                "operations": [
                    {"opcode": "const", "outputs": ["answer"], "attributes": {"value": 42}},
                    {"opcode": "return", "inputs": ["answer"]},
                ],
            }],
            "control_flow": {},
            "data_flow": {},
            "memory_model": {},
            "error_handling": {},
            "io": {},
            "dependencies": [],
            "security": {},
            "performance": {},
        },
    }
    source = tmp_path / "program.json"
    output = tmp_path / "program.c"
    source.write_text(json.dumps(document), encoding="utf-8")

    assert main(["emit-c", str(source), str(output)]) == 0
    generated = output.read_text(encoding="utf-8")
    assert "return answer;" in generated
