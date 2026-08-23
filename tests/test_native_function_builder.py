from omni.native_function_builder import build_function_ir
from omni.native_ir import FunctionIR


def test_function_ir_build_driver_reaches_artifact():
    fn=FunctionIR('main',(),())
    result=build_function_ir((fn,),entry='main')
    assert result.identity.entry=='main'
    assert result.target.arch=='x86_64'
    assert result.identity.artifact
