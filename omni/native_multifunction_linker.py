"""Link local function fragments and patch direct CALL rel32 references."""
from __future__ import annotations
from .multi_function_image import assemble_functions
from .native_call_patch import patch_call_rel32

def link(functions):
    image=assemble_functions(tuple((name,bytes(code)) for name,code,_ in functions))
    payload=bytearray(image.payload)
    offsets={f.name:f.offset for f in image.functions}
    for name,_,calls in functions:
        base=offsets[name]
        for call_offset,target in calls:
            if target not in offsets: raise KeyError(target)
            patch_call_rel32(payload,base+call_offset,offsets[target])
    return bytes(payload),offsets
