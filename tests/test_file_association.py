from omni.file_association import source_file_association

def test_oi_uses_official_omni_icon():
    association = source_file_association()
    assert association["extension"] == ".oi"
    assert association["language"] == "Omni"
    assert association["icon"] == "assets/branding/omni-logo.jpg"
