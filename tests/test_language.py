import pytest

from omni.language import OmniKeyword, OmniProgram


def test_omni_is_parsed_by_its_own_language_core():
    program = OmniProgram.parse("entity Website")
    assert program.keywords() == (OmniKeyword.ENTITY,)
    assert program.identifiers() == ("entity", "Website")
    program.validate()


def test_empty_omni_source_is_rejected():
    with pytest.raises(ValueError):
        OmniProgram.parse("   ").validate()


def test_non_text_source_is_rejected():
    with pytest.raises(TypeError, match="text"):
        OmniProgram.parse(None)


def test_token_lookup_uses_source_spans():
    program = OmniProgram.parse("let answer")
    assert program.token_at(0).text == "let"
    assert program.token_at(4).text == "answer"
    with pytest.raises(IndexError):
        program.token_at(999)


def test_token_lookup_rejects_invalid_offset_type():
    program = OmniProgram.parse("entity App")
    with pytest.raises(TypeError, match="integer"):
        program.token_at("0")


def test_all_language_keywords_are_recognized():
    program = OmniProgram.parse("entity function return let")
    assert program.keywords() == (
        OmniKeyword.ENTITY,
        OmniKeyword.FUNCTION,
        OmniKeyword.RETURN,
        OmniKeyword.LET,
    )
