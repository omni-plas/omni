from omni.omni_lowering import lower_source
from omni.runtime import execute


def test_runtime_executes_true_if_branch():
    fn = lower_source('fn main(x) { if (x > 10) { return 1; } else { return 0; } }').functions[0]
    assert execute(fn, {'x': 11}) == 1


def test_runtime_executes_false_if_branch():
    fn = lower_source('fn main(x) { if (x > 10) { return 1; } else { return 0; } }').functions[0]
    assert execute(fn, {'x': 10}) == 0
