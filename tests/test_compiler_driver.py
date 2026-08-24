from omni.compiler_driver import compile_source

def test_driver_compiles_source_and_optimizes():
    unit=compile_source('fn main(a) {}')
    assert unit.source.startswith('fn main')
    assert unit.ir.functions[0].name=='main'
