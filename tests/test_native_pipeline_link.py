from omni.native_pipeline import compile_function_module
from omni.ir import FunctionIR


def test_function_module_pipeline_produces_elf():
    result=compile_function_module((FunctionIR('main'),), entry='main')
    assert result.executable[:4]==b'\x7fELF'
    assert result.symbols=={'main':0}
