from omni.targets import TargetDescriptor


def test_target_descriptor_supports_open_world_targets():
    target = TargetDescriptor(
        platform="future-os",
        architecture="future-cpu",
        abi="future-abi",
        capabilities={"graphics": "next-gen"},
    )
    assert target.identity() == "future-os-future-cpu-future-abi"
    assert target.capabilities["graphics"] == "next-gen"
