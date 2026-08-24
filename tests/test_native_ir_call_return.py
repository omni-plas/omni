from omni.ir import BasicBlock, FunctionIR, Operation
from omni.native_ir_linked_executable import compile_functions_to_native

def test_call_result_is_linked_through_rax():
    callee=FunctionIR('callee',blocks=(BasicBlock('entry',(Operation('const',outputs=('v',),attributes={'value':9}),Operation('return',inputs=('v',))),),))
    caller=FunctionIR('main',blocks=(BasicBlock('entry',(Operation('call',outputs=('r',),attributes={'function':'callee'}),Operation('return',inputs=('r',))),),))
    linked=compile_functions_to_native((caller,callee))
    assert linked.symbols['callee']>linked.symbols['main']
