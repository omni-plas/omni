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
