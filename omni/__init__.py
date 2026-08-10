"""Omni universal digital creation and compilation engine."""

from .entities import EntitySpec
from .ir import BasicBlock, FunctionIR, ModuleIR, Operation, Value
from .lower import lower_to_ir
from .materialize import MaterializedArtifact, Materializer, validate_materialized_artifact
from .pipeline import CompilationResult, compile_semantics
from .runtime import RuntimeErrorBase, execute, execute_module
from .semantics import SemanticModel
from .targets import TargetDescriptor
from .types import TypeKind, TypeRef
from .uir import UIR, UIRValidationError, validate_uir
from .validation import SemanticValidationError, validate_function, validate_module

__all__ = [
    "BasicBlock", "CompilationResult", "EntitySpec", "FunctionIR", "MaterializedArtifact",
    "Materializer", "ModuleIR", "Operation", "RuntimeErrorBase", "SemanticModel",
    "SemanticValidationError", "TargetDescriptor", "TypeKind", "TypeRef", "UIR",
    "UIRValidationError", "Value", "compile_semantics", "execute", "execute_module",
    "lower_to_ir", "validate_function", "validate_materialized_artifact", "validate_module",
    "validate_uir",
]
