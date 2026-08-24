"""Type-aware validation at the native lowering boundary."""
from __future__ import annotations
from .type_system import Type

SUPPORTED_INTEGER_BITS={1,8,16,32,64}

def validate_native_type(typ:Type):
    if getattr(typ,'kind',None) in ('integer','int'):
        bits=getattr(typ,'bits',64)
        if bits not in SUPPORTED_INTEGER_BITS: raise ValueError(f'unsupported integer width: {bits}')
        return True
    if str(typ) in ('void','Void'): return False
    raise ValueError(f'unsupported native type: {typ}')
