import pytest

from omni.digital import DigitalSpec
from omni.digital_validate import DigitalSpecValidationError, validate_digital_spec


def test_valid_open_world_spec_passes():
    spec = DigitalSpec(kind="future.device", name="prototype", interfaces=("input",))
    assert validate_digital_spec(spec) is spec


def test_invalid_interface_is_rejected():
    spec = DigitalSpec(kind="future.device", name="prototype", interfaces=("",))
    with pytest.raises(DigitalSpecValidationError):
        validate_digital_spec(spec)
