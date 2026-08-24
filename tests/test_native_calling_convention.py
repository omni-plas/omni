from omni.native_calling_convention import ARG_REGISTERS, RETURN_REGISTER, assign_arguments

def test_first_arguments_use_registers():
    regs,stack=assign_arguments(8)
    assert regs==ARG_REGISTERS
    assert stack==2
    assert RETURN_REGISTER==0
