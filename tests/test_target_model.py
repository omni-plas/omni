import pytest

from omni.target_model import TargetModel


def test_future_target_is_representable_without_catalog_entry():
    target = TargetModel(
        platform="future-os",
        architecture="future-cpu",
        runtime="future-runtime",
        abi="future-abi",
        execution_model="future-execution",
        capabilities={"threads": True},
    )
    assert target.identity == "future-os:future-cpu:future-runtime:future-abi:future-execution"
    assert target.supports("threads")


def test_target_identity_cannot_be_empty():
    with pytest.raises(ValueError):
        TargetModel(platform="")
