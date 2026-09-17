from omni.source_compiler import compile_source, default_compiler_registry, resolve_source
from omni.registry import CompilerRegistry, RegistryError
from omni.frontends import SourceUnit
from omni.uir import UIR


class EchoFrontend:
    language = "FutureLang"

    def lower(self, source: SourceUnit) -> UIR:
        assert source.language == "FutureLang"
        return UIR.from_dict({
            "version": "0.1",
            "entity": {"kind": "program", "name": source.origin or "future"},
            "source": {"language": "FutureLang", "version": "1", "extension": ".fl"},
            "target": {"platform": "semantic-artifact", "architecture": None, "abi": None, "capabilities": {}},
            "semantics": {
                "program": {"entry": "main"}, "types": {}, "functions": [],
                "control_flow": {}, "data_flow": {}, "memory_model": {},
                "error_handling": {}, "io": {}, "dependencies": [],
                "security": {}, "performance": {},
            },
        })


def test_default_registry_resolves_canonical_oi():
    resolved = resolve_source("fn main() { return 42; }", origin="hello.oi")
    assert resolved.definition.identity == "Omni@1"
    assert resolved.frontend.language == "omni"


def test_source_compiler_lowers_native_oi_into_semantic_pipeline():
    result = compile_source("fn main() { let answer = 40 + 2; return answer; }", origin="hello.oi")
    assert result.ok
    assert result.ir is not None
    assert result.ir.functions[0].name == "main"


def test_custom_language_can_be_resolved_without_changing_pipeline():
    registry = CompilerRegistry()
    from omni.language_definition import LanguageDefinition
    definition = LanguageDefinition(name="FutureLang", version="1", source_extensions=(".fl",))
    registry.register_language_definition(definition)
    frontend = EchoFrontend()
    registry.register_frontend("FutureLang", frontend)
    resolved = resolve_source("future source", origin="example.fl", registry=registry)
    assert resolved.definition is definition
    assert resolved.frontend is frontend


def test_auto_resolution_requires_origin():
    try:
        resolve_source("fn main() { return 1; }")
    except RegistryError as exc:
        assert "origin" in str(exc)
    else:
        raise AssertionError("expected automatic-resolution error")
