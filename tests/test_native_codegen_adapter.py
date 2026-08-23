from omni.native_codegen_adapter import adapt_allocation
from omni.register_alloc import Allocation


def test_adapter_preserves_registers_and_spills():
    result = adapt_allocation(Allocation({"x": 3}, {"y": 0}, 8))
    assert result.registers == {"x": 3}
    assert result.spill_offsets == {"y": 0}
    assert result.stack_size == 16
