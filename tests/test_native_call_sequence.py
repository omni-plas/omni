from omni.native_call_sequence import build_call_sequence


def test_call_sequence_tracks_stack_arguments():
    seq=build_call_sequence('callee',(3,4,5,6,7,8,9))
    assert seq.target=='callee'
    assert seq.stack_argument_count==1
