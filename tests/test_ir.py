import pytest

from omni.ir import BasicBlock, FunctionIR, ModuleIR, Operation, Value
from omni.lower import lower_to_ir
from omni.types import TypeKind, TypeRef


def test_module_ir_rejects_unknown_successor():
    function = FunctionIR("main", {}, TypeRef(TypeKind.VOID), (BasicBlock("entry", successors=("missing",)),))
    with pytest.raises(ValueError, match="unknown successor"):
        ModuleIR("demo", {}, (function,)).validate()


def test_module_ir_rejects_empty_function_name():
    function = FunctionIR("", {}, TypeRef(TypeKind.VOID), (BasicBlock("entry"),))
    with pytest.raises(ValueError, match="function name"):
        ModuleIR("demo", {}, (function,)).validate()


def test_module_ir_rejects_duplicate_blocks():
    function = FunctionIR("main", {}, TypeRef(TypeKind.VOID), (BasicBlock("entry"), BasicBlock("entry")))
    with pytest.raises(ValueError, match="duplicate block"):
        ModuleIR("demo", {}, (function,)).validate()


def test_module_ir_rejects_duplicate_successors():
    function = FunctionIR("main", {}, TypeRef(TypeKind.VOID), (BasicBlock("entry", successors=("exit", "exit")), BasicBlock("exit")))
    with pytest.raises(ValueError, match="duplicate successor"):
        ModuleIR("demo", {}, (function,)).validate()


def test_module_ir_rejects_duplicate_operation_outputs():
    function = FunctionIR("main", {}, TypeRef(TypeKind.VOID), (BasicBlock("entry", (Operation("x", outputs=("a", "a")),)),))
    with pytest.raises(ValueError, match="duplicate operation output"):
        ModuleIR("demo", {}, (function,)).validate()


def test_module_ir_validates_global_types():
    function = FunctionIR("main", {}, TypeRef(TypeKind.VOID), (BasicBlock("entry", (Operation("return"),)),))
    module = ModuleIR("demo", {}, (function,), globals={"answer": Value(TypeRef(TypeKind.INTEGER), 42)})
    module.validate()


def test_lowering_creates_real_operation_ir():
    document = {"version": "0.1", "entity": {"kind": "application", "name": "demo"}, "source": {"language": "future-language"}, "target": {"platform": "future-os"}, "semantics": {"program": {"entry": "main"}, "types": {}, "control_flow": {}, "data_flow": {}, "memory_model": {}, "error_handling": {}, "io": {}, "dependencies": [], "security": {}, "performance": {}, "functions": [{"name": "main", "result": "void", "operations": [{"opcode": "return"}]}]}}
    module = lower_to_ir(document)
    assert module.name == "demo"
    assert module.functions[0].blocks[0].operations == (Operation(opcode="return"),)
