import pytest
from omni.native_target import NativeTarget
from omni.native_build_gate import preflight


def test_preflight_accepts_complete_manifest():
    assert preflight(NativeTarget('linux','x86_64','sysv'),{'entry':'main','sources':['main.omni']})


def test_preflight_rejects_missing_sources():
    with pytest.raises(ValueError):
        preflight(NativeTarget('linux','x86_64','sysv'),{'entry':'main'})
