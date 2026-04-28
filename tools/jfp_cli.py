#!/usr/bin/env python3
"""JFP command line interface prototype.

Usage:
  python tools/jfp_cli.py parse specs/minimal-build-spec.jfp
  python tools/jfp_cli.py validate specs/minimal-build-spec.jfp
  python tools/jfp_cli.py inspect specs/minimal-build-spec.jfp
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

try:
    from parser import parse_jfp
    from validator import validate
except ImportError:
    from tools.parser import parse_jfp
    from tools.validator import validate


def read_spec(path_value: str) -> str:
    path = Path(path_value)
    if not path.exists():
        raise FileNotFoundError(f"JFP spec not found: {path}")
    if not path.is_file():
        raise IsADirectoryError(f"Expected a file, got directory: {path}")
    return path.read_text(encoding="utf-8")


def command_parse(args: argparse.Namespace) -> int:
    text = read_spec(args.spec)
    ast = parse_jfp(text)
    print(json.dumps(ast, indent=2))
    return 0


def command_validate(args: argparse.Namespace) -> int:
    text = read_spec(args.spec)
    report = validate(text)
    print(json.dumps(report, indent=2))
    return 0 if report.get("valid") else 1


def command_inspect(args: argparse.Namespace) -> int:
    text = read_spec(args.spec)
    ast = parse_jfp(text)
    report = validate(text)

    sections = list(ast.get("sections", {}).keys())
    blocks = ast.get("blocks", {})
    task_count = len([name for name in blocks if name.startswith("TASK_")])
    fact_count = len(ast.get("facts", []))

    summary: dict[str, Any] = {
        "spec": args.spec,
        "valid": report.get("valid"),
        "issue_count": report.get("issue_count"),
        "sections": sections,
        "task_count": task_count,
        "fact_count": fact_count,
    }

    print(json.dumps(summary, indent=2))
    return 0 if report.get("valid") else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="jfp",
        description="JFP - JARO Flash Protocol CLI prototype",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    parse_cmd = subparsers.add_parser("parse", help="Parse a .jfp file into JSON")
    parse_cmd.add_argument("spec", help="Path to a .jfp specification file")
    parse_cmd.set_defaults(func=command_parse)

    validate_cmd = subparsers.add_parser("validate", help="Validate a .jfp file through L1-L5 checks")
    validate_cmd.add_argument("spec", help="Path to a .jfp specification file")
    validate_cmd.set_defaults(func=command_validate)

    inspect_cmd = subparsers.add_parser("inspect", help="Show a compact summary of a .jfp file")
    inspect_cmd.add_argument("spec", help="Path to a .jfp specification file")
    inspect_cmd.set_defaults(func=command_inspect)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
