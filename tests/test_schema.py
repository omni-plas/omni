from omni.schema import REQUIRED_ROOT_FIELDS, REQUIRED_SEMANTIC_FIELDS, schema_summary


def test_schema_summary_matches_contract():
    schema = schema_summary()
    assert schema["root"] == REQUIRED_ROOT_FIELDS
    assert "semantics" in schema["root"]
    assert "memory_model" in schema["semantics"]
    assert "security" in schema["semantics"]


def test_required_fields_are_stable_and_nonempty():
    assert REQUIRED_ROOT_FIELDS
    assert REQUIRED_SEMANTIC_FIELDS
    assert len(set(REQUIRED_ROOT_FIELDS)) == len(REQUIRED_ROOT_FIELDS)
    assert len(set(REQUIRED_SEMANTIC_FIELDS)) == len(REQUIRED_SEMANTIC_FIELDS)
