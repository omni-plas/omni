import pytest

from omni.ir import Operation
from omni.omni_lowering import OmniLoweringError, lower_source
from omni.types import TypeKind


def test_lower_integer_function_to_ir():
    module = lower_source('fn main(a, b) { let x = a + b * 2; return x; }')
    module.validate()
    fn = module.functions[0]
    assert fn.name == 'main'
    assert fn.result.kind == TypeKind.INTEGER
    assert [op.opcode for op in fn.blocks[0].operations] == ['const', 'mul', 'add', 'move', 'return']


def test_undefined_name_is_rejected():
    with pytest.raises(OmniLoweringError):
        lower_source('fn main(a) { return missing; }')


def test_non_integer_arithmetic_is_rejected():
    with pytest.raises(OmniLoweringError):
        lower_source('fn main() { return "a" + "b"; }')
