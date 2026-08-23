from omni.native_target import NativeTarget


def test_target_triple():
    assert NativeTarget('linux','x86_64','sysv').triple()=='x86_64-linux-sysv'
