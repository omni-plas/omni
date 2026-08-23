"""Small OS-facing runtime primitives for generated native code."""
from __future__ import annotations
from .native_syscalls import syscall6

SYS_EXIT=60
SYS_WRITE=1

def emit_exit(status_register:int=0)->bytes:
    return syscall6(SYS_EXIT,(status_register,))

def emit_write(fd_register:int, buffer_register:int, length_register:int)->bytes:
    return syscall6(SYS_WRITE,(fd_register,buffer_register,length_register))
