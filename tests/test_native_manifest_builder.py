from omni.native_manifest_builder import manifest_for_functions
from omni.ir import FunctionIR


def test_manifest_from_functions():
    functions=(FunctionIR('main'),FunctionIR('helper'))
    m=manifest_for_functions(functions,entry='main')
    assert m.entry=='main'
    assert m.source_units==('main','helper')
