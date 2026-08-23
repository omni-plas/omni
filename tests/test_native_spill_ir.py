from omni.native_spill_ir import materialize_locations, reload, spill
from omni.native_value_locations import ResolvedValue


def test_spilled_value_materializes_and_reloads():
    value=ResolvedValue("x",None,-8)
    materialized=materialize_locations((value,),11)[0]
    assert materialized.register == 11
    assert reload(materialized)
    assert spill(materialized)
