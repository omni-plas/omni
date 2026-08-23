import pytest

from omni.stack_model import StackModelError, layout_stack_slots


def test_stack_slots_are_aligned_and_frame_is_aligned():
    frame = layout_stack_slots([("a", 8, 8), ("b", 4, 4)])
    assert frame.offset_of("a") == 0
    assert frame.offset_of("b") == 8
    assert frame.size % 16 == 0


def test_duplicate_stack_slot_is_rejected():
    with pytest.raises(StackModelError):
        layout_stack_slots([("a", 8, 8), ("a", 8, 8)])
