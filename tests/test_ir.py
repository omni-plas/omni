import pytest

from omni.ir import BasicBlock, FunctionIR, ModuleIR, Operation
from omni.lower import lower_to_ir
from omni.types import TypeKind, TypeRef


def test_module_ir_rejects_unknown_successor():
    function = FunctionIR(
        name="main",
        parameters={},
        result=TypeRef(TypeKind.VOID),
        blocks=(BasicBlock("entry", successors=("missing",)),),
    )
    with pytest.raises(ValueError, match="unknown successor"):
        ModuleIR("demo", {}, (function,)).validate()


def test_lowering_creates_real_operation_ir():
    document = {
        "version": "0.1",
        "entity": {"kind": "application", "name": "demo"},
        "source": {"language": "future-language"},
        "target": {"platform": "future-os"},
        "semantics": {
            "program": {"entry": "main"},
            "types": {},
            "control_flow": {},
            "data_flow": {},
            "memory_model": {},
            "error_handling": {},
            "io": {},
            "dependencies": [],
            "security": {},
            "performance": {},
            "functions": [{
                "name": "main",
                "result": "void",
                "operations": [{"opcode": "return"}],
            }],
        },
    }
    module = lower_to_ir(document)
    assert module.name == "demo"
    assert module.functions[0].blocks[0].operations == (Operation(opcode="return"),)
