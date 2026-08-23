from pathlib import Path

from omni.cli import main


def test_cli_validates_native_omni_source(tmp_path: Path, capsys):
    source = tmp_path / "hello.omni"
    source.write_text(
        "entity = application\nname = hello\nplatform = test-os\narchitecture = test-cpu\nabi = test-abi\n",
        encoding="utf-8",
    )
    assert main(["validate", str(source), "--language", "omni"]) == 0
    assert '"name": "hello"' in capsys.readouterr().out
