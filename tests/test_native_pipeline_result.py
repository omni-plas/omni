from omni.native_pipeline_result import PipelineResult
from omni.native_build_diagnostics import error


def test_pipeline_result_ok():
    result=PipelineResult.ok(7)
    assert result.success and result.value==7


def test_pipeline_result_failure():
    result=PipelineResult.failure(error('emit','E_EMIT','bad'))
    assert not result.success and result.diagnostics[0].code=='E_EMIT'
