from omni.native_stage_runner import run_stage


def test_successful_stage():
    result=run_stage('parse',lambda:42)
    assert result.success and result.value==42


def test_failed_stage_is_structured():
    result=run_stage('link',lambda: (_ for _ in ()).throw(ValueError('missing symbol')))
    assert not result.success
    assert result.diagnostics[0].stage=='link'
