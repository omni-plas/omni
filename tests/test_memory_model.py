import pytest

from omni.memory_model import Memory, MemoryModelError


def test_allocate_store_and_load_integer():
    memory = Memory()
    obj = memory.allocate(16)
    memory.store(obj.address, 0x12345678, 4)
    assert memory.load(obj.address, 4) == 0x12345678


def test_memory_access_is_bounds_checked():
    memory = Memory()
    obj = memory.allocate(4)
    with pytest.raises(MemoryModelError):
        memory.load(obj.address + 3, 2)


def test_byte_round_trip():
    memory = Memory()
    obj = memory.allocate(8)
    payload = b"Omni!"
    memory.write_bytes(obj.address, payload)
    assert memory.read_bytes(obj.address, len(payload)) == payload
