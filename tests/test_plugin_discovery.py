import pytest

from omni.language_definition import LanguageDefinition
from omni.plugin_discovery import discover_plugins
from omni.registry import CompilerRegistry


def test_plugin_discovery_is_deterministic_when_no_plugins_are_installed():
    report = discover_plugins(CompilerRegistry(), groups=())
    assert report.loaded == ()
    assert report.skipped == ()
    assert report.errors == ()


def test_plugin_discovery_strict_mode_rejects_unknown_groups():
    with pytest.raises(ValueError, match="unsupported plugin group"):
        discover_plugins(CompilerRegistry(), strict=True, groups=("omni.unknown",))


def test_plugin_discovery_module_exposes_language_group_contract():
    definition = LanguageDefinition(name="ExampleLang", version="1", source_extensions=(".ex",))
    assert definition.identity == "ExampleLang@1"
