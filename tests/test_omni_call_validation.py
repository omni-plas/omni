import pytest

from omni.omni_lowering import OmniLoweringError, lower_source


def test_unknown_function_is_rejected_during_lowering():
    with pytest.raises(OmniLoweringError, match='undefined function'):
        lower_source('fn main() { return missing(1); }')


def test_call_arity_is_checked_during_lowering():
    with pytest.raises(OmniLoweringError, match='expects 1 arguments'):
        lower_source('fn inc(x) { return x + 1; } fn main() { return inc(1, 2); }')
