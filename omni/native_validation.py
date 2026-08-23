"""Strict validation for Omni's bootstrap ELF artifacts."""

from __future__ import annotations

import struct

from .native_codegen import NativeExecutable


def validate_x86_64_elf(executable: NativeExecutable) -> None:
    payload = executable.payload
    if len(payload) < 120:
        raise ValueError("native executable is too small to contain ELF64 headers")
    if payload[:4] != b"\x7fELF":
        raise ValueError("invalid ELF magic")
    if payload[4] != 2 or payload[5] != 1:
        raise ValueError("native executable must be ELF64 little-endian")
    machine = struct.unpack_from("<H", payload, 18)[0]
    if machine != 62:
        raise ValueError("native executable is not x86-64")
    phoff = struct.unpack_from("<Q", payload, 32)[0]
    phentsize = struct.unpack_from("<H", payload, 54)[0]
    phnum = struct.unpack_from("<H", payload, 56)[0]
    if phoff != 64 or phentsize != 56 or phnum != 1:
        raise ValueError("unexpected ELF program-header layout")
    p_offset = struct.unpack_from("<Q", payload, phoff + 8)[0]
    p_filesz = struct.unpack_from("<Q", payload, phoff + 32)[0]
    if p_offset != 0 or p_filesz != len(payload):
        raise ValueError("ELF load segment does not cover the artifact")
