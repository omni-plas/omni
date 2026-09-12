import json

import pytest

from omni.target_pack import TargetPackError, dump_target_pack, load_target_pack, target_from_mapping
from omni.targets import TargetDescriptor


def test_target_pack_round_trip(tmp_path):
    target = TargetDescriptor("FutureOS", "future-cpu", "future-abi", {"gui": True, "native-executable": True})
    path = tmp_path / "future-target.json"
    dump_target_pack(target, path)
    assert load_target_pack(path) == target
    assert json.loads(path.read_text(encoding="utf-8"))["platform"] == "FutureOS"


def test_target_pack_rejects_missing_platform():
    with pytest.raises(TargetPackError):
        target_from_mapping({"architecture": "x86_64"})
