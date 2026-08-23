import pytest

from omni.omni_compile import compile_omni_source
from omni.omni_runtime import OmniRuntimeError, execute_function


def test_runtime_executes_arithmetic():
    result = compile_omni_source('fn main(a, b) { let x = a + b * 2; return x; }')
    assert execute_function(result.module, 'main', (3, 4)) == 11


def test_runtime_rejects_wrong_arity():
    result = compile_omni_source('fn main(a) { return a; }')
    with pytest.raises(OmniRuntimeError):
        execute_function(result.module, 'main', ())


def test_runtime_rejects_division_by_zero():
    result = compile_omni_source('fn main() { let x = 1 / 0; return x; }')
    with pytest.raises(OmniRuntimeError):
        execute_function(result.module, 'main')
