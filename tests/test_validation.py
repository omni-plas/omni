import pytest

from omni.ir import BasicBlock, FunctionIR, ModuleIR, Operation
from omni.types import TypeKind, TypeRef
from omni.validation import SemanticValidationError, validate_module


def _module(operations, successors=()):
    integer = TypeRef(TypeKind.INTEGER)
    return ModuleIR(
        name="test",
        types={},
        functions=(FunctionIR(
            name="main", parameters={"x": integer}, result=integer,
            blocks=(BasicBlock(name="entry", operations=tuple(operations), successors=successors),),
        ),),
    )


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
    operations = [
        Operation("branch", inputs=("x",), attributes={"true": "yes", "false": "no"}),
    ]
    with pytest.raises(SemanticValidationError, match="successors must match"):
        validate_module(_module(operations, successors=("wrong", "no")))
