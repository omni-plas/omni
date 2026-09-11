import json

from omni.oi_registration import registration_for, render_registration_manifest


def test_known_platforms_keep_the_same_colored_oi_identity():
    windows = registration_for("Windows")
    macos = registration_for("Darwin")
    linux = registration_for("Linux")

    assert windows.extension == macos.extension == linux.extension == ".oi"
    assert windows.icon_color == macos.icon_color == linux.icon_color == "color"
    assert windows.icon_asset == macos.icon_asset == linux.icon_asset
    assert windows.native_icon_format == "ico"
    assert macos.native_icon_format == "icns"
    assert linux.native_icon_format == "svg-or-png"


def test_manifest_is_deterministic_and_future_platform_safe():
    first = render_registration_manifest()
    second = render_registration_manifest()
    assert first == second

    document = json.loads(first)
    assert document["extension"] == ".oi"
    assert document["icon"]["color"] == "color"
    assert {item["platform"] for item in document["registrations"]} == {
        "windows", "macos", "freedesktop", "generic"
    }
