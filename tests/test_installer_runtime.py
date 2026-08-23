from omni.installer import InstallerKind, plan_installation
from omni.installer_builder import build_installer
from omni.installer_runtime import extract_installer, inspect_installer
from omni.targets import TargetDescriptor


def test_installer_runtime_round_trip(tmp_path):
    target = TargetDescriptor("linux", "x86_64", "sysv")
    plan = plan_installation(target, kind=InstallerKind.PACKAGE, artifact_format="omni-package", artifacts=("app",))
    bundle = build_installer(plan, b"payload", filename="app.omni")
    info = inspect_installer(bundle.payload)
    assert info["package_digest"] == bundle.digest[:0] + __import__("hashlib").sha256(b"payload").hexdigest()
    path = extract_installer(bundle.payload, tmp_path, plan=plan)
    assert path.read_bytes() == b"payload"
