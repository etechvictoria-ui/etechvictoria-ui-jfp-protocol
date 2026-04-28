#!/usr/bin/env python3
"""JFP parser prototype.

Parses JFP text into sections, blocks, and fact records.
This is intentionally small and dependency-free.
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any


@dataclass
class Fact:
    key: str
    value: str
    line: int
    section: str | None = None
    block: str | None = None


def parse_jfp(text: str) -> dict[str, Any]:
    """Parse JFP text into a lightweight AST-like dictionary."""
    current_section: str | None = None
    current_block: str | None = None
    sections: dict[str, list[dict[str, Any]]] = {}
    blocks: dict[str, dict[str, Any]] = {}
    facts: list[Fact] = []
    raw_lines = text.splitlines()

    for line_no, raw in enumerate(raw_lines, start=1):
        line = raw.strip()

        if not line:
            continue

        if line.startswith("===") and line.endswith("==="):
            current_section = line.strip("= ").strip()
            current_block = None
            sections.setdefault(current_section, [])
            continue

        if line.startswith("[") and line.endswith("]"):
            current_block = line[1:-1].strip()
            blocks[current_block] = {"section": current_section, "facts": []}
            continue

        if line.startswith("F:"):
            if not line.endswith(";"):
                facts.append(Fact("__SYNTAX_ERROR__", line, line_no, current_section, current_block))
                continue

            content = line[:-1]
            parts = content.split(":", 2)
            if len(parts) != 3:
                facts.append(Fact("__SYNTAX_ERROR__", line, line_no, current_section, current_block))
                continue

            _, key, value = parts
            fact = Fact(key=key.strip(), value=value.strip(), line=line_no, section=current_section, block=current_block)
            facts.append(fact)

            item = asdict(fact)
            if current_section:
                sections.setdefault(current_section, []).append(item)
            if current_block:
                blocks[current_block]["facts"].append(item)

    return {
        "sections": sections,
        "blocks": blocks,
        "facts": [asdict(f) for f in facts],
    }


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("Usage: parser.py <SPEC.jfp>", file=sys.stderr)
        return 2

    path = Path(argv[1])
    if not path.exists():
        print(f"File not found: {path}", file=sys.stderr)
        return 2

    ast = parse_jfp(path.read_text(encoding="utf-8"))
    print(json.dumps(ast, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
