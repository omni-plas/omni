"""Omni universal digital creation and compilation engine."""

from .ir import BasicBlock, FunctionIR, ModuleIR, Operation, Value
from .lower import lower_to_ir
from .pipeline import CompilationResult, compile_semantics
from .runtime import RuntimeErrorBase, execute, execute_module
from .semantics import SemanticModel
from .targets import TargetDescriptor
from .types import TypeKind, TypeRef
from .uir import UIR, UIRValidationError, validate_uir

__all__ = [
    "BasicBlock",
    "CompilationResult",
    "FunctionIR",
    "ModuleIR",
    "Operation",
    "RuntimeErrorBase",
    "SemanticModel",
    "TargetDescriptor",
    "TypeKind",
    "TypeRef",
    "UIR",
    "UIRValidationError",
    "Value",
    "compile_semantics",
    "execute",
    "execute_module",
    "lower_to_ir",
    "validate_uir",
]
