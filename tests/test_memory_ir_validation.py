import pytest
from omni.memory_ir import MemoryIROperationError, alloc


def test_alloc_rejects_non_power_of_two_alignment():
    with pytest.raises(MemoryIROperationError):
        alloc("p", "n", alignment=3)


def test_alloc_accepts_power_of_two_alignment():
    operation = alloc("p", "n", alignment=16)
    assert operation.attributes["alignment"] == 16
