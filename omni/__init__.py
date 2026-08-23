"""Omni universal digital creation, compilation, packaging and installation engine."""

from .artifact_io import read_artifact_file, write_artifact
from .artifacts import ArtifactManifest, manifest
from .backends import Artifact, Backend, emit_with_backend
from .backend import BackendError, BackendRegistry, BackendSelection, GenericArtifactBackend, TargetBackend
from .control_flow import ControlFlowError, ControlFlowGraph, analyze_control_flow
from .ir import BasicBlock, FunctionIR, ModuleIR, Operation, Value
from .memory_ir import MemoryIROperationError, alloc, free, load, ptr_add, store
from .memory_model import Memory, MemoryModelError, MemoryObject
from .native_memory_codegen import NativeMemoryCodegenError, add_imm64, mov_imm64, mov_mem64, store_mem64
from .native_backend import NativeArtifactBackend, read_artifact
from .native_codegen import NativeCodegenError, NativeExecutable, emit_x86_64_elf
from .native_multi_codegen import emit_multi_x86_64_elf
from .omni_source import Binary, Call, Function, Let, Literal, Name, OmniSyntaxError, Parser, Program, Return, Token, TokenKind, parse as parse_omni_source, tokenize as tokenize_omni_source
from .omni_lowering import OmniLoweringError, lower_program, lower_source
from .runtime import RuntimeErrorBase, execute, execute_module
from .stack_model import StackFrame, StackModelError, StackSlot, layout_stack_slots
from .types import TypeKind, TypeRef

__all__ = [
    "Artifact", "ArtifactManifest", "Backend", "BackendError", "BackendRegistry", "BackendSelection", "BasicBlock", "Binary", "Call", "ControlFlowError", "ControlFlowGraph", "Function", "FunctionIR", "GenericArtifactBackend", "Let", "Literal", "Memory", "MemoryIROperationError", "MemoryModelError", "MemoryObject", "ModuleIR", "Name", "NativeArtifactBackend", "NativeCodegenError", "NativeExecutable", "NativeMemoryCodegenError", "OmniLoweringError", "OmniSyntaxError", "Operation", "Parser", "Program", "Return", "RuntimeErrorBase", "StackFrame", "StackModelError", "StackSlot", "TargetBackend", "Token", "TokenKind", "TypeKind", "TypeRef", "Value", "add_imm64", "alloc", "analyze_control_flow", "emit_multi_x86_64_elf", "emit_x86_64_elf", "execute", "execute_module", "free", "layout_stack_slots", "load", "lower_program", "lower_source", "mov_imm64", "mov_mem64", "parse_omni_source", "ptr_add", "read_artifact", "read_artifact_file", "store", "store_mem64", "tokenize_omni_source", "write_artifact",
]
