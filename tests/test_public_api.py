import omni


def test_public_api_exposes_core_pipeline():
    assert callable(omni.compile_semantics)
    assert callable(omni.validate_uir)
    assert callable(omni.lower_to_ir)
    assert callable(omni.optimize_module)
    assert callable(omni.resolve_target)
    assert omni.ValidationError.__mro__[1] is omni.OmniError


def test_public_api_exposes_os_packaging_and_installation_models():
    target = omni.TargetDescriptor("future-os", "future-cpu")
    os_spec = omni.OperatingSystemSpec("future-os", target, kernel="kernel")
    package = omni.PackageManifest("future-os", "1.0", target)
    installer = omni.plan_installation(target, artifact_format="future-package")

    assert os_spec.target == target
    assert package.target == target
    assert installer.kind.value == "package"
    assert omni.InstallerKind.BOOTABLE.value == "bootable"
