from omni.pipeline import compile_semantics
from omni.runtime import execute_module


def test_uir_to_execution_vertical_slice():
    document = {
        "version": "0.1",
        "entity": {"kind": "application", "name": "adder"},
        "source": {"language": "omni"},
        "target": {"platform": "reference-runtime"},
        "semantics": {
            "program": {"entry": "main"},
            "types": {},
            "functions": [
                {
                    "name": "main",
                    "parameters": {"left": "integer", "right": "integer"},
                    "result": "integer",
                    "operations": [
                        {"opcode": "add", "inputs": ["left", "right"], "outputs": ["sum"]},
                        {"opcode": "return", "inputs": ["sum"]},
                    ],
                }
            ],
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

    result = compile_semantics(document)
    assert result.ok
    assert result.plan.source_language == "omni"
    assert execute_module(result.ir, "main", {"left": 20, "right": 22}) == 42
