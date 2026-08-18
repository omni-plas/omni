"""Omni universal digital creation and compilation engine."""

from .artifacts import ArtifactManifest, manifest
from .capabilities import CapabilityGap, CapabilityReport, match
from .capability import CapabilityRequirement, evaluate_capabilities
from .construct import ConstructionPlan, plan_construction
from .digital import DigitalSpec
from .emitters import EmitterError, emit_c
from .entities import EntitySpec
from .entity_validate import entity_from_mapping
from .errors import BackendError, CapabilityError, LoweringError, OmniError, ValidationError
from .ir import BasicBlock, FunctionIR, ModuleIR, Operation, Value
from .lower import lower_to_ir
from .materialize import MaterializedArtifact, Materializer, validate_materialized_artifact
from .optimize import optimize_module
from .pipeline import CompilationResult, compile_semantics
from .plugins import PluginRegistry
from .runtime import RuntimeErrorBase, execute, execute_module
from .semantics import SemanticModel
from .targeting import TargetMatch, TargetResolutionError, resolve_target
from .targets import TargetDescriptor
from .typecheck import TypeDiagnostic, check_module, is_valid
from .types import TypeKind, TypeRef
from .uir import UIR, UIRValidationError, validate_uir
from .validation import SemanticValidationError, validate_function, validate_module
from .validation_report import ValidationReport, report

__all__ = [
    "ArtifactManifest", "BackendError", "BasicBlock", "CapabilityError", "CapabilityGap", "CapabilityReport",
    "CapabilityRequirement", "CompilationResult", "ConstructionPlan", "DigitalSpec", "EmitterError", "EntitySpec",
    "FunctionIR", "LoweringError", "MaterializedArtifact", "Materializer", "ModuleIR", "OmniError", "Operation",
    "PluginRegistry", "RuntimeErrorBase", "SemanticModel", "SemanticValidationError", "TargetDescriptor",
    "TargetMatch", "TargetResolutionError", "TypeDiagnostic", "TypeKind", "TypeRef", "UIR", "UIRValidationError",
    "ValidationError", "ValidationReport", "Value", "check_module", "compile_semantics", "emit_c", "entity_from_mapping",
    "evaluate_capabilities", "execute", "execute_module", "is_valid", "lower_to_ir", "manifest", "match",
    "optimize_module", "plan_construction", "report", "resolve_target", "validate_materialized_artifact",
    "validate_function", "validate_module",
]
