"""Omni universal digital creation and compilation engine."""

from .ir import BasicBlock, FunctionIR, ModuleIR, Operation, Value
from .lower import lower_to_ir
from .semantics import SemanticModel
from .targets import TargetDescriptor
from .types import TypeKind, TypeRef
from .uir import UIR, UIRValidationError, validate_uir

__all__ = [
    "BasicBlock",
    "FunctionIR",
    "ModuleIR",
    "Operation",
    "SemanticModel",
    "TargetDescriptor",
    "TypeKind",
    "TypeRef",
    "UIR",
    "UIRValidationError",
    "Value",
    "lower_to_ir",
    "validate_uir",
]
