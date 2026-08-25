from omni.oi_file_icon import OI_ICON_ASSET, OI_ICON_COLOR_MODE, oi_file_icon_policy


def test_every_oi_file_uses_the_canonical_colored_logo():
    policy = oi_file_icon_policy()
    manifest = policy.file_icon_manifest()

    assert policy.extension == ".oi"
    assert manifest["extension"] == ".oi"
    assert manifest["icon_asset"] == str(OI_ICON_ASSET)
    assert manifest["color_mode"] == OI_ICON_COLOR_MODE == "color"
    assert manifest["apply_to"] == "every .oi file created or registered by Omni"


def test_native_formats_are_selected_per_platform_without_changing_the_logo():
    policy = oi_file_icon_policy()

    assert policy.platform_registration("Windows")["native_icon_format"] == "ico"
    assert policy.platform_registration("Darwin")["native_icon_format"] == "icns"
    assert policy.platform_registration("Linux")["native_icon_format"] == "svg-or-png"
    assert policy.platform_registration("FutureOS")["native_icon_format"] == "native"

    for system in ("Windows", "Darwin", "Linux", "FutureOS"):
        registration = policy.platform_registration(system)
        assert registration["icon_asset"] == str(OI_ICON_ASSET)
        assert registration["icon_color"] == "color"
