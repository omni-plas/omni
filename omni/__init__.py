"""Omni universal digital creation, compilation, packaging and installation engine."""

from .artifact_io import read_artifact_file, write_artifact
from .artifacts import ArtifactManifest, manifest
from .backends import Artifact, Backend, emit_with_backend
from .backend import BackendError, BackendRegistry, BackendSelection, GenericArtifactBackend, TargetBackend
from .build_pipeline import BuildPipelineError, OSBuildPlan, create_os_build_plan
from .capabilities import CapabilityGap, CapabilityReport, match
from .capability import CapabilityRequirement, evaluate_capabilities
from .compiler import CompilationError, CompilationPlan, plan_compilation
from .compile_engine import CompilationResult as BackendCompilationResult, compile_uir
from .construct import ConstructionPlan, plan_construction
from .creation import CreationPlan, CreationStep, plan_creation
from .diagnostics import Diagnostic, Severity, format_diagnostics
from .digital import DigitalSpec
from .emitters import EmitterError, emit_c
from .entities import EntitySpec
from .entity_validate import entity_from_mapping
from .errors import CapabilityError, LoweringError, OmniError, ValidationError
from .frontend import Frontend, FrontendRegistry
from .fs_materializer import FilesystemMaterializationError, MaterializedFile, materialize_to_directory
from .installer import InstallationError, InstallationPlan, InstallerKind, plan_installation
from .installer_apply import apply_installer
from .installer_builder import InstallerBuildError, InstallerBundle, build_installer, write_installer
from .installer_runtime import InstallerRuntimeError, extract_installer, inspect_installer
from .installer_verify import InstallerVerificationError, verify_installer
from .ir import BasicBlock, FunctionIR, ModuleIR, Operation, Value
from .language import OmniKeyword, OmniProgram
from .lexer import Token, tokenize
from .lower import lower_to_ir
from .materialize import MaterializedArtifact, Materializer, validate_materialized_artifact
from .materializer import MaterializationError, MaterializationPlan, create_materialization_plan
from .native_backend import NativeArtifactBackend, read_artifact
from .native_codegen import NativeCodegenError, NativeExecutable, emit_x86_64_elf
from .native_executable import compile_native_executable, write_native_executable
from .native_frontend import OmniNativeFrontend
from .native_pipeline import compile_native
from .omni_frontend import OmniFrontend
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
from .source_pipeline import SourceCompilationResult, SourcePipelineError, compile_source
from .target_artifact import validate_artifact_for_target
from .target_installers import InstallerFormat, InstallerTarget, resolve_installer_target
from .target_model import TargetModel
from .targeting import TargetMatch, TargetResolutionError, resolve_target
from .targets import TargetDescriptor
from .typecheck import TypeDiagnostic, check_module, is_valid
from .types import TypeKind, TypeRef
from .uir import UIR, UIRValidationError, validate_uir
from .validation import SemanticValidationError, validate_function, validate_module
from .validation_report import ValidationReport, report

__all__ = [
    "Artifact", "ArtifactManifest", "Backend", "BackendCompilationResult", "BackendError", "BackendRegistry", "BackendSelection", "BasicBlock",
    "BuildPipelineError", "CapabilityError", "CapabilityGap", "CapabilityReport", "CapabilityRequirement", "CompilationError", "CompilationPlan",
    "CompilationResult", "ConstructionPlan", "CreationPlan", "CreationStep", "Diagnostic", "DigitalSpec", "EmitterError", "EntitySpec", "Frontend",
    "FrontendRegistry", "FilesystemMaterializationError", "FunctionIR", "GenericArtifactBackend", "InstallationError", "InstallationPlan", "InstallerBuildError",
    "InstallerBundle", "InstallerFormat", "InstallerKind", "InstallerRuntimeError", "InstallerTarget", "InstallerVerificationError", "LoweringError", "MaterializedArtifact", "MaterializedFile", "Materializer", "MaterializationError", "MaterializationPlan",
    "ModuleIR", "NativeArtifactBackend", "NativeCodegenError", "NativeExecutable", "OmniError", "OmniFrontend", "OmniKeyword", "OmniNativeFrontend", "OmniProgram", "Operation", "OSBuildPlan", "OSModelError", "OperatingSystemSpec",
    "PackageError", "PackageManifest", "PackageWriteError", "PluginRegistry", "ReleasePipelineError", "ReleaseResult", "RuntimeErrorBase", "SemanticModel",
    "SemanticValidationError", "SerializationError", "Severity", "SourceCompilationResult", "SourceNode", "SourcePipelineError", "SourceSpan", "SourceUnit",
    "TargetBackend", "TargetDescriptor", "TargetMatch", "TargetModel", "TargetResolutionError", "Token", "TypeDiagnostic", "TypeKind", "TypeRef", "UIR",
    "UIRValidationError", "ValidationError", "ValidationReport", "Value", "apply_installer", "build_installer", "build_package", "build_release", "check_module", "compile_native", "compile_native_executable", "compile_semantics",
    "compile_source", "compile_uir", "create_materialization_plan", "create_os_build_plan", "dumps_uir", "emit_c", "emit_with_backend", "emit_x86_64_elf", "entity_from_mapping",
    "evaluate_capabilities", "execute", "execute_module", "extract_installer", "format_diagnostics", "inspect_installer", "is_valid", "loads_uir", "lower_to_ir", "manifest", "match", "read_artifact", "read_artifact_file",
    "materialize_to_directory", "optimize_module", "plan_compilation", "plan_construction", "plan_creation", "plan_installation", "report", "resolve_installer_target", "resolve_target", "tokenize", "validate_artifact_for_target",
    "validate_materialized_artifact", "validate_function", "validate_module", "validate_uir", "verify_installer", "write_artifact", "write_installer", "write_native_executable", "write_package", "write_release",
]
