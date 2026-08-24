from omni.pipeline_contract import Stage, StageResult

class Echo(Stage[str,str]):
    name='echo'
    def run(self,value): return StageResult(value)

def test_stage_contract():
    result=Echo().run('omni')
    assert result.value=='omni'
    assert result.diagnostics==()
