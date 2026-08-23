from omni.native_build_driver import build_artifact
from omni.native_target import NativeTarget


def test_build_driver_runs_preflight_verification_and_identity():
    data=b'\x7fELF'+bytes([2,1])+b'\0'*58
    manifest={'entry':'main','sources':['main.omni'],'symbols':{'main':0},'entry_offset':0}
    result=build_artifact(lambda:data,NativeTarget('linux','x86_64','sysv'),manifest)
    assert result.artifact==data
    assert result.target.triple()=='x86_64-linux-sysv'
    assert len(result.identity.artifact)==64
