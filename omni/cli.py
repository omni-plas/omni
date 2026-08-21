"""Command-line entry point for Omni validation, execution, inspection, and emission."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .emitters import EmitterError, emit_c
from .errors import OmniError
from .lower import lower_to_ir
from .pipeline import compile_semantics
from .runtime import execute_module
from .serialization import loads_uir
from .targets import TargetDescriptor


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="omni", description="Omni semantic compiler")
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

    return parser


def _load(path: Path) -> dict:
    return loads_uir(path.read_text(encoding="utf-8"))


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        document = _load(args.source)

        if args.command == "validate":
            result = compile_semantics(document)
            if not result.ok or result.ir is None:
                for diagnostic in result.diagnostics:
                    print(f"omni: {diagnostic.severity.value}: {diagnostic.message}", file=sys.stderr)
                return 2
            print("valid")
            return 0

        if args.command == "run":
            result = compile_semantics(document)
            if not result.ok or result.ir is None:
                for diagnostic in result.diagnostics:
                    print(f"omni: {diagnostic.severity.value}: {diagnostic.message}", file=sys.stderr)
                return 2
            entry = args.entry or document["semantics"]["program"]["entry"]
            values = json.loads(args.args)
            if not isinstance(values, dict):
                raise ValueError("--args must be a JSON object")
            output = execute_module(result.ir, entry, values)
            print(json.dumps(output, ensure_ascii=False))
            return 0

        if args.command == "emit-c":
            module = lower_to_ir(document)
            args.output.write_bytes(emit_c(module, TargetDescriptor("portable-c")))
            return 0

    except (OSError, ValueError, KeyError, EmitterError, OmniError, json.JSONDecodeError) as exc:
        print(f"omni: error: {exc}", file=sys.stderr)
        return 2
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
