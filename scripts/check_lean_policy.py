#!/usr/bin/env python3
"""Fail-closed release-specific AI/Lean policy check.

The common Math harness intentionally ignores every ``support_runs`` segment,
so its PASS does not cover this repository. This checker applies the same eight
Lean rules to the exact public module inventory and also rejects floating
GitHub Action references.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
POLICY_PATH = ROOT / "evidence" / "verification-policy.json"
INVENTORY_PATH = ROOT / "evidence" / "module-declaration-inventory.json"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def remove_lean_comments_and_strings(text: str) -> str:
    """Replace nested comments and strings by spaces while retaining lines."""

    output: list[str] = []
    block_depth = 0
    in_line_comment = False
    in_string = False
    escaped = False
    index = 0
    while index < len(text):
        char = text[index]
        next_char = text[index + 1] if index + 1 < len(text) else ""

        if in_line_comment:
            if char in "\r\n":
                output.append(char)
                in_line_comment = False
            else:
                output.append(" ")
            index += 1
            continue

        if block_depth:
            if char == "/" and next_char == "-":
                block_depth += 1
                output.extend((" ", " "))
                index += 2
                continue
            if char == "-" and next_char == "/":
                block_depth -= 1
                output.extend((" ", " "))
                index += 2
                continue
            output.append(char if char in "\r\n" else " ")
            index += 1
            continue

        if in_string:
            output.append(char if char in "\r\n" else " ")
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            index += 1
            continue

        if char == "-" and next_char == "-":
            in_line_comment = True
            output.extend((" ", " "))
            index += 2
            continue
        if char == "/" and next_char == "-":
            block_depth = 1
            output.extend((" ", " "))
            index += 2
            continue
        if char == '"':
            in_string = True
            output.append(" ")
            index += 1
            continue

        output.append(char)
        index += 1

    return "".join(output)


def main() -> int:
    policy = load_json(POLICY_PATH)
    inventory = load_json(INVENTORY_PATH)
    errors: list[str] = []
    findings: list[dict[str, Any]] = []

    expected_paths = sorted(inventory.get("modules", {}))
    actual_paths = sorted(
        path.relative_to(ROOT).as_posix()
        for tree in (ROOT / "src", ROOT / "test")
        for path in tree.rglob("*.lean")
        if path.is_file()
    )
    if actual_paths != expected_paths:
        errors.append(
            "LEAN_MODULE_SET_MISMATCH: "
            f"missing={sorted(set(expected_paths) - set(actual_paths))}, "
            f"extra={sorted(set(actual_paths) - set(expected_paths))}"
        )

    expected_count = policy["scan"]["expected_lean_files"]
    if len(actual_paths) != expected_count:
        errors.append(
            f"LEAN_FILE_DENOMINATOR_MISMATCH: {len(actual_paths)} != {expected_count}"
        )

    for relative in actual_paths:
        path = ROOT / relative
        raw = path.read_text(encoding="utf-8")
        active = remove_lean_comments_and_strings(raw)
        raw_lines = raw.splitlines()
        for rule in policy["lean_rules"]:
            pattern = re.compile(rule["regex"], re.IGNORECASE)
            for match in pattern.finditer(active):
                line_number = active.count("\n", 0, match.start()) + 1
                finding = {
                    "path": relative,
                    "line": line_number,
                    "rule": rule["id"],
                    "severity": rule["severity"],
                    "excerpt": raw_lines[line_number - 1].strip()
                    if line_number <= len(raw_lines)
                    else "",
                    "allowlisted": False,
                    "disposition": "OPEN_REVIEW_REQUIRED",
                }
                findings.append(finding)
                errors.append(
                    f"{rule['id']} at {relative}:{line_number} ({rule['severity']})"
                )

    uses_pattern = re.compile(r"(?m)^\s*(?:-\s*)?uses:\s*([^\s#]+)")
    observed_actions: dict[str, str] = {}
    for workflow in sorted((ROOT / ".github" / "workflows").glob("*.y*ml")):
        text = workflow.read_text(encoding="utf-8")
        for reference in uses_pattern.findall(text):
            if reference.startswith("./"):
                continue
            if "@" not in reference:
                errors.append(f"UNPINNED_ACTION: {workflow.relative_to(ROOT)}: {reference}")
                continue
            action, revision = reference.rsplit("@", 1)
            observed_actions[action] = revision
            if not re.fullmatch(r"[0-9a-fA-F]{40}", revision):
                errors.append(f"UNPINNED_ACTION: {workflow.relative_to(ROOT)}: {reference}")

    for action, expected_revision in policy["remote_action_pins"].items():
        if action == "all_remote_uses_must_end_in_40_hex":
            continue
        actual_revision = observed_actions.get(action)
        if actual_revision != expected_revision:
            errors.append(
                f"ACTION_PIN_MISMATCH: {action}@{actual_revision} != {expected_revision}"
            )

    result = {
        "schema_version": "1.0.0",
        "campaign_id": policy["campaign_id"],
        "status": "PASS" if not errors else "FAIL",
        "lean_files_scanned": len(actual_paths),
        "expected_lean_files": expected_count,
        "findings": findings,
        "open_findings": len(findings),
        "remote_actions": observed_actions,
        "errors": errors,
        "gate_transfer_allowed": False,
        "does_not_establish": [
            "compilation",
            "kernel replay",
            "axiom equality",
            "semantic fidelity",
            "human source review",
            "canonical promotion",
        ],
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
