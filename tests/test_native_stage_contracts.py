from omni.native_stage_contracts import success, failure


def test_success_stage_result():
    result=success('link',b'code')
    assert result.ok()
    assert result.output==b'code'


def test_failure_stage_result():
    result=failure('link','unresolved symbol')
    assert not result.ok()
    assert result.diagnostics==('unresolved symbol',)
