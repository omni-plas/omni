from omni.native_frontend import OmniNativeFrontend


def test_native_omni_source_becomes_uir():
    source = """
    entity = application
    name = hello
    platform = test-os
    architecture = test-cpu
    abi = test-abi
    entry = main
    """
    uir = OmniNativeFrontend().parse(source, filename="hello.omni")
    assert uir.entity["kind"] == "application"
    assert uir.entity["name"] == "hello"
    assert uir.target.platform == "test-os"
    assert uir.target.architecture == "test-cpu"


def test_native_omni_source_reports_missing_fields():
    try:
        OmniNativeFrontend().parse("entity = application\nname = x", filename="bad.omni")
    except ValueError as exc:
        assert "platform" in str(exc)
        assert "architecture" in str(exc)
        assert "abi" in str(exc)
    else:
        raise AssertionError("expected missing-field validation")
