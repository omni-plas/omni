from omni.cli import build_parser


def test_validate_accepts_unknown_language_identifier():
    args = build_parser().parse_args(["validate", "program.src", "--language", "future-language-2099"])
    assert args.language == "future-language-2099"


def test_native_exec_accepts_future_target_identifier():
    args = build_parser().parse_args([
        "native-exec", "program.json", "-o", "out.bin",
        "--target", "future-os-2099", "--architecture", "future-cpu-1",
    ])
    assert args.target == "future-os-2099"
    assert args.architecture == "future-cpu-1"
