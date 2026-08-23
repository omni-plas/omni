import pytest
from omni.native_memory_runtime import AllocationRequest, AllocationResult, MemoryRuntimeError, validate_result


def test_memory_result_validation():
    req = AllocationRequest(32, 16)
    validate_result(AllocationResult(0x1000, 32, 16), req)


def test_misaligned_result_is_rejected():
    with pytest.raises(MemoryRuntimeError):
        validate_result(AllocationResult(0x1008, 32, 16), AllocationRequest(32, 16))
