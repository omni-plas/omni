from omni.native_artifact import compile_native_artifact


def test_native_artifact_is_reproducible():
    source = """entity = application
name = hello
platform = semantic-artifact
architecture = universal
abi = universal
entry = main
"""
    first = compile_native_artifact(source)
    second = compile_native_artifact(source)
    assert first.payload == second.payload
    assert first.digest == second.digest
    assert len(first.digest) == 64
