from omni.native_build_manifest import NativeBuildManifest


def test_manifest_is_deterministic_data():
    manifest=NativeBuildManifest('linux','x86_64','main',('a.omni','b.omni'),('main','helper'))
    assert manifest.as_dict()['target_arch']=='x86_64'
    assert manifest.as_dict()['source_units']==['a.omni','b.omni']
