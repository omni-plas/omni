from omni.native_artifact_record import ArtifactRecord


def test_record_contains_content_identity():
    record=ArtifactRecord.create(b'omni','linux','x86_64','main')
    assert record.size==4
    assert len(record.digest)==64
    assert record.entry=='main'
