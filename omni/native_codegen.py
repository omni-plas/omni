"""Minimal self-contained x86-64 ELF generator for the Omni IR subset.

No external assembler or compiler is used. The backend currently supports one
zero-argument function, one basic block, integer constants, add/sub/mul, and
return. Unsupported IR is rejected explicitly so the result is never
mistaken for a partially compiled executable.
"""

from __future__ import annotations

import struct
from dataclasses import dataclass

from .ir import ModuleIR, Operation
from .targets import TargetDescriptor

_BASE = 0x400000
_PAGE = 0x1000
_ELF64_EHDR = 64
_ELF64_PHDR = 56


class NativeCodegenError(ValueError):
    pass


@dataclass(frozen=True)
class NativeExecutable:
    target: TargetDescriptor
    payload: bytes
    format: str = "elf-x86_64"


def _rex(reg: int, rm: int) -> int:
    return 0x48 | ((reg >> 3) & 1) << 2 | ((rm >> 3) & 1)


def _mov_imm64(reg: int, value: int) -> bytes:
    if not 0 <= reg <= 15:
        raise NativeCodegenError("invalid register")
    return bytes([0x48 | ((reg >> 3) & 1), 0xB8 + (reg & 7)]) + struct.pack("<Q", value & 0xFFFFFFFFFFFFFFFF)


def _rr(opcode: bytes, dst: int, src: int) -> bytes:
    if not 0 <= dst <= 15 or not 0 <= src <= 15:
        raise NativeCodegenError("invalid register")
    return bytes([_rex(src, dst)]) + opcode + bytes([0xC0 | ((src & 7) << 3) | (dst & 7)])


def _compile_ops(module: ModuleIR) -> bytes:
    module.validate()
    if len(module.functions) != 1:
        raise NativeCodegenError("ELF bootstrap requires exactly one function")
    function = module.functions[0]
    if function.parameters:
        raise NativeCodegenError("ELF bootstrap requires a zero-argument function")
    if len(function.blocks) != 1:
        raise NativeCodegenError("ELF bootstrap requires exactly one basic block")

    registers: dict[str, int] = {}
    free = iter(range(10))  # rax..r9
    code = bytearray()
    returned = False
    for op in function.blocks[0].operations:
        if op.opcode == "const":
            if len(op.outputs) != 1 or "value" not in op.attributes:
                raise NativeCodegenError("const requires one output and value")
            if not isinstance(op.attributes["value"], int) or isinstance(op.attributes["value"], bool):
                raise NativeCodegenError("const currently requires an integer")
            try:
                reg = next(free)
            except StopIteration as exc:
                raise NativeCodegenError("register limit exceeded") from exc
            registers[op.outputs[0]] = reg
            code += _mov_imm64(reg, op.attributes["value"])
            continue
        if op.opcode in {"add", "sub", "mul"}:
            if len(op.inputs) != 2 or len(op.outputs) != 1:
                raise NativeCodegenError(f"{op.opcode} requires two inputs and one output")
            if op.inputs[0] not in registers or op.inputs[1] not in registers:
                raise NativeCodegenError(f"undefined operand in {op.opcode}")
            try:
                dst = next(free)
            except StopIteration as exc:
                raise NativeCodegenError("register limit exceeded") from exc
            left, right = registers[op.inputs[0]], registers[op.inputs[1]]
            code += _mov_imm64(dst, 0)
            code += _rr(b"\x01", dst, left)
            if op.opcode == "add":
                code += _rr(b"\x01", dst, right)
            elif op.opcode == "sub":
                code += _rr(b"\x29", dst, right)
                # dst currently equals left; 0 + left - right.
            else:
                code += _rr(b"\x0f\xaf", dst, right)
            registers[op.outputs[0]] = dst
            continue
        if op.opcode == "return":
            if len(op.inputs) != 1 or op.inputs[0] not in registers:
                raise NativeCodegenError("return requires one defined operand")
            source = registers[op.inputs[0]]
            if source != 0:
                code += _rr(b"\x89", 0, source)
            code += b"\xC3"
            returned = True
            continue
        raise NativeCodegenError(f"unsupported x86-64 operation: {op.opcode}")
    if not returned:
        raise NativeCodegenError("function has no return")
    return bytes(code)


def _elf64(code: bytes) -> bytes:
    phoff = _ELF64_EHDR
    code_offset = _ELF64_EHDR + _ELF64_PHDR
    entry = _BASE + code_offset
    total = code_offset + len(code)
    ehdr = struct.pack(
        "<16sHHIQQQIHHHHHH",
        b"\x7fELF\x02\x01\x01\x00" + b"\x00" * 8,
        2, 62, 1, entry, phoff, 0, 0, _ELF64_EHDR, _ELF64_PHDR, 1, 0, 0, 0,
    )
    phdr = struct.pack(
        "<IIQQQQQQ",
        1, 7, 0, _BASE, _BASE, total, total, _PAGE,
    )
    return ehdr + phdr + code


def emit_x86_64_elf(module: ModuleIR, target: TargetDescriptor | None = None) -> NativeExecutable:
    requested = target or TargetDescriptor("linux", "x86_64", "sysv", {"native-executable": True})
    if requested.platform not in {"linux", "gnu-linux"} or requested.architecture not in {None, "x86_64", "amd64"}:
        raise NativeCodegenError(f"unsupported ELF bootstrap target: {requested.identity()}")
    code = _compile_ops(module)
    return NativeExecutable(requested, _elf64(code))
