"""Command-line entry point for executing a validated UIR program."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .pipeline import compile_semantics
from .runtime import execute_module
from .serialization import loads_uir


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="omni", description="Omni UIR compiler/runtime")
    subparsers = parser.add_subparsers(dest="command", required=True)

    run = subparsers.add_parser("run", help="validate, lower, and execute a UIR JSON program")
    run.add_argument("source", type=Path)
    run.add_argument("--entry", default=None)
    run.add_argument("--args", default="{}", help="JSON object containing entry arguments")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "run":
        try:
            document = loads_uir(args.source.read_text(encoding="utf-8"))
            result = compile_semantics(document)
            entry = args.entry or document["semantics"]["program"]["entry"]
            values = json.loads(args.args)
            if not isinstance(values, dict):
                raise ValueError("--args must be a JSON object")
            output = execute_module(result.ir, entry, values)
        except (OSError, ValueError, KeyError) as exc:
            print(f"omni: error: {exc}", file=sys.stderr)
            return 2
        print(json.dumps(output, ensure_ascii=False))
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
