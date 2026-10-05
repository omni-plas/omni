"""Omni universal digital creation, compilation, packaging and installation engine."""

from .artifact_io import read_artifact_file, write_artifact
from .artifacts import ArtifactManifest, manifest
from .backends import Artifact, Backend, emit_with_backend
from .backend import BackendError, BackendRegistry, BackendSelection, GenericArtifactBackend, TargetBackend
from .control_flow import ControlFlowError, ControlFlowGraph, analyze_control_flow
from .file_association import source_file_association
from .frontends import Frontend, SourceUnit
from .frontend import FrontendRegistry
from .ir import BasicBlock, FunctionIR, IRModule, ModuleIR, Operation, Value
from .language_definition import LanguageDefinition, LanguageDefinitionError
from .language_pack import LanguagePackError, definition_from_mapping, dump_language_pack, load_language_pack, register_language_pack
from .memory_ir import MemoryIROperationError, alloc, free, load, ptr_add, store
from .memory_model import Memory, MemoryModelError, MemoryObject
from .memory_pipeline import EncodedMemoryOp, MemoryPipelineError, encode_memory_operation
from .native_memory_codegen import NativeMemoryCodegenError, add_imm64, add_rr, mov_imm64, mov_mem64, mov_rr, store_mem64
from .native_spill import NativeSpillError, SpillAction, SpillPlan, plan_spills, stack_offset_from_rbp
from .native_backend import NativeArtifactBackend, read_artifact
from .native_codegen import NativeCodegenError, NativeExecutable, emit_x86_64_elf
from .native_multi_codegen import emit_multi_x86_64_elf
from .native_frontend import OmniNativeFrontend
from .oi_file_icon import OI_EXTENSION, OI_ICON_ASSET, OI_ICON_COLOR_MODE, OI_MIME_TYPE, OIFileIconPolicy, native_registration_for_current_os, oi_file_icon_policy
from .oi_registration import OIRegistration, registration_for, render_registration_manifest
from .omni_source import Binary, Call, Function, Let, Literal, Name, OmniSyntaxError, Parser, Program, Return, Token, TokenKind, parse as parse_omni_source, tokenize as tokenize_omni_source
from .omni_lowering import OmniLoweringError, lower_program, lower_source
from .register_alloc import Allocation, LiveInterval, RegisterAllocationError, allocate, compute_intervals
from .registry import CompilerRegistry, RegistryError
from .runtime import RuntimeErrorBase, execute, execute_module
from .source_compiler import ResolvedSource, compile_source, default_compiler_registry, resolve_source
from .universal_pipeline import UniversalCompilationResult, UniversalPipelineError, compile_universal
from .source_files import OmniSourceFileError, is_omni_source_path, load_oi_source, require_omni_source_path
from .stack_model import StackFrame, StackModelError, StackSlot, layout_stack_slots
from .target_pack import TargetPackError, dump_target_pack, load_target_pack, target_from_mapping
from .targets import TargetDescriptor, TargetError
from .types import TypeKind, TypeRef

__all__ = [
    "Allocation", "Artifact", "ArtifactManifest", "Backend", "BackendError", "BackendRegistry", "BackendSelection", "BasicBlock", "Binary", "Call", "CompilerRegistry", "ControlFlowError", "EncodedMemoryOp", "Frontend", "Function", "FunctionIR", "FrontendRegistry", "GenericArtifactBackend", "LanguageDefinition", "LanguageDefinitionError", "LanguagePackError", "Let", "Literal", "LiveInterval", "Memory", "MemoryIROperationError", "MemoryModelError", "MemoryObject", "MemoryPipelineError", "IRModule", "ModuleIR", "Name", "NativeArtifactBackend", "NativeCodegenError", "NativeExecutable", "NativeMemoryCodegenError", "NativeSpillError", "OIFileIconPolicy", "OIRegistration", "OI_EXTENSION", "OI_ICON_ASSET", "OI_ICON_COLOR_MODE", "OI_MIME_TYPE", "OmniLoweringError", "OmniNativeFrontend", "OmniSourceFileError", "OmniSyntaxError", "Operation", "Parser", "Program", "RegisterAllocationError", "RegistryError", "ResolvedSource", "Return", "RuntimeErrorBase", "SourceUnit", "SpillAction", "SpillPlan", "StackFrame", "StackModelError", "StackSlot", "TargetBackend", "TargetDescriptor", "TargetError", "TargetPackError", "Token", "TokenKind", "TypeKind", "TypeRef", "UniversalCompilationResult", "UniversalPipelineError", "Value", "add_imm64", "add_rr", "allocate", "analyze_control_flow", "alloc", "compile_source", "compile_universal", "compute_intervals", "definition_from_mapping", "default_compiler_registry", "dump_language_pack", "dump_target_pack", "emit_multi_x86_64_elf", "emit_x86_64_elf", "encode_memory_operation", "execute", "execute_module", "free", "is_omni_source_path", "layout_stack_slots", "load", "load_language_pack", "load_oi_source", "load_target_pack", "lower_program", "lower_source", "mov_imm64", "mov_mem64", "mov_rr", "native_registration_for_current_os", "oi_file_icon_policy", "parse_omni_source", "plan_spills", "ptr_add", "read_artifact", "read_artifact_file", "register_language_pack", "registration_for", "render_registration_manifest", "require_omni_source_path", "resolve_source", "source_file_association", "stack_offset_from_rbp", "store", "store_mem64", "target_from_mapping", "tokenize_omni_source", "write_artifact",
]
