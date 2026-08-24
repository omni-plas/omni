from omni.ir import BasicBlock, FunctionIR, Operation
from omni.native_ir_linked_executable import compile_functions_to_elf, compile_functions_to_native

def test_multi_function_native_linking():
    callee=FunctionIR('callee',blocks=(BasicBlock('entry',(Operation('const',outputs=('v',),attributes={'value':7}),Operation('return',inputs=('v',))),),))
    caller=FunctionIR('main',blocks=(BasicBlock('entry',(Operation('call',attributes={'function':'callee'}),Operation('const',outputs=('v',),attributes={'value':0}),Operation('return',inputs=('v',))),),))
    linked=compile_functions_to_native((caller,callee))
    assert linked.symbols['main']==0
    assert linked.symbols['callee']>0
    elf=compile_functions_to_elf((caller,callee))
    assert elf[:4]==b'\x7fELF'
