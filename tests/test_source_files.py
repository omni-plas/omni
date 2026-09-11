from pathlib import Path

import pytest

from omni.source_files import OmniSourceFileError, is_omni_source_path, load_oi_source, require_omni_source_path


def test_only_oi_is_the_native_omni_source_extension():
    assert is_omni_source_path("program.oi")
    assert is_omni_source_path("PROGRAM.OI")
    assert not is_omni_source_path("program.py")
    assert not is_omni_source_path("program.omni")


def test_require_oi_rejects_other_extensions():
    assert require_omni_source_path("hello.oi") == Path("hello.oi")
    with pytest.raises(OmniSourceFileError):
        require_omni_source_path("hello.py")


def test_load_oi_source_reads_and_parses_native_source(tmp_path):
    source_path = tmp_path / "hello.oi"
    source_path.write_text("fn main() { let answer = 40 + 2; return answer; }", encoding="utf-8")

    program = load_oi_source(source_path)

    assert len(program.functions) == 1
    assert program.functions[0].name == "main"


def test_load_oi_source_rejects_missing_file(tmp_path):
    with pytest.raises(OmniSourceFileError):
        load_oi_source(tmp_path / "missing.oi")
