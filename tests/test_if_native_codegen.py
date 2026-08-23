from omni.native_multi_codegen import emit_multi_x86_64_elf
from omni.omni_lowering import lower_source


def test_if_else_lowers_to_cfg():
    module = lower_source('fn main(x) { if (x > 10) { return 1; } else { return 0; } }')
    fn = module.functions[0]
    assert len(fn.blocks) >= 3
    assert any(op.opcode == 'branch' for block in fn.blocks for op in block.operations)


def test_if_else_reaches_native_elf():
    module = lower_source('fn main(x) { if (x > 10) { return 1; } else { return 0; } }')
    executable = emit_multi_x86_64_elf(module)
    assert executable.payload[:4] == b'\x7fELF'
