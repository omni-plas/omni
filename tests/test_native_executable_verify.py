import pytest
from omni.native_executable_verify import verify_elf64


def test_verify_elf64_accepts_header():
    blob=b'\x7fELF'+bytes([2,1])+b'\0'*58
    assert verify_elf64(blob)


def test_verify_elf64_rejects_non_elf():
    with pytest.raises(ValueError):
        verify_elf64(b'bad')
