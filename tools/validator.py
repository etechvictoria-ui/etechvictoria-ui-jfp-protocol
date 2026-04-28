#!/usr/bin/env python3
"""JFP validator prototype.

Validation layers:
L1 - syntax
L2 - structure
L3 - dependency
L4 - policy
L5 - execution safety
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

try:
    from parser import parse_jfp
except ImportError:
    from tools.parser import parse_jfp


def _facts_by_key(facts: list[dict[str, Any]], key: str) -> list[dict[str, Any]]:
    return [f for f in facts if f.get("key") == key]


def _block_value(block: dict[str, Any], key: str) -> str | None:
    for fact in block.get("facts", []):
        if fact.get("key") == key:
            return fact.get("value")
    return None


def validate(text: str) -> dict[str, Any]:
    ast = parse_jfp(text)
    facts = ast["facts"]
    sections = ast["sections"]
    blocks = ast["blocks"]

    issues: list[dict[str, str]] = []

    def add(layer: str, message: str) -> None:
        issues.append({"layer": layer, "message": message})

    # L1 - syntax
    if "JFP_DOCUMENT" not in sections:
        add("L1", "Missing JFP_DOCUMENT section")
    if "END_JFP" not in sections:
        add("L1", "Missing END_JFP marker")
    for fact in facts:
        if fact.get("key") == "__SYNTAX_ERROR__":
            add("L1", f"Syntax error on line {fact.get('line')}: {fact.get('value')}")

    # L2 - structure
    if not _facts_by_key(facts, "VERSION"):
        add("L2", "Missing VERSION fact")
    if not _facts_by_key(facts, "TYPE"):
        add("L2", "Missing TYPE fact")
    if "META" not in sections:
        add("L2", "Missing META section")
    if "BUILD_GRAPH" not in sections and "PATCH_GRAPH" not in sections:
        add("L2", "Missing BUILD_GRAPH or PATCH_GRAPH section")

    task_blocks = {
        block_id: block
        for block_id, block in blocks.items()
        if block_id.startswith("TASK_")
    }

    for task_id, task in task_blocks.items():
        if not _block_value(task, "ACTION"):
            add("L2", f"{task_id}: missing ACTION")
        if not _block_value(task, "OUTPUT"):
            add("L2", f"{task_id}: missing OUTPUT")

    # L3 - dependency
    task_ids = set(task_blocks)
    for task_id, task in task_blocks.items():
        deps = [f.get("value") for f in task.get("facts", []) if f.get("key") == "DEPENDENCY"]
        for dep in deps:
            if dep not in task_ids:
                add("L3", f"{task_id}: unknown dependency {dep}")

    # L4 - policy
    constraint_values = {f.get("value") for f in facts if f.get("section") == "CONSTRAINTS" and f.get("key") == "RULE"}
    if not constraint_values:
        add("L4", "No CONSTRAINTS rules declared")

    destructive_actions = {"fs.delete", "fs.rm", "dependency.install", "shell.exec"}
    for task_id, task in task_blocks.items():
        action = _block_value(task, "ACTION")
        if action in destructive_actions and "requires_human_approval" not in constraint_values:
            add("L4", f"{task_id}: action {action} requires explicit approval constraint")

    # L5 - execution safety
    output_map_paths = {
        f.get("value")
        for f in facts
        if f.get("section") == "OUTPUT_MAP" and f.get("key") == "PATH"
    }
    if not output_map_paths:
        add("L5", "OUTPUT_MAP has no PATH entries")

    for task_id, task in task_blocks.items():
        output = _block_value(task, "OUTPUT")
        if output and output_map_paths and output not in output_map_paths:
            add("L5", f"{task_id}: output {output} not declared in OUTPUT_MAP")

    signal_triggers = {
        f.get("value")
        for f in facts
        if f.get("section") == "SIGNAL_ORANGE" and f.get("key") == "TRIGGER"
    }
    if "output_not_mapped" not in signal_triggers:
        add("L5", "SIGNAL_ORANGE should include output_not_mapped")
    if "constraint_conflict" not in signal_triggers:
        add("L5", "SIGNAL_ORANGE should include constraint_conflict")

    layer_status = {}
    for layer in ["L1", "L2", "L3", "L4", "L5"]:
        layer_status[layer] = not any(issue["layer"] == layer for issue in issues)

    return {
        "valid": not issues,
        "layers": layer_status,
        "issue_count": len(issues),
        "issues": issues,
    }


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("Usage: validator.py <SPEC.jfp>", file=sys.stderr)
        return 2

    path = Path(argv[1])
    if not path.exists():
        print(f"File not found: {path}", file=sys.stderr)
        return 2

    report = validate(path.read_text(encoding="utf-8"))
    print(json.dumps(report, indent=2))
    return 0 if report["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
