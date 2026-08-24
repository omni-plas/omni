"""Build a validated CFG for structured Omni statements."""
from __future__ import annotations
from dataclasses import dataclass
from .omni_statements import If
from .omni_loop import While

@dataclass(frozen=True)
class CFGBlock:
    name: str
    statements: tuple
    successors: tuple[str,...]


def build_cfg(statements):
    blocks=[]
    counter=[0]

    def fresh(prefix='b'):
        name=f'{prefix}{counter[0]}'; counter[0]+=1; return name

    def sequence(items, fallthrough=None):
        current=[]
        for stmt in items:
            if isinstance(stmt,If):
                if current:
                    name=fresh(); blocks.append(CFGBlock(name,tuple(current),()))
                    current=[]
                then_name=fresh('then'); else_name=fresh('else'); join_name=fresh('join')
                blocks.append(CFGBlock(f'cond{counter[0]}',(stmt,), (then_name,else_name)))
                then_blocks=sequence(stmt.then_body,join_name)
                else_blocks=sequence(stmt.else_body,join_name)
                if then_blocks and then_blocks[-1].successors==():
                    last=then_blocks[-1]; blocks[blocks.index(last)]=CFGBlock(last.name,last.statements,(join_name,))
                if else_blocks and else_blocks[-1].successors==():
                    last=else_blocks[-1]; blocks[blocks.index(last)]=CFGBlock(last.name,last.statements,(join_name,))
                blocks.append(CFGBlock(join_name,(),()))
            elif isinstance(stmt,While):
                if current:
                    name=fresh(); blocks.append(CFGBlock(name,tuple(current),()))
                    current=[]
                cond_name=fresh('while_cond'); body_name=fresh('while_body'); exit_name=fresh('while_exit')
                blocks.append(CFGBlock(cond_name,(stmt.condition,),(body_name,exit_name)))
                body_blocks=sequence(stmt.body,cond_name)
                if body_blocks and body_blocks[-1].successors==():
                    last=body_blocks[-1]; blocks[blocks.index(last)]=CFGBlock(last.name,last.statements,(cond_name,))
                blocks.append(CFGBlock(exit_name,(),()))
            else:
                current.append(stmt)
        if current:
            name=fresh(); successors=() if fallthrough is None else (fallthrough,)
            block=CFGBlock(name,tuple(current),successors); blocks.append(block); return (block,)
        return tuple(b for b in blocks if b.name.startswith(('then','else','while_body')))

    sequence(tuple(statements))
    return tuple(blocks)
