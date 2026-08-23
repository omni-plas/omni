from omni.native_artifact_verify import verify_artifact


def test_artifact_metadata_verification():
    blob=b'\x7fELF'+bytes([2,1])+b'\0'*58
    assert verify_artifact(blob,0,{'main':0},'main')
