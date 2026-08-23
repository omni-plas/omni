"""Place native global data after code and expose image-relative addresses."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class GlobalData:
    name: str
    data: bytes
    alignment: int = 1

@dataclass(frozen=True)
class DataImage:
    data: bytes
    offsets: dict[str,int]

def align_up(value:int, alignment:int)->int:
    if alignment <= 0 or alignment & (alignment-1):
        raise ValueError("alignment must be a positive power of two")
    return (value + alignment - 1) & ~(alignment - 1)

def place_data(globals_, start_offset:int):
    cursor=start_offset
    chunks=[]
    offsets={}
    for item in globals_:
        cursor=align_up(cursor,item.alignment)
        offsets[item.name]=cursor
        pad=cursor-(start_offset+sum(len(x) for x in chunks))
        if pad>0: chunks.append(b"\0"*pad)
        chunks.append(bytes(item.data)); cursor += len(item.data)
    return DataImage(b"".join(chunks),offsets)
