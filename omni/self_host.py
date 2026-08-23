"""Describe the bootstrap-to-self-hosting compiler transition."""
from __future__ import annotations
from dataclasses import dataclass
from .native_self_build import SelfBuildTarget

@dataclass(frozen=True)
class SelfHostPlan:
    bootstrap: SelfBuildTarget
    native_compiler_source: str
    stages: tuple[str,...]

def make_self_host_plan(target:SelfBuildTarget|None=None)->SelfHostPlan:
    target=target or SelfBuildTarget('compiler.omni','linux','x86_64',True)
    return SelfHostPlan(target,target.compiler_source,('bootstrap','native-compile','self-compile','replace-bootstrap'))
