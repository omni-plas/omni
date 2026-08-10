"""Omni universal digital creation and compilation engine."""

from .artifacts import ArtifactManifest, manifest
from .construct import ConstructionPlan, plan_construction
from .digital import DigitalSpec
from .emitters import EmitterError, emit_c
from .entities import EntitySpec
from .entity_validate import entity_from_mapping
from .ir import BasicBlock, FunctionIR, ModuleIR, Operation, Value
from .lower import lower_to_ir
from .materialize import MaterializedArtifact, Materializer, validate_materialized_artifact
from .pipeline import CompilationResult, compile_semantics
from .runtime import RuntimeErrorBase, execute, execute_module
from .semantics import SemanticModel
from .targets import TargetDescriptor
from .typecheck import TypeDiagnostic, check_module, is_valid
from .types import TypeKind, TypeRef
from .uir import UIR, UIRValidationError, validate_uir
from .validation import SemanticValidationError, validate_function, validate_module

__all__ = [
    "ArtifactManifest", "BasicBlock", "CompilationResult", "ConstructionPlan", "DigitalSpec",
    "EmitterError", "EntitySpec", "FunctionIR", "MaterializedArtifact", "Materializer", "ModuleIR",
    "Operation", "RuntimeErrorBase", "SemanticModel", "SemanticValidationError", "TargetDescriptor",
    "TypeDiagnostic", "TypeKind", "TypeRef", "UIR", "UIRValidationError", "Value", "check_module",
    "compile_semantics", "emit_c", "entity_from_mapping", "execute", "execute_module", "is_valid",
    "lower_to_ir", "manifest", "plan_construction", "validate_materialized_artifact", "validate_function",
    "validate_module", "validate_uir",
]
