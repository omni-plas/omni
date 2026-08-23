"""Build a verified native artifact directly from FunctionIR values."""
from __future__ import annotations
from .native_build_driver import build_artifact
from .native_manifest_builder import manifest_for_functions
from .native_target import NativeTarget
from .native_function_module import compile_functions
from .native_module_linker import NativeFragment
from .native_executable_pipeline import link_module


def build_function_ir(functions, *, target=None, entry=None):
    funcs=tuple(functions)
    target=target or NativeTarget('linux','x86_64','sysv')
    manifest_obj=manifest_for_functions(funcs,target.os,target.arch,entry)
    manifest=manifest_obj.as_dict()
    manifest['symbols']={name:0 for name in manifest_obj.symbols}
    manifest['entry_offset']=0

    def emit():
        linked=compile_functions(funcs)
        if not linked.symbols:
            raise ValueError('module contains no functions')
        if manifest_obj.entry not in linked.symbols:
            raise KeyError(manifest_obj.entry)
        image=link_module((NativeFragment('__module__',linked.code),),None)
        return image.data

    return build_artifact(emit,target,manifest)
