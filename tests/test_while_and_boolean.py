from omni.omni_lowering import lower_source
from omni.runtime import execute


def test_while_loop_executes_and_mutates_local():
    module = lower_source('fn main() { let x = 0; while (x < 5) { x = x + 1; } return x; }')
    assert execute(module.functions[0]) == 5


def test_boolean_logic_executes():
    module = lower_source('fn main() { if ((1 < 2) && !(2 < 1)) { return 7; } else { return 3; } }')
    assert execute(module.functions[0]) == 7
