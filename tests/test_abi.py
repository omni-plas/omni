import pytest

from omni.abi import ABIError, SYSV_AMD64, validate_arity


def test_sysv_integer_argument_registers():
    assert SYSV_AMD64.integer_argument_registers == (7, 6, 2, 1, 8, 9)
    assert SYSV_AMD64.return_register == 0
    assert SYSV_AMD64.stack_alignment == 16


def test_abi_rejects_too_many_integer_arguments():
    with pytest.raises(ABIError):
        validate_arity(SYSV_AMD64, 7)
