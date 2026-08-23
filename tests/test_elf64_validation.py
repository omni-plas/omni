import pytest
from omni.elf64 import ELFError, build_elf64


def test_empty_code_is_rejected():
    with pytest.raises(ELFError):
        build_elf64(b"")


def test_invalid_entry_is_rejected():
    with pytest.raises(ELFError):
        build_elf64(b"\xc3", 1)
