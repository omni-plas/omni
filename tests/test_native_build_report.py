from omni.native_build_driver import build_artifact
from omni.native_build_report import build_report
from omni.native_target import NativeTarget


def test_build_report_contains_identity():
    data=b'\x7fELF'+bytes([2,1])+b'\0'*58
    m={'entry':'main','sources':['main.omni'],'symbols':{'main':0},'entry_offset':0}
    r=build_artifact(lambda:data,NativeTarget('linux','x86_64','sysv'),m)
    report=build_report(r)
    assert report['target']=='x86_64-linux-sysv'
    assert report['artifact_size']==64
    assert len(report['artifact_sha256'])==64
