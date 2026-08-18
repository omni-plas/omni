import pytest

from omni.language import OmniKeyword, OmniProgram


def test_omni_is_parsed_by_its_own_language_core():
    program = OmniProgram.parse("entity Website")
    assert program.keywords() == (OmniKeyword.ENTITY,)
    program.validate()


def test_empty_omni_source_is_rejected():
    with pytest.raises(ValueError):
        OmniProgram.parse("   ").validate()
