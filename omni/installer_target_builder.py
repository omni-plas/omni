"""Build installer bundles while preserving explicit target semantics."""

from __future__ import annotations

import json
import zipfile
from io import BytesIO

from .installer_builder import InstallerBundle
from .installer import InstallationPlan
from .target_installers import InstallerTarget, resolve_installer_target


def build_target_installer(
    plan: InstallationPlan,
    package_payload: bytes,
    *,
    filename: str = "package.omni",
    target: InstallerTarget | None = None,
) -> InstallerBundle:
    """Build an Omni installer and embed the resolved target contract."""
    from .installer_builder import build_installer

    resolved = target or resolve_installer_target(plan.target)
    base = build_installer(plan, package_payload, filename=filename)
    source = BytesIO(base.payload)
    output = BytesIO()
    with zipfile.ZipFile(source, "r") as reader, zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as writer:
        for item in reader.infolist():
            payload = reader.read(item.filename)
            if item.filename == "install.json":
                document = json.loads(payload.decode("utf-8"))
                document["installer_format"] = resolved.format.value
                document["bootable"] = resolved.bootable
                payload = (json.dumps(document, sort_keys=True, separators=(",", ":")) + "\n").encode()
            writer.writestr(item.filename, payload)
    payload = output.getvalue()
    import hashlib
    return InstallerBundle(payload, hashlib.sha256(payload).hexdigest())
