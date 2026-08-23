"""Model the repeatable Omni self-hosting build sequence."""
from __future__ import annotations
from dataclasses import dataclass
from .native_self_build import SelfBuildTarget

@dataclass(frozen=True)
class SelfHostStep:
    name:str
    input_artifact:str
    output_artifact:str


def build_steps(target:SelfBuildTarget):
    return (
        SelfHostStep('bootstrap','bootstrap compiler',target.compiler_source+'.native'),
        SelfHostStep('compile-self',target.compiler_source+'.native','omni-self-hosted'),
        SelfHostStep('verify-self','omni-self-hosted','omni-self-hosted.verified'),
        SelfHostStep('promote','omni-self-hosted.verified','omni compiler'),
    )
