"""Open-world boot contract primitives for Omni OS targets."""
from __future__ import annotations

from dataclasses import dataclass

from .os_image import OSImageError
from .targets import TargetDescriptor


@dataclass(frozen=True)
class BootContract:
    target: TargetDescriptor
    boot_protocol: str
    firmware: str
    filesystem: str
    entrypoint: str

    def validate(self) -> None:
        values = {
            "boot_protocol": self.boot_protocol,
            "firmware": self.firmware,
            "filesystem": self.filesystem,
            "entrypoint": self.entrypoint,
        }
        for name, value in values.items():
            if not isinstance(value, str) or not value.strip():
                raise OSImageError(f"boot contract {name} cannot be empty")


def require_boot_capabilities(target: TargetDescriptor, contract: BootContract) -> None:
    if contract.target != target:
        raise OSImageError("boot contract target does not match requested target")
    contract.validate()
    target.require("boot_protocol", contract.boot_protocol)
    target.require("firmware", contract.firmware)
    target.require("filesystem", contract.filesystem)
