import json

from omni.omni_frontend import OmniFrontend


def test_omni_frontend_accepts_canonical_uir():
    document = {
        "version": "1",
        "entity": {"kind": "application", "name": "self"},
        "source": {"language": "omni", "version": "1"},
        "target": {"platform": "future-os", "capabilities": {"semantic-artifact": True}},
        "semantics": {"program": {"entry": "main"}},
    }
    uir = OmniFrontend().parse(json.dumps(document))
    assert uir.source["language"] == "omni"
    assert uir.entity_kind == "application"
