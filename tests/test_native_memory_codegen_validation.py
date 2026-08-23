import pytest

from omni.native_memory_codegen import NativeMemoryCodegenError, add_imm64, mov_mem64, store_mem64


def test_rejects_invalid_registers():
    with pytest.raises(NativeMemoryCodegenError):
        add_imm64(16, 1)


def test_rejects_large_memory_displacement():
    with pytest.raises(NativeMemoryCodegenError):
        mov_mem64(0, 3, 128)


def test_rejects_sib_register_until_dedicated_encoder_exists():
    with pytest.raises(NativeMemoryCodegenError):
        store_mem64(4, 0, 0)
