from omni.native_stack_args import place_stack_arguments


def test_outgoing_frame_is_aligned():
    frame=place_stack_arguments((3,4,5),alignment=16)
    assert frame.size % 16 == 0
    assert [a.source_register for a in frame.arguments] == [5,4,3]
