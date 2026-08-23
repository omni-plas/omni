"""Multi-function x86-64 native emitter for the Omni bootstrap subset."""

from __future__ import annotations

import struct

from .ir import ModuleIR
from .native_codegen import NativeCodegenError, NativeExecutable
from .targets import TargetDescriptor
from .types import TypeKind

_BASE = 0x400000
_PAGE = 0x1000
_ARG_REGS = (7, 6, 2, 1, 8, 9)
_WORK_REGS = (3, 4, 5, 10, 11, 12, 13, 14, 15)


def _rex(w=1, r=0, b=0):
    return bytes([0x40 | (w << 3) | (r << 2) | b])


def _mov_imm(reg, value):
    return _rex(b=(reg >> 3) & 1) + bytes([0xB8 + (reg & 7)]) + struct.pack("<Q", value & 0xFFFFFFFFFFFFFFFF)


def _mov_rr(dst, src):
    return _rex(r=(src >> 3) & 1, b=(dst >> 3) & 1) + b"\x89" + bytes([0xC0 | ((src & 7) << 3) | (dst & 7)])


def _rr(op, dst, src):
    return _rex(r=(src >> 3) & 1, b=(dst >> 3) & 1) + op + bytes([0xC0 | ((src & 7) << 3) | (dst & 7)])


def _call_rel32(displacement):
    return b"\xE8" + struct.pack("<i", displacement)


def _compile_function(fn, known):
    if len(fn.parameters) > len(_ARG_REGS):
        raise NativeCodegenError(f"too many parameters: {fn.name}")
    if len(fn.blocks) != 1:
        raise NativeCodegenError(f"function must have one block: {fn.name}")
    regs = {}
    for (name, typ), reg in zip(fn.parameters.items(), _ARG_REGS):
        if typ.kind != TypeKind.INTEGER:
            raise NativeCodegenError(f"non-integer parameter: {name}")
        regs[name] = reg
    free = iter(_WORK_REGS)
    code = bytearray()
    fixups = []
    returned = False
    for op in fn.blocks[0].operations:
        if returned:
            raise NativeCodegenError(f"operation after return in {fn.name}")
        if op.opcode == "const":
            value = op.attributes.get("value")
            if len(op.outputs) != 1 or not isinstance(value, int) or isinstance(value, bool):
                raise NativeCodegenError("integer const required")
            try:
                reg = next(free)
            except StopIteration as exc:
                raise NativeCodegenError("register limit exceeded") from exc
            regs[op.outputs[0]] = reg
            code += _mov_imm(reg, value)
        elif op.opcode in {"add", "sub", "mul"}:
            if len(op.inputs) != 2 or len(op.outputs) != 1:
                raise NativeCodegenError("binary operation arity")
            try:
                left, right = regs[op.inputs[0]], regs[op.inputs[1]]
            except (KeyError, IndexError) as exc:
                raise NativeCodegenError("undefined binary operand") from exc
            try:
                dst = next(free)
            except StopIteration as exc:
                raise NativeCodegenError("register limit exceeded") from exc
            code += _mov_rr(dst, left)
            code += _rr({"add": b"\x01", "sub": b"\x29", "mul": b"\x0f\xaf"}[op.opcode], dst, right)
            regs[op.outputs[0]] = dst
        elif op.opcode == "move":
            if len(op.inputs) != 1 or len(op.outputs) != 1 or op.inputs[0] not in regs:
                raise NativeCodegenError("invalid move")
            try:
                dst = next(free)
            except StopIteration as exc:
                raise NativeCodegenError("register limit exceeded") from exc
            code += _mov_rr(dst, regs[op.inputs[0]])
            regs[op.outputs[0]] = dst
        elif op.opcode == "call":
            callee = op.attributes.get("callee")
            if callee not in known:
                raise NativeCodegenError(f"unknown callee: {callee}")
            if len(op.inputs) > len(_ARG_REGS):
                raise NativeCodegenError("too many call arguments")
            for i, name in enumerate(op.inputs):
                if name not in regs:
                    raise NativeCodegenError(f"undefined call argument: {name}")
                if regs[name] != _ARG_REGS[i]:
                    code += _mov_rr(_ARG_REGS[i], regs[name])
            pos = len(code)
            code += _call_rel32(0)
            fixups.append((pos, callee))
            if len(op.outputs) != 1:
                raise NativeCodegenError("call requires one output")
            try:
                dst = next(free)
            except StopIteration as exc:
                raise NativeCodegenError("register limit exceeded") from exc
            code += _mov_rr(dst, 0)
            regs[op.outputs[0]] = dst
        elif op.opcode == "return":
            if len(op.inputs) != 1 or op.inputs[0] not in regs:
                raise NativeCodegenError("invalid return")
            code += _mov_rr(0, regs[op.inputs[0]])
            code += (_mov_rr(7, 0) + _mov_imm(0, 60) + b"\x0f\x05") if fn.name == "main" else b"\xc3"
            returned = True
        else:
            raise NativeCodegenError(f"unsupported operation: {op.opcode}")
    if not returned:
        raise NativeCodegenError(f"function has no return: {fn.name}")
    return bytes(code), fixups


def _elf(code, entry):
    off = 120
    total = off + len(code)
    header = struct.pack(
        "<16sHHIQQQIHHHHHH",
        b"\x7fELF\x02\x01\x01\x00" + b"\x00" * 8,
        2, 62, 1, entry, 64, 0, 0, 64, 56, 1, 0, 0, 0,
    )
    program = struct.pack("<IIQQQQQQ", 1, 7, 0, _BASE, _BASE, total, total, _PAGE)
    return header + program + code


def emit_multi_x86_64_elf(module: ModuleIR, target: TargetDescriptor | None = None) -> NativeExecutable:
    module.validate()
    names = [fn.name for fn in module.functions]
    if len(set(names)) != len(names):
        raise NativeCodegenError("duplicate function name")
    if "main" not in names:
        raise NativeCodegenError("native executable requires main")
    requested = target or TargetDescriptor("linux", "x86_64", "sysv", {"native-executable": True})
    if requested.platform not in {"linux", "gnu-linux"} or requested.architecture not in {None, "x86_64", "amd64"}:
        raise NativeCodegenError(f"unsupported target: {requested.identity()}")
    offsets = {}
    chunks = []
    all_fixups = []
    cursor = 0
    known = set(names)
    for fn in module.functions:
        offsets[fn.name] = cursor
        chunk, fixups = _compile_function(fn, known)
        chunks.append(chunk)
        all_fixups.append((cursor, fixups))
        cursor += len(chunk)
    code = bytearray(b"".join(chunks))
    for base, fixups in all_fixups:
        for pos, callee in fixups:
            rel = offsets[callee] - (base + pos + 5)
            code[base + pos:base + pos + 5] = _call_rel32(rel)
    entry = _BASE + 120 + offsets["main"]
    return NativeExecutable(requested, _elf(bytes(code), entry))
