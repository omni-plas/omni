import pytest

from omni.errors import BackendError, CapabilityError, LoweringError, OmniError, ValidationError


@pytest.mark.parametrize("error", [ValidationError, LoweringError, BackendError, CapabilityError])
def test_public_errors_share_omni_base(error):
    assert issubclass(error, OmniError)
