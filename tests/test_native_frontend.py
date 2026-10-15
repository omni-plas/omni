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
    uir = OmniNativeFrontend().parse(source, filename="hello.manifest")
    assert uir.entity["kind"] == "application"
    assert uir.entity["name"] == "hello"
    assert uir.target["platform"] == "test-os"
    assert uir.target["architecture"] == "test-cpu"


def test_canonical_oi_programming_syntax_becomes_uir():
    source = "fn main() { let answer = 40 + 2; return answer; }"
    uir = OmniNativeFrontend().parse(source, filename="hello.oi")
    assert uir.source["extension"] == ".oi"
    assert uir.target["platform"] == "semantic-artifact"
    assert uir.semantics["program"]["entry"] == "main"
    assert uir.semantics["functions"][0]["name"] == "main"
    assert [op["opcode"] for op in uir.semantics["functions"][0]["operations"]][-1] == "return"


def test_native_omni_source_reports_missing_fields():
    try:
        OmniNativeFrontend().parse("entity = application\nname = x", filename="bad.manifest")
    except ValueError as exc:
        assert "platform" in str(exc)
        assert "architecture" in str(exc)
        assert "abi" in str(exc)
    else:
        raise AssertionError("expected missing-field validation")
