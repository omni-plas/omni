from omni.native_artifact_v2 import NativeArtifact


def test_artifact_verifies_elf():
    blob=b'\x7fELF'+bytes([2,1])+b'\0'*58
    artifact=NativeArtifact.from_elf(blob,0,{'main':0})
    assert artifact.verify()
    assert artifact.symbols['main']==0
