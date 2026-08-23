import pytest

from omni.native_codegen import NativeCodegenError
from omni.native_multi_codegen import emit_multi_x86_64_elf
from omni.omni_lowering import lower_source


def test_native_backend_rejects_missing_main():
    with pytest.raises(NativeCodegenError, match="requires main"):
        emit_multi_x86_64_elf(lower_source("fn worker() { return 1; }"))


def test_native_backend_rejects_unknown_native_call():
    module = lower_source("fn main() { return missing(1); }")
    # Semantic lowering normally catches this before native codegen.
    with pytest.raises(Exception):
        emit_multi_x86_64_elf(module)
