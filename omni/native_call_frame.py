"""Plan stack cleanup around outgoing calls."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class CallFrame:
    stack_argument_bytes:int
    alignment_padding:int
    cleanup_bytes:int = 0

    @property
    def stack_bytes(self) -> int:
        return self.stack_argument_bytes + self.alignment_padding

def plan_call_frame(stack_argument_count:int, current_alignment:int=0)->CallFrame:
    if stack_argument_count<0: raise ValueError('negative argument count')
    raw=stack_argument_count*8
    padding=(16-((current_alignment+raw)%16))%16
    return CallFrame(raw,padding,raw+padding)
