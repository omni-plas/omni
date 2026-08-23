from omni.self_build_contract import CORE_COMPONENTS, validate_self_build_requirements


def test_core_self_build_components_are_complete():
    validate_self_build_requirements(CORE_COMPONENTS)
    assert len(CORE_COMPONENTS) >= 8
