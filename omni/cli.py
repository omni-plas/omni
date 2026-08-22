"""Command-line entry point for Omni validation, execution, inspection, and emission."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .diagnostics import format_diagnostics
from .emitters import EmitterError, emit_c
from .errors import OmniError
from .installer import InstallerKind, plan_installation
from .lower import lower_to_ir
from .pipeline import compile_semantics
from .runtime import execute_module
from .serialization import loads_uir
from .targets import TargetDescriptor


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="omni", description="Omni semantic compiler and digital build tool")
    subparsers = parser.add_subparsers(dest="command", required=True)
    run = subparsers.add_parser("run", help="validate, lower, and execute a UIR JSON program")
    run.add_argument("source", type=Path)
    run.add_argument("--entry", default=None)
    run.add_argument("--args", default="{}", help="JSON object containing entry arguments")
    validate = subparsers.add_parser("validate", help="validate a UIR JSON program without executing it")
    validate.add_argument("source", type=Path)
    emit = subparsers.add_parser("emit-c", help="emit a UIR program as C99 source")
    emit.add_argument("source", type=Path)
    emit.add_argument("output", type=Path)
    install = subparsers.add_parser("install-plan", help="create a target-neutral installation plan")
    install.add_argument("--target", required=True, help="target platform identifier")
    install.add_argument("--architecture", default=None)
    install.add_argument("--abi", default=None)
    install.add_argument("--kind", choices=[kind.value for kind in InstallerKind], default=InstallerKind.PACKAGE.value)
    install.add_argument("--format", dest="artifact_format", required=True, help="installer artifact format")
    install.add_argument("--bootable", action="store_true")
    install.add_argument("--filesystem", default=None)
    install.add_argument("--manifest", action="store_true", help="emit the canonical installation manifest")
    return parser


def _load(path: Path) -> dict:
    return loads_uir(path.read_text(encoding="utf-8"))


def _installation_json(args: argparse.Namespace) -> str:
    target = TargetDescriptor(args.target, args.architecture, args.abi)
    plan = plan_installation(
        target,
        kind=InstallerKind(args.kind),
        artifact_format=args.artifact_format,
        bootable=args.bootable,
        filesystem=args.filesystem,
    )
    if args.manifest:
        return plan.render_manifest()
    return json.dumps(
        {
            "identity": plan.identity(),
            "target": plan.target.identity(),
            "kind": plan.kind.value,
            "artifact_format": plan.artifact_format,
            "bootable": plan.bootable,
            "filesystem": plan.filesystem,
            "artifacts": list(plan.artifacts),
        },
        ensure_ascii=False,
        sort_keys=True,
    )


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "install-plan":
            print(_installation_json(args), end="" if args.manifest else "\n")
            return 0
        document = _load(args.source)
        if args.command in {"validate", "run"}:
            result = compile_semantics(document)
            if not result.ok or result.ir is None:
                print(format_diagnostics(result.diagnostics), file=sys.stderr)
                return 2
            if args.command == "validate":
                print("valid")
                return 0
            entry = args.entry or document["semantics"]["program"]["entry"]
            values = json.loads(args.args)
            if not isinstance(values, dict):
                raise ValueError("--args must be a JSON object")
            print(json.dumps(execute_module(result.ir, entry, values), ensure_ascii=False))
            return 0
        if args.command == "emit-c":
            args.output.write_bytes(emit_c(lower_to_ir(document), TargetDescriptor("portable-c")))
            return 0
    except (OSError, ValueError, KeyError, EmitterError, OmniError, json.JSONDecodeError) as exc:
        print(f"omni: error: {exc}", file=sys.stderr)
        return 2
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
