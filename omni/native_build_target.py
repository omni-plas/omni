"""Validate native build targets before code generation."""
from __future__ import annotations
from .native_target import NativeTarget

SUPPORTED_ABIS={'x86_64':{'sysv','win64'}}

def validate_target(target:NativeTarget):
    if target.arch not in SUPPORTED_ABIS:
        raise ValueError(f'unsupported architecture: {target.arch}')
    if target.abi not in SUPPORTED_ABIS[target.arch]:
        raise ValueError(f'unsupported ABI: {target.abi}')
    if not target.os:
        raise ValueError('target OS is required')
    return True
