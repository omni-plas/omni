from omni.language_definition import LanguageDefinition, LanguageDefinitionError


def test_language_definition_has_open_world_identity_and_manifest():
    definition = LanguageDefinition(
        name="FutureLang",
        version="1.0",
        aliases=("future", "FL"),
        source_extensions=("fl", ".future"),
        syntax={"grammar": "defined-by-spec"},
        semantics={"evaluation": "specified"},
        type_rules={"typing": "specified"},
        execution_model={"model": "defined"},
        memory_model={"model": "defined"},
        abi_expectations={"calling_convention": "target-defined"},
        dependency_rules={"resolution": "omni"},
    )

    assert definition.identity == "FutureLang@1.0"
    assert definition.matches("future")
    assert definition.matches("FL", "1.0")
    assert not definition.matches("FL", "2.0")
    assert definition.matches_extension(".FL")
    assert definition.matches_extension("future")
    assert definition.manifest()["identity"] == definition.identity


def test_language_definition_rejects_missing_identity():
    for kwargs in ({"name": "", "version": "1"}, {"name": "X", "version": ""}):
        try:
            LanguageDefinition(**kwargs)
        except LanguageDefinitionError:
            pass
        else:
            raise AssertionError("incomplete language definition was accepted")
