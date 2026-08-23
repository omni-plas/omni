import pytest

from omni.memory_ir import MemoryIROperationError, alloc, free, load, ptr_add, store


def test_memory_ops_have_stable_opcodes_and_operands():
    assert alloc("p", "n").opcode == "alloc"
    assert load("v", "p", size=4).inputs == ("p",)
    assert store("p", "v", size=8).inputs == ("p", "v")
    assert ptr_add("q", "p", "n").inputs == ("p", "n")
    assert free("p").inputs == ("p",)


def test_memory_sizes_are_validated():
    with pytest.raises(MemoryIROperationError):
        load("v", "p", size=3)
    with pytest.raises(MemoryIROperationError):
        store("p", "v", size=16)
