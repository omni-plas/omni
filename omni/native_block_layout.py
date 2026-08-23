"""Lay out native basic blocks and resolve local labels."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class BlockSpan:
    name: str
    start: int
    end: int

@dataclass(frozen=True)
class NativeLayout:
    spans: tuple[BlockSpan, ...]
    labels: dict[str, int]
    code: bytes

def layout_blocks(blocks, encoded):
    if len(blocks) != len(encoded):
        raise ValueError("block/encoding count mismatch")
    offset=0
    spans=[]
    labels={}
    chunks=[]
    for block,code in zip(blocks,encoded):
        labels[block.name]=offset
        chunks.append(code)
        end=offset+len(code)
        spans.append(BlockSpan(block.name,offset,end))
        offset=end
    return NativeLayout(tuple(spans),labels,b"".join(chunks))
