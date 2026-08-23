"""Omni universal digital creation, compilation, packaging and installation engine."""

from .artifact_io import read_artifact_file, write_artifact
from .artifacts import ArtifactManifest, manifest
from .backends import Artifact, Backend, emit_with_backend
from .backend import BackendError, BackendRegistry, BackendSelection, GenericArtifactBackend, TargetBackend
from .boot_backend import BootArtifact, BootBackend, ContainerBootBackend, build_boot_artifact
from .boot_contract import BootContract, require_boot_capabilities
from .boot_manifest import BootManifest, create_boot_manifest
from .boot_manifest_verify import verify_boot_manifest
from .boot_pipeline import VerifiedBootResult, build_verified_boot
from .boot_registry import BootBackendMatch, BootBackendRegistry
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
from .frontend import Frontend, FrontendCandidate, FrontendRegistry
from .frontend_metadata import FrontendMetadata
from .fs_materializer import FilesystemMaterializationError, MaterializedFile, materialize_to_directory
from .installer import InstallationError, InstallationPlan, InstallerKind, plan_installation
from .installer_apply import apply_installer
from .installer_builder import InstallerBuildError, InstallerBundle, build_installer, write_installer
from .installer_runtime import InstallerRuntimeError, extract_installer, inspect_installer
from .installer_verify import InstallerVerificationError, verify_installer
from .ir import BasicBlock, FunctionIR, ModuleIR, Operation, Value
from .language import OmniKeyword, OmniProgram
from .lower import lower_to_ir
from .materialize import MaterializedArtifact, Materializer, validate_materialized_artifact
from .materializer import MaterializationError, MaterializationPlan, create_materialization_plan
from .native_backend import NativeArtifactBackend, read_artifact
from .native_codegen import NativeCodegenError, NativeExecutable, emit_x86_64_elf
from .native_executable import compile_native_executable, write_native_executable
from .native_frontend import OmniNativeFrontend
from .native_pipeline import compile_native
from .omni_bootstrap import OmniBootstrapArtifact, build_bootstrap
from .omni_frontend import OmniFrontend
from .omni_source import Binary, Call, Function, Let, Literal, Name, OmniSyntaxError, Parser, Program, Return, Token, TokenKind, parse as parse_omni_source, tokenize as tokenize_omni_source
from .omni_runtime import OmniRuntimeError, execute_function
from .optimize import optimize_module
from .os_image import OSImage, OSImageError, build_os_image
from .os_image_parse import OSImageFile, ParsedOSImage, parse_os_image
from .os_model import OSModelError, OperatingSystemSpec
from .package_writer import PackageWriteError, build_package, write_package
from .packaging import PackageError, PackageManifest
from .pipeline import CompilationResult, compile_semantics
from .plugins import PluginRegistry
from .release_pipeline import ReleasePipelineError, ReleaseResult, build_release, write_release
from .runtime import RuntimeErrorBase, execute, execute_module
from .self_build import SelfBuildError, SelfBuildResult, SelfBuildSpec, SelfBuildStage, plan_self_build, source_digest, validate_self_build_result
from .semantics import SemanticModel
from .serialization import SerializationError, dumps_uir, loads_uir
from .source_model import SourceNode, SourceSpan, SourceUnit
from .source_pipeline import SourceCompilationResult, SourcePipelineError, compile_source
from .target_artifact import validate_artifact_for_target
from .target_context import apply_target_context
from .target_installers import InstallerFormat, InstallerTarget, resolve_installer_target
from .target_model import TargetModel
from .targeting import TargetMatch, TargetResolutionError, resolve_target
from .targets import TargetDescriptor
from .typecheck import TypeDiagnostic, check_module, is_valid
from .types import TypeKind, TypeRef
from .uir import UIR, UIRValidationError, validate_uir
from .universal_pipeline import UniversalCompilationResult, UniversalPipelineError, compile_universal
from .validation import SemanticValidationError, validate_function, validate_module
from .validation_report import ValidationReport, report

__all__ = [
    "Artifact", "ArtifactManifest", "Backend", "BackendCompilationResult", "BackendError", "BackendRegistry", "BackendSelection", "BasicBlock", "Binary", "BootArtifact", "BootBackend", "BootBackendMatch", "BootBackendRegistry", "BootContract", "BootManifest", "BuildPipelineError", "Call", "CapabilityError", "CapabilityGap", "CapabilityReport", "CapabilityRequirement", "CompilationError", "CompilationPlan", "CompilationResult", "ConstructionPlan", "ContainerBootBackend", "CreationPlan", "CreationStep", "Diagnostic", "DigitalSpec", "EmitterError", "EntitySpec", "Frontend", "FrontendCandidate", "FrontendMetadata", "FrontendRegistry", "FilesystemMaterializationError", "Function", "FunctionIR", "GenericArtifactBackend", "InstallationError", "InstallationPlan", "InstallerBuildError", "InstallerBundle", "InstallerFormat", "InstallerKind", "InstallerRuntimeError", "InstallerTarget", "InstallerVerificationError", "Let", "Literal", "LoweringError", "MaterializedArtifact", "MaterializedFile", "Materializer", "MaterializationError", "MaterializationPlan", "ModuleIR", "Name", "NativeArtifactBackend", "NativeCodegenError", "NativeExecutable", "OmniBootstrapArtifact", "OSImage", "OSImageError", "OSImageFile", "OmniError", "OmniFrontend", "OmniKeyword", "OmniNativeFrontend", "OmniProgram", "OmniRuntimeError", "OmniSyntaxError", "Operation", "OSBuildPlan", "OSModelError", "OperatingSystemSpec", "PackageError", "PackageManifest", "PackageWriteError", "Parser", "PluginRegistry", "Program", "ReleasePipelineError", "ReleaseResult", "Return", "RuntimeErrorBase", "SemanticModel", "SelfBuildError", "SelfBuildResult", "SelfBuildSpec", "SelfBuildStage", "SemanticValidationError", "SerializationError", "Severity", "SourceCompilationResult", "SourceNode", "SourcePipelineError", "SourceSpan", "SourceUnit", "TargetBackend", "TargetDescriptor", "TargetMatch", "TargetModel", "TargetResolutionError", "Token", "TokenKind", "TypeDiagnostic", "TypeKind", "TypeRef", "UIR", "UIRValidationError", "UniversalCompilationResult", "UniversalPipelineError", "ValidationError", "ValidationReport", "Value", "VerifiedBootResult", "apply_installer", "apply_target_context", "build_boot_artifact", "build_bootstrap", "build_installer", "build_os_image", "build_package", "build_release", "build_verified_boot", "check_module", "compile_native", "compile_native_executable", "compile_semantics", "compile_universal", "compile_source", "compile_uir", "create_boot_manifest", "create_materialization_plan", "create_os_build_plan", "dumps_uir", "emit_c", "emit_with_backend", "emit_x86_64_elf", "entity_from_mapping", "evaluate_capabilities", "execute", "execute_function", "execute_module", "extract_installer", "format_diagnostics", "inspect_installer", "is_valid", "loads_uir", "lower_to_ir", "manifest", "match", "materialize_to_directory", "optimize_module", "parse_omni_source", "parse_os_image", "plan_compilation", "plan_construction", "plan_creation", "plan_installation", "plan_self_build", "read_artifact", "read_artifact_file", "report", "require_boot_capabilities", "resolve_installer_target", "resolve_target", "source_digest", "tokenize_omni_source", "validate_artifact_for_target", "validate_function", "validate_module", "validate_self_build_result", "validate_uir", "verify_boot_manifest", "verify_installer", "write_artifact", "write_installer", "write_native_executable", "write_package", "write_release",
]
