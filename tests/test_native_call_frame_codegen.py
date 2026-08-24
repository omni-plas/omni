from omni.native_call_frame_codegen import plan_call_frame

def test_call_frame_for_register_arguments():
    frame=plan_call_frame(2)
    assert frame.stack_bytes==0

def test_call_frame_accounts_for_stack_arguments():
    frame=plan_call_frame(8)
    assert frame.stack_bytes==16
