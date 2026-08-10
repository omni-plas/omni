import pytest

from omni.ir import BasicBlock, FunctionIR, ModuleIR, Operation
from omni.types import TypeKind, TypeRef
from omni.validation import SemanticValidationError, validate_module


def _module(operations):
    integer = TypeRef(TypeKind.INTEGER)
    return ModuleIR(
        name="test",
        types={},
        functions=(
            FunctionIR(
                name="main",
                parameters={"x": integer},
                result=integer,
                blocks=(BasicBlock(name="entry", operations=tuple(operations)),),
            ),
        ),
    )


def test_validation_rejects_undefined_data_flow_value():
    with pytest.raises(SemanticValidationError, match="undefined value"):
        validate_module(_module([Operation("return", inputs=("missing",))]))


def test_validation_rejects_unknown_opcode():
    with pytest.raises(SemanticValidationError, match="unsupported reference opcode"):
        validate_module(_module([Operation("future_opcode"), Operation("return")]))


def test_validation_requires_const_value():
    with pytest.raises(SemanticValidationError, match="const requires a value"):
        validate_module(_module([Operation("const", outputs=("x",)), Operation("return", inputs=("x",))]))
