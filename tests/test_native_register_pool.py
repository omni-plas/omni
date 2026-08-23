import pytest
from omni.native_register_pool import RegisterPool


def test_pool_acquire_release_is_deterministic():
    pool = RegisterPool((3, 4, 5))
    assert pool.acquire() == 3
    assert pool.acquire() == 4
    pool.release(3)
    assert pool.acquire() == 3


def test_pool_rejects_exhaustion():
    pool = RegisterPool((3,))
    pool.acquire()
    with pytest.raises(RuntimeError):
        pool.acquire()
