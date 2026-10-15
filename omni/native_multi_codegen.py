"""Multi-function x86-64 native emitter for the Omni bootstrap subset."""
from __future__ import annotations
import struct
from .ir import ModuleIR
from .native_codegen import NativeCodegenError, NativeExecutable
from .targets import TargetDescriptor
from .types import TypeKind

_BASE=0x400000; _PAGE=0x1000
_ARG_REGS=(7,6,2,1,8,9); _WORK_REGS=(3,5,10,11,12,13,14,15)
_CC={"eq":4,"ne":5,"lt":12,"le":14,"gt":15,"ge":13}

def _rex(w=1,r=0,b=0): return bytes([0x40|(w<<3)|(r<<2)|b])
def _mov_imm(reg,value): return _rex(b=(reg>>3)&1)+bytes([0xB8+(reg&7)])+struct.pack('<Q',value&0xffffffffffffffff)
def _mov_rr(dst,src): return _rex(r=(src>>3)&1,b=(dst>>3)&1)+b'\x89'+bytes([0xC0|((src&7)<<3)|(dst&7)])
def _rr(op,dst,src): return _rex(r=(src>>3)&1,b=(dst>>3)&1)+op+bytes([0xC0|((src&7)<<3)|(dst&7)])
def _call(d): return b'\xE8'+struct.pack('<i',d)
def _jmp(d): return b'\xE9'+struct.pack('<i',d)
def _jcc(cc,d): return b'\x0f'+bytes([0x80|cc])+struct.pack('<i',d)
def _test(reg): return _rex(b=(reg>>3)&1,r=(reg>>3)&1)+b'\x85'+bytes([0xC0|((reg&7)<<3)|(reg&7)])

def _compile_function(fn,known):
    if len(fn.parameters)>6: raise NativeCodegenError(f'too many parameters: {fn.name}')
    if not fn.blocks: raise NativeCodegenError(f'function has no blocks: {fn.name}')
    regs={name:reg for (name,typ),reg in zip(fn.parameters.items(),_ARG_REGS) if typ.kind==TypeKind.INTEGER}
    if len(regs)!=len(fn.parameters): raise NativeCodegenError(f'non-integer parameter: {fn.name}')
    free=iter(_WORK_REGS); code=bytearray(); call_fix=[]; jump_fix=[]; block_offsets={}; known_blocks={b.name for b in fn.blocks}; returned=False
    def get(name):
        if name not in regs: raise NativeCodegenError(f'undefined value: {name}')
        return regs[name]
    for block in fn.blocks:
        block_offsets[block.name]=len(code); terminated=False
        for op in block.operations:
            if terminated: raise NativeCodegenError(f'operation after terminator in {block.name}')
            if op.opcode=='const':
                value=op.attributes.get('value')
                if len(op.outputs)!=1 or not isinstance(value,int) or isinstance(value,bool): raise NativeCodegenError('integer const required')
                try: dst=next(free)
                except StopIteration as e: raise NativeCodegenError('register limit exceeded') from e
                regs[op.outputs[0]]=dst; code+=_mov_imm(dst,value)
            elif op.opcode in {'add','sub','mul','div'}:
                if len(op.inputs)!=2 or len(op.outputs)!=1: raise NativeCodegenError('binary operation arity')
                a,b=get(op.inputs[0]),get(op.inputs[1])
                if op.opcode=='div':
                    # idiv consumes RDX:RAX. Preserve any live value currently
                    # assigned to RDX before using it as the high dividend word.
                    rdx_names=[name for name,reg in regs.items() if reg==2 and name not in op.outputs]
                    if rdx_names:
                        try: saved=next(free)
                        except StopIteration as e: raise NativeCodegenError('register limit exceeded') from e
                        code+=_mov_rr(saved,2)
                        for name in rdx_names: regs[name]=saved
                        a,b=get(op.inputs[0]),get(op.inputs[1])
                    try: dst=next(free)
                    except StopIteration as e: raise NativeCodegenError('register limit exceeded') from e
                    code+=_mov_rr(0,a)+b'\x48\x99'+_rex(b=(b>>3)&1)+b'\xf7'+bytes([0xf8|(b&7)])+_mov_rr(dst,0)
                else:
                    try: dst=next(free)
                    except StopIteration as e: raise NativeCodegenError('register limit exceeded') from e
                    code+=_mov_rr(dst,a)+_rr({'add':b'\x01','sub':b'\x29','mul':b'\x0f\xaf'}[op.opcode],dst,b)
                regs[op.outputs[0]]=dst
            elif op.opcode=='move':
                if len(op.inputs)!=1 or len(op.outputs)!=1: raise NativeCodegenError('invalid move')
                output=op.outputs[0]
                if output in regs:
                    # Reassignment must update the existing location so a
                    # loop's back-edge observes the new value on each iteration.
                    dst=regs[output]
                else:
                    try: dst=next(free)
                    except StopIteration as e: raise NativeCodegenError('register limit exceeded') from e
                code+=_mov_rr(dst,get(op.inputs[0])); regs[output]=dst
            elif op.opcode=='compare':
                if len(op.inputs)!=2 or len(op.outputs)!=1: raise NativeCodegenError('compare arity')
                cc=_CC.get(op.attributes.get('operator'))
                if cc is None: raise NativeCodegenError(f"unsupported comparison: {op.attributes.get('operator')}")
                a,b=get(op.inputs[0]),get(op.inputs[1])
                try: dst=next(free)
                except StopIteration as e: raise NativeCodegenError('register limit exceeded') from e
                code+=_rr(b'\x39',a,b)+_mov_imm(dst,0)+_jcc({4:5,5:4,12:13,13:12,14:15,15:14}[cc],10)+_mov_imm(dst,1); regs[op.outputs[0]]=dst
            elif op.opcode in {'and','or'}:
                if len(op.inputs)!=2 or len(op.outputs)!=1: raise NativeCodegenError(f'{op.opcode} arity')
                a,b=get(op.inputs[0]),get(op.inputs[1])
                try: dst=next(free)
                except StopIteration as e: raise NativeCodegenError('register limit exceeded') from e
                code+=_mov_rr(dst,a)
                code+=_rr(b'\x21' if op.opcode=='and' else b'\x09',dst,b)
                regs[op.outputs[0]]=dst
            elif op.opcode=='not':
                if len(op.inputs)!=1 or len(op.outputs)!=1: raise NativeCodegenError('not arity')
                try: dst=next(free)
                except StopIteration as e: raise NativeCodegenError('register limit exceeded') from e
                code+=_mov_rr(dst,get(op.inputs[0]))+_test(dst)+_mov_imm(dst,0)+_jcc(4,10)+_mov_imm(dst,1); regs[op.outputs[0]]=dst
            elif op.opcode=='call':
                callee=op.attributes.get('callee')
                if callee not in known: raise NativeCodegenError(f'unknown callee: {callee}')
                if len(op.inputs)>6: raise NativeCodegenError('too many call arguments')
                for i,name in enumerate(op.inputs):
                    src=get(name)
                    if src!=_ARG_REGS[i]: code+=_mov_rr(_ARG_REGS[i],src)
                pos=len(code); code+=_call(0); call_fix.append((pos,callee))
                if len(op.outputs)!=1: raise NativeCodegenError('call requires one output')
                try: dst=next(free)
                except StopIteration as e: raise NativeCodegenError('register limit exceeded') from e
                code+=_mov_rr(dst,0); regs[op.outputs[0]]=dst
            elif op.opcode=='branch':
                if len(op.inputs)!=1: raise NativeCodegenError('branch requires one condition')
                t,f=op.attributes.get('true'),op.attributes.get('false')
                if t not in known_blocks or f not in known_blocks: raise NativeCodegenError('branch target not found')
                code+=_test(get(op.inputs[0])); pos=len(code); code+=_jcc(5,0); jump_fix.append((pos,t,6)); pos=len(code); code+=_jmp(0); jump_fix.append((pos,f,5)); terminated=True
            elif op.opcode=='jump':
                target=op.attributes.get('target')
                if target not in known_blocks: raise NativeCodegenError('jump target not found')
                pos=len(code); code+=_jmp(0); jump_fix.append((pos,target,5)); terminated=True
            elif op.opcode=='return':
                if len(op.inputs)>1: raise NativeCodegenError('invalid return')
                code+=_mov_rr(0,get(op.inputs[0])) if op.inputs else _mov_imm(0,0)
                code+=(_mov_rr(7,0)+_mov_imm(0,60)+b'\x0f\x05') if fn.name=='main' else b'\xc3'; terminated=True; returned=True
            else: raise NativeCodegenError(f'unsupported operation: {op.opcode}')
        if not terminated and block.successors:
            if len(block.successors)!=1: raise NativeCodegenError(f'block has multiple successors without branch: {block.name}')
            target=block.successors[0]
            pos=len(code); code+=_jmp(0); jump_fix.append((pos,target,5))
    if not returned: raise NativeCodegenError(f'function has no return: {fn.name}')
    return bytes(code),call_fix,jump_fix,block_offsets

def _elf(code,entry):
    total=120+len(code); eh=struct.pack('<16sHHIQQQIHHHHHH',b'\x7fELF\x02\x01\x01\x00'+b'\x00'*8,2,62,1,entry,64,0,0,64,56,1,0,0,0); ph=struct.pack('<IIQQQQQQ',1,7,0,_BASE,_BASE,total,total,_PAGE); return eh+ph+code

def emit_multi_x86_64_elf(module:ModuleIR,target:TargetDescriptor|None=None)->NativeExecutable:
    module.validate(); names=[f.name for f in module.functions]
    if len(set(names))!=len(names): raise NativeCodegenError('duplicate function name')
    if 'main' not in names: raise NativeCodegenError('native executable requires main')
    requested=target or TargetDescriptor('linux','x86_64','sysv',{'native-executable':True})
    if requested.platform not in {'linux','gnu-linux'} or requested.architecture not in {None,'x86_64','amd64'}: raise NativeCodegenError(f'unsupported target: {requested.identity()}')
    chunks=[]; function_offsets={}; call_fix=[]; jump_fix=[]; cursor=0; known=set(names)
    for fn in module.functions:
        function_offsets[fn.name]=cursor; chunk,calls,jumps,blocks=_compile_function(fn,known); chunks.append(chunk); call_fix.extend((cursor,p,c) for p,c in calls); jump_fix.extend((cursor,p,t,blocks) for p,t,_ in jumps); cursor+=len(chunk)
    code=bytearray(b''.join(chunks))
    for base,pos,callee in call_fix: code[base+pos:base+pos+5]=_call(function_offsets[callee]-(base+pos+5))
    for base,pos,target,blocks in jump_fix:
        is_jcc=code[base+pos:base+pos+2]==b'\x0f\x85'; size=6 if is_jcc else 5; rel=base+blocks[target]-(base+pos+size); code[base+pos:base+pos+size]=_jcc(5,rel) if is_jcc else _jmp(rel)
    return NativeExecutable(requested,_elf(bytes(code),_BASE+120+function_offsets['main']))
