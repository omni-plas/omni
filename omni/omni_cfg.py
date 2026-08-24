"""Build a validated CFG for structured Omni statements."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class CFGBlock:
    name:str
    statements:tuple
    successors:tuple[str,...]

def build_cfg(statements):
    blocks=[]; current=[]; index=0
    def flush(succ=()):
        nonlocal current,index
        if current:
            name=f'b{index}'; index+=1; blocks.append(CFGBlock(name,tuple(current),tuple(succ))); current=[]
    for stmt in statements:
        if getattr(stmt,'__class__',None).__name__=='If':
            flush((f'then{index}',f'else{index}'))
            idx=index; index+=2
            blocks.append(CFGBlock(f'then{idx}',tuple(stmt.then_body),()))
            blocks.append(CFGBlock(f'else{idx}',tuple(stmt.else_body),()))
        else: current.append(stmt)
    flush()
    return tuple(blocks)
