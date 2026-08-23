import json

from omni.cli import main
from omni.serialization import dumps_uir


def test_native_exec_cli_writes_elf(tmp_path):
    source = {
        "version": "1",
        "entity": {"kind": "application", "name": "cli-smoke"},
        "semantics": {
            "program": {"entry": "main"},
            "functions": {
                "main": {
                    "parameters": [],
                    "result": {"kind": "int", "bits": 64},
                    "blocks": [{
                        "name": "entry",
                        "operations": [
                            {"opcode": "const", "outputs": ["value"], "attributes": {"value": 7}},
                            {"opcode": "return", "inputs": ["value"]},
                        ],
                        "successors": [],
                    }],
                }
            },
        },
    }
    source_path = tmp_path / "program.json"
    output_path = tmp_path / "program"
    source_path.write_text(dumps_uir(source), encoding="utf-8")
    assert main(["native-exec", str(source_path), "-o", str(output_path)]) == 0
    assert output_path.read_bytes()[:4] == b"\x7fELF"
