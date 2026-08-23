import pytest
from omni.native_target import NativeTarget
from omni.native_build_target import validate_target


def test_supported_target():
    assert validate_target(NativeTarget('linux','x86_64','sysv'))


def test_unsupported_architecture():
    with pytest.raises(ValueError):
        validate_target(NativeTarget('linux','aarch64','sysv'))
