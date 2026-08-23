from omni.native_spill import plan_spills, stack_offset_from_rbp
from omni.register_alloc import Allocation


def test_spill_plan_aligns_frame_and_orders_slots():
    allocation = Allocation({"a": 3}, {"b": 8, "c": 0}, 16)
    plan = plan_spills(allocation)
    assert plan.stack_size == 16
    assert [action.value for action in plan.actions] == ["c", "b"]


def test_rbp_offsets_are_negative_slots():
    assert stack_offset_from_rbp(0) == -8
    assert stack_offset_from_rbp(8) == -16
