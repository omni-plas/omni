from omni.omni_bootstrap import build_bootstrap


def test_bootstrap_builds_native_artifact():
    artifact = build_bootstrap('fn main() { return 7; }')
    assert artifact.target.identity() == 'linux-x86_64-sysv'
    assert artifact.executable.payload[:4] == b'\x7fELF'
