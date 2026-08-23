from omni.cli import main


def test_cli_install_plan(capsys):
    assert main([
        "install-plan",
        "--target", "test-os",
        "--architecture", "test-cpu",
        "--abi", "test-abi",
        "--format", "test-installer",
        "--artifact", "app.bin",
    ]) == 0
    output = capsys.readouterr().out
    assert '"artifact_format": "test-installer"' in output
    assert '"target": "test-os/test-cpu/test-abi"' in output
