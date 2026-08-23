import pytest

from omni.omni_compile import compile_omni_source
from omni.omni_multi_runtime import OmniRuntimeError, execute_function


def test_runtime_executes_function_calls():
    result = compile_omni_source('fn double(x) { return x * 2; } fn main() { return double(21); }')
    assert execute_function(result.module, 'main') == 42


def test_runtime_supports_nested_calls():
    result = compile_omni_source('fn inc(x) { return x + 1; } fn twice(x) { return inc(inc(x)); } fn main() { return twice(40); }')
    assert execute_function(result.module, 'main') == 42


def test_runtime_rejects_unknown_callee():
    result = compile_omni_source('fn main() { return missing(1); }')
    with pytest.raises(OmniRuntimeError):
        execute_function(result.module, 'main')
