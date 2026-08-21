import pytest

from omni.ir import BasicBlock, FunctionIR, ModuleIR, Operation
from omni.types import TypeKind, TypeRef
from omni.validation import SemanticValidationError, validate_function, validate_module


def _module(operations, successors=()):
    integer = TypeRef(TypeKind.INTEGER)
    return ModuleIR("test", {}, (FunctionIR("main", {"x": integer}, integer, (BasicBlock("entry", tuple(operations), successors),)),))


def test_validation_rejects_undefined_data_flow_value():
    with pytest.raises(SemanticValidationError, match="undefined value"):
        validate_module(_module([Operation("return", inputs=("missing",))]))


def test_validation_rejects_unknown_opcode():
    with pytest.raises(SemanticValidationError, match="unsupported reference opcode"):
        validate_module(_module([Operation("future_opcode"), Operation("return")]))


def test_validation_requires_const_value():
    with pytest.raises(SemanticValidationError, match="const requires one output"):
        validate_module(_module([Operation("const", outputs=("x",)), Operation("return", inputs=("x",))]))


def test_validation_requires_branch_targets_to_match_cfg():
    operations = [Operation("branch", inputs=("x",), attributes={"true": "yes", "false": "no"})]
    with pytest.raises(SemanticValidationError, match="successors must match"):
        validate_module(_module(operations, successors=("wrong", "no")))


def test_validation_rejects_operation_after_terminator():
    fn = FunctionIR("main", {}, TypeRef(TypeKind.VOID), (BasicBlock("entry", (
        Operation("return"), Operation("const", outputs=("x",), attributes={"value": 1}),
    )),))
    with pytest.raises(SemanticValidationError, match="after a terminator"):
        validate_function(fn)


def test_validation_accepts_multiple_functions():
    integer = TypeRef(TypeKind.INTEGER)
    module = ModuleIR("multi", {}, (
        FunctionIR("a", {}, integer, (BasicBlock("entry", (Operation("const", outputs=("x",), attributes={"value": 1}), Operation("return", inputs=("x",)))),)),
        FunctionIR("b", {}, integer, (BasicBlock("entry", (Operation("const", outputs=("y",), attributes={"value": 2}), Operation("return", inputs=("y",)))),)),
    ))
    validate_module(module)
