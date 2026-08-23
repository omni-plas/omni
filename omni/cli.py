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
from .installer_apply import apply_installer
from .installer_runtime import extract_installer, inspect_installer
from .lower import lower_to_ir
from .native_artifact import compile_native_artifact
from .native_executable import compile_native_executable, write_native_executable
from .native_frontend import OmniNativeFrontend
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
    validate = subparsers.add_parser("validate", help="validate a source program")
    validate.add_argument("source", type=Path)
    validate.add_argument("--language", default="uir-json", choices=("uir-json", "omni"))
    build = subparsers.add_parser("build", help="build native Omni source into a portable artifact")
    build.add_argument("source", type=Path)
    build.add_argument("-o", "--output", type=Path, required=True)
    native_exec = subparsers.add_parser("native-exec", help="compile a UIR JSON program to a self-contained x86-64 ELF executable")
    native_exec.add_argument("source", type=Path)
    native_exec.add_argument("-o", "--output", type=Path, required=True)
    native_exec.add_argument("--target", default="linux", choices=("linux", "gnu-linux"))
    native_exec.add_argument("--architecture", default="x86_64", choices=("x86_64", "amd64"))
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
    install.add_argument("--artifact", action="append", default=[], help="artifact path; may be repeated")
    install.add_argument("--metadata", action="append", default=[], metavar="KEY=VALUE", help="installer metadata; may be repeated")
    install.add_argument("--manifest", action="store_true", help="emit the canonical installation manifest")
    inspect = subparsers.add_parser("installer-inspect", help="validate and inspect an Omni installer bundle")
    inspect.add_argument("installer", type=Path)
    extract = subparsers.add_parser("installer-extract", help="safely extract the verified package from an Omni installer")
    extract.add_argument("installer", type=Path)
    extract.add_argument("destination", type=Path)
    apply = subparsers.add_parser("installer-apply", help="validate and atomically install the verified package")
    apply.add_argument("installer", type=Path)
    apply.add_argument("destination", type=Path)
    apply.add_argument("--overwrite", action="store_true")
    return parser


def _load(path: Path) -> dict:
    return loads_uir(path.read_text(encoding="utf-8"))


def _metadata(values: list[str]) -> dict[str, str]:
    result: dict[str, str] = {}
    for item in values:
        key, separator, value = item.partition("=")
        if not separator or not key.strip():
            raise ValueError("--metadata values must use KEY=VALUE")
        result[key.strip()] = value
    return result


def _installation_json(args: argparse.Namespace) -> str:
    target = TargetDescriptor(args.target, args.architecture, args.abi)
    plan = plan_installation(target, kind=InstallerKind(args.kind), artifact_format=args.artifact_format, bootable=args.bootable, filesystem=args.filesystem, artifacts=tuple(args.artifact), metadata=_metadata(args.metadata))
    if args.manifest:
        return plan.render_manifest()
    return json.dumps({"identity": plan.identity(), "target": plan.target.identity(), "kind": plan.kind.value, "artifact_format": plan.artifact_format, "bootable": plan.bootable, "filesystem": plan.filesystem, "artifacts": list(plan.artifacts), "metadata": dict(plan.metadata)}, ensure_ascii=False, sort_keys=True)


def _validate_native(path: Path) -> int:
    uir = OmniNativeFrontend().parse(path.read_text(encoding="utf-8"), filename=str(path))
    print(json.dumps(uir.to_dict(), ensure_ascii=False, sort_keys=True))
    return 0


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "install-plan":
            print(_installation_json(args), end="" if args.manifest else "\n")
            return 0
        if args.command == "installer-inspect":
            print(json.dumps(inspect_installer(args.installer.read_bytes()), ensure_ascii=False, sort_keys=True))
            return 0
        if args.command == "installer-extract":
            path = extract_installer(args.installer.read_bytes(), args.destination)
            print(path)
            return 0
        if args.command == "installer-apply":
            path = apply_installer(args.installer.read_bytes(), args.destination, overwrite=args.overwrite)
            print(path)
            return 0
        if args.command == "build":
            artifact = compile_native_artifact(args.source.read_text(encoding="utf-8"), filename=str(args.source))
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_bytes(artifact.payload)
            return 0
        if args.command == "native-exec":
            document = _load(args.source)
            result = compile_semantics(document)
            if not result.ok or result.ir is None:
                print(format_diagnostics(result.diagnostics), file=sys.stderr)
                return 2
            target = TargetDescriptor(args.target, args.architecture, "sysv", {"native-executable": True})
            executable = compile_native_executable(result.ir, target)
            write_native_executable(args.output, executable)
            return 0
        if args.command == "validate" and args.language == "omni":
            return _validate_native(args.source)
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
