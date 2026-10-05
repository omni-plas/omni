from pathlib import Path

from omni.cli import main
from omni.native_backend import read_artifact


def test_cli_validates_declarative_native_omni_source(tmp_path: Path, capsys):
    source = tmp_path / "hello.manifest"
    source.write_text(
        "entity = application\nname = hello\nplatform = test-os\narchitecture = test-cpu\nabi = test-abi\n",
        encoding="utf-8",
    )
    assert main(["validate", str(source), "--language", "omni"]) == 0
    assert '"name": "hello"' in capsys.readouterr().out


def test_cli_validates_and_builds_canonical_oi_source(tmp_path: Path, capsys):
    source = tmp_path / "hello.oi"
    source.write_text("fn main() { let answer = 40 + 2; return answer; }", encoding="utf-8")
    assert main(["validate", str(source)]) == 0
    assert '"extension": ".oi"' in capsys.readouterr().out

    output = tmp_path / "hello.omni-artifact"
    assert main(["build", str(source), "--output", str(output)]) == 0
    document = read_artifact(output.read_bytes())
    assert document["source"]["extension"] == ".oi"
    assert document["semantics"]["program"]["entry"] == "main"


def test_cli_compiles_canonical_oi_source_to_native_executable(tmp_path: Path):
    source = tmp_path / "hello.oi"
    source.write_text("fn main() { let answer = 40 + 2; return answer; }", encoding="utf-8")
    output = tmp_path / "hello"

    assert main(["native-exec", str(source), "--output", str(output)]) == 0
    payload = output.read_bytes()
    assert payload[:4] == b"\x7fELF"
    assert payload[4] == 2
    assert output.stat().st_mode & 0o111


def test_cli_canonicalizes_language_pack(tmp_path: Path, capsys):
    source = tmp_path / "future.json"
    source.write_text(
        '{"name":"FutureLang","version":"1","aliases":["future"],"source_extensions":[".fl"]}',
        encoding="utf-8",
    )
    assert main(["language-pack", str(source)]) == 0
    output = capsys.readouterr().out
    assert '"identity": "FutureLang@1"' in output
    assert '"source_extensions": [' in output


def test_cli_canonicalizes_target_pack(tmp_path: Path, capsys):
    source = tmp_path / "future-target.json"
    source.write_text(
        '{"schema":"omni.target.v1","platform":"FutureOS","architecture":"future-cpu","abi":"future-abi","capabilities":{"gui":true}}',
        encoding="utf-8",
    )
    assert main(["target-pack", str(source)]) == 0
    output = capsys.readouterr().out
    assert '"platform": "FutureOS"' in output
    assert '"architecture": "future-cpu"' in output
