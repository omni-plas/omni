from omni.target_model import TargetModel

def test_target_identity_and_capability():
    target=TargetModel('windows','x86_64','native','sysv','native',{'elf':True})
    assert target.identity=='windows:x86_64:native:sysv:native'
    assert target.supports('elf')
    assert not target.supports('unknown')
