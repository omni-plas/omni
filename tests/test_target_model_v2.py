from omni.target_model_v2 import TargetModel


def test_target_identity_and_features():
    target = TargetModel("future-os", "future-cpu", "future-abi", "future-exe", frozenset({"memory"}))
    assert target.identity() == "future-os/future-cpu/future-abi/future-exe"
    assert target.supports("memory")
