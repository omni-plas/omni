"""Self-contained x86-64 ELF generator for a validated Omni IR subset.

The backend emits machine code and ELF structures directly; it does not invoke
an external compiler, assembler, or linker. Unsupported IR is rejected.
"""

from __future__ import annotations

import struct
from dataclasses import dataclass

from .ir import ModuleIR
from .targets import TargetDescriptor
from .types import TypeKind

_BASE = 0x400000
_PAGE = 0x1000
_SYSV_INTEGER_ARGUMENT_REGISTERS = (7, 6, 2, 1, 8, 9)  # rdi,rsi,rdx,rcx,r8,r9
_ALLOCATABLE_REGISTERS = (3, 5, 10, 11, 12, 13, 14, 15)


class NativeCodegenError(ValueError):
    pass


@dataclass(frozen=True)
class NativeExecutable:
    target: TargetDescriptor
    payload: bytes
    format: str = "elf-x86_64"


def _rex(w: int = 1, r: int = 0, x: int = 0, b: int = 0) -> int:
    return 0x40 | (w << 3) | (r << 2) | (x << 1) | b


def _mov_imm64(reg: int, value: int) -> bytes:
    if not 0 <= reg <= 15:
        raise NativeCodegenError("invalid register")
    return bytes([_rex(b=(reg >> 3) & 1), 0xB8 + (reg & 7)]) + struct.pack("<Q", value & 0xFFFFFFFFFFFFFFFF)


def _mov_rr(dst: int, src: int) -> bytes:
    if not 0 <= dst <= 15 or not 0 <= src <= 15:
        raise NativeCodegenError("invalid register")
    return bytes([_rex(r=(src >> 3) & 1, b=(dst >> 3) & 1), 0x89, 0xC0 | ((src & 7) << 3) | (dst & 7)])


def _rr(opcode: bytes, dst: int, src: int) -> bytes:
    if not 0 <= dst <= 15 or not 0 <= src <= 15:
        raise NativeCodegenError("invalid register")
    return bytes([_rex(r=(src >> 3) & 1, b=(dst >> 3) & 1)]) + opcode + bytes([0xC0 | ((src & 7) << 3) | (dst & 7)])


def _compile_ops(module: ModuleIR) -> bytes:
    module.validate()
    if len(module.functions) != 1:
        raise NativeCodegenError("ELF bootstrap requires exactly one function")
    function = module.functions[0]
    if len(function.parameters) > len(_SYSV_INTEGER_ARGUMENT_REGISTERS):
        raise NativeCodegenError("ELF bootstrap supports at most six integer parameters")
    if len(function.blocks) != 1:
        raise NativeCodegenError("ELF bootstrap requires exactly one basic block")

    registers: dict[str, int] = {}
    for name, parameter_type in function.parameters.items():
        if parameter_type.kind != TypeKind.INTEGER:
            raise NativeCodegenError(f"unsupported parameter type for {name}: {parameter_type}")
    for (name, _), register in zip(function.parameters.items(), _SYSV_INTEGER_ARGUMENT_REGISTERS):
        registers[name] = register

    free = iter(_ALLOCATABLE_REGISTERS)
    code = bytearray()
    returned = False
    return_reg: int | None = None

    for op in function.blocks[0].operations:
        if returned:
            raise NativeCodegenError("operation appears after return")
        if op.opcode == "const":
            if len(op.outputs) != 1 or "value" not in op.attributes:
                raise NativeCodegenError("const requires one output and value")
            value = op.attributes["value"]
            if not isinstance(value, int) or isinstance(value, bool):
                raise NativeCodegenError("const currently requires an integer")
            if op.outputs[0] in registers:
                raise NativeCodegenError(f"value name already defined: {op.outputs[0]}")
            try:
                reg = next(free)
            except StopIteration as exc:
                raise NativeCodegenError("register limit exceeded") from exc
            registers[op.outputs[0]] = reg
            code += _mov_imm64(reg, value)
            continue

        if op.opcode in {"add", "sub", "mul"}:
            if len(op.inputs) != 2 or len(op.outputs) != 1:
                raise NativeCodegenError(f"{op.opcode} requires two inputs and one output")
            if op.outputs[0] in registers:
                raise NativeCodegenError(f"value name already defined: {op.outputs[0]}")
            try:
                left = registers[op.inputs[0]]
                right = registers[op.inputs[1]]
            except KeyError as exc:
                raise NativeCodegenError(f"undefined operand in {op.opcode}") from exc
            try:
                dst = next(free)
            except StopIteration as exc:
                raise NativeCodegenError("register limit exceeded") from exc
            code += _mov_rr(dst, left)
            if op.opcode == "add":
                code += _rr(b"\x01", dst, right)
            elif op.opcode == "sub":
                code += _rr(b"\x29", dst, right)
            else:
                code += _rr(b"\x0f\xaf", dst, right)
            registers[op.outputs[0]] = dst
            continue

        if op.opcode == "return":
            if len(op.inputs) > 1 or (op.inputs and op.inputs[0] not in registers):
                raise NativeCodegenError("return requires at most one defined operand")
            if op.inputs:
                return_reg = registers[op.inputs[0]]
                if return_reg != 0:
                    code += _mov_rr(0, return_reg)
            else:
                return_reg = 0
                code += _mov_imm64(0, 0)
            code += _mov_rr(7, 0)  # RDI = RAX
            code += _mov_imm64(0, 60)  # RAX = SYS_exit
            code += b"\x0F\x05"  # syscall
            returned = True
            continue

        raise NativeCodegenError(f"unsupported x86-64 operation: {op.opcode}")

    if not returned:
        raise NativeCodegenError("function has no return")
    return bytes(code)


def _elf64(code: bytes) -> bytes:
    phoff = 64
    phentsize = 56
    code_offset = phoff + phentsize
    entry = _BASE + code_offset
    total = code_offset + len(code)
    ehdr = struct.pack(
        "<16sHHIQQQIHHHHHH",
        b"\x7fELF\x02\x01\x01\x00" + b"\x00" * 8,
        2, 62, 1, entry, phoff, 0, 0, 64, 56, 1, 0, 0, 0,
    )
    phdr = struct.pack("<IIQQQQQQ", 1, 7, 0, _BASE, _BASE, total, total, _PAGE)
    return ehdr + phdr + code


def emit_x86_64_elf(module: ModuleIR, target: TargetDescriptor | None = None) -> NativeExecutable:
    requested = target or TargetDescriptor("linux", "x86_64", "sysv", {"native-executable": True})
    if requested.platform not in {"linux", "gnu-linux"} or requested.architecture not in {None, "x86_64", "amd64"}:
        raise NativeCodegenError(f"unsupported ELF bootstrap target: {requested.identity()}")
    return NativeExecutable(requested, _elf64(_compile_ops(module)))
