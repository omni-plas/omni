"""Omni universal digital creation, compilation, packaging and installation engine."""

from .artifacts import ArtifactManifest, manifest
from .backends import Artifact, Backend, emit_with_backend
from .build_pipeline import BuildPipelineError, OSBuildPlan, create_os_build_plan
from .capabilities import CapabilityGap, CapabilityReport, match
from .capability import CapabilityRequirement, evaluate_capabilities
from .compiler import CompilationError, CompilationPlan, plan_compilation
from .construct import ConstructionPlan, plan_construction
from .creation import CreationPlan, CreationStep, plan_creation
from .diagnostics import Diagnostic, Severity, format_diagnostics
from .digital import DigitalSpec
from .emitters import EmitterError, emit_c
from .entities import EntitySpec
from .entity_validate import entity_from_mapping
from .errors import BackendError, CapabilityError, LoweringError, OmniError, ValidationError
from .frontend import Frontend, FrontendRegistry
from .fs_materializer import FilesystemMaterializationError, MaterializedFile, materialize_to_directory
from .installer import InstallationError, InstallationPlan, InstallerKind, plan_installation
from .installer_builder import InstallerBuildError, InstallerBundle, build_installer, write_installer
from .ir import BasicBlock, FunctionIR, ModuleIR, Operation, Value
from .language import OmniKeyword, OmniProgram
from .lexer import Token, tokenize
from .lower import lower_to_ir
from .materialize import MaterializedArtifact, Materializer, validate_materialized_artifact
from .materializer import MaterializationError, MaterializationPlan, create_materialization_plan
from .optimize import optimize_module
from .os_model import OSModelError, OperatingSystemSpec
from .package_writer import PackageWriteError, build_package, write_package
from .packaging import PackageError, PackageManifest
from .pipeline import CompilationResult, compile_semantics
from .plugins import PluginRegistry
from .release_pipeline import ReleasePipelineError, ReleaseResult, build_release, write_release
from .runtime import RuntimeErrorBase, execute, execute_module
from .semantics import SemanticModel
from .serialization import SerializationError, dumps_uir, loads_uir
from .source_model import SourceNode, SourceSpan, SourceUnit
from .target_model import TargetModel
from .targeting import TargetMatch, TargetResolutionError, resolve_target
from .targets import TargetDescriptor
from .typecheck import TypeDiagnostic, check_module, is_valid
from .types import TypeKind, TypeRef
from .uir import UIR, UIRValidationError, validate_uir
from .validation import SemanticValidationError, validate_function, validate_module
from .validation_report import ValidationReport, report

__all__ = [
    "Artifact", "ArtifactManifest", "Backend", "BackendError", "BasicBlock", "BuildPipelineError", "CapabilityError",
    "CapabilityGap", "CapabilityReport", "CapabilityRequirement", "CompilationError", "CompilationPlan", "CompilationResult",
    "ConstructionPlan", "CreationPlan", "CreationStep", "Diagnostic", "DigitalSpec", "EmitterError", "EntitySpec", "Frontend",
    "FrontendRegistry", "FilesystemMaterializationError", "FunctionIR", "InstallationError", "InstallationPlan", "InstallerBuildError",
    "InstallerBundle", "InstallerKind", "LoweringError", "MaterializedArtifact", "MaterializedFile", "Materializer", "MaterializationError",
    "MaterializationPlan", "ModuleIR", "OmniError", "OmniKeyword", "OmniProgram", "Operation", "OSBuildPlan", "OSModelError",
    "OperatingSystemSpec", "PackageError", "PackageManifest", "PackageWriteError", "PluginRegistry", "ReleasePipelineError", "ReleaseResult",
    "RuntimeErrorBase", "SemanticModel", "SemanticValidationError", "SerializationError", "Severity", "SourceNode", "SourceSpan", "SourceUnit",
    "TargetDescriptor", "TargetMatch", "TargetModel", "TargetResolutionError", "Token", "TypeDiagnostic", "TypeKind", "TypeRef", "UIR",
    "UIRValidationError", "ValidationError", "ValidationReport", "Value", "build_installer", "build_package", "build_release", "check_module",
    "compile_semantics", "create_materialization_plan", "create_os_build_plan", "dumps_uir", "emit_c", "emit_with_backend", "entity_from_mapping",
    "evaluate_capabilities", "execute", "execute_module", "format_diagnostics", "is_valid", "loads_uir", "lower_to_ir", "manifest", "match",
    "materialize_to_directory", "optimize_module", "plan_compilation", "plan_construction", "plan_creation", "plan_installation", "report",
    "resolve_target", "tokenize", "validate_materialized_artifact", "validate_function", "validate_module", "validate_uir", "write_installer",
    "write_package", "write_release",
]
