"""Model x86-64 stack-frame layout for native calls."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class StackFrame:
    local_size:int
    outgoing_size:int
    saved_size:int
    alignment:int=16

    @property
    def size(self)->int:
        raw=self.local_size+self.outgoing_size+self.saved_size
        return (raw+self.alignment-1)//self.alignment*self.alignment

def make_frame(local_size=0,outgoing_size=0,saved_size=0,alignment=16):
    if min(local_size,outgoing_size,saved_size)<0: raise ValueError('frame sizes must be non-negative')
    if alignment<=0 or alignment&(alignment-1): raise ValueError('alignment must be a power of two')
    return StackFrame(local_size,outgoing_size,saved_size,alignment)
