from pathlib import Path

import pytest

from omni.entities import EntitySpec
from omni.fs_materializer import FilesystemMaterializationError, materialize_to_directory
from omni.materialize import MaterializedArtifact
from omni.targets import TargetDescriptor


def _artifact(name="program.bin"):
    target = TargetDescriptor("future-os", "future-cpu")
    entity = EntitySpec("binary", name, execution={"target": target.serialize().decode("utf-8") and target.document()})
    return MaterializedArtifact(entity, "bin", b"omni-artifact")


def test_materialize_writes_bytes_and_returns_manifest(tmp_path: Path):
    result = materialize_to_directory(_artifact(), tmp_path)
    assert result.path == tmp_path / "program.bin"
    assert result.path.read_bytes() == b"omni-artifact"
    assert result.manifest.size == len(b"omni-artifact")
    assert len(result.manifest.digest) == 64


def test_materialize_creates_nested_paths(tmp_path: Path):
    result = materialize_to_directory(_artifact("bin/program"), tmp_path)
    assert result.path == tmp_path / "bin" / "program"
    assert result.path.read_bytes() == b"omni-artifact"


def test_materialize_rejects_path_escape(tmp_path: Path):
    with pytest.raises(FilesystemMaterializationError, match="staging root"):
        materialize_to_directory(_artifact("../escape"), tmp_path)


def test_materialize_requires_target_contract(tmp_path: Path):
    entity = EntitySpec("binary", "program", execution={})
    with pytest.raises(FilesystemMaterializationError, match="target descriptor"):
        materialize_to_directory(MaterializedArtifact(entity, "bin", b"x"), tmp_path)


def test_materialize_does_not_execute_payload(tmp_path: Path):
    result = materialize_to_directory(_artifact("payload.bin"), tmp_path)
    assert result.path.exists()
    assert result.path.read_bytes() == b"omni-artifact"
