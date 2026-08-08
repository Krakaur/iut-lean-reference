#!/usr/bin/env python3
"""Check the exact 16/68/92 Lean inventory and optional axiom replay."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
import unicodedata
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
INVENTORY_PATH = ROOT / "evidence" / "module-declaration-inventory.json"
WHITELIST_PATH = ROOT / "evidence" / "axiom-whitelist.json"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def remove_lean_comments_and_strings(text: str) -> str:
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


def flatten_whitelist(document: dict[str, Any], errors: list[str]) -> dict[str, list[str]]:
    expected: dict[str, list[str]] = {}
    allowed = set(document["allowed_axiom_universe"])
    for group in document["expected_groups"]:
        axioms = sorted(group["axioms"])
        if not set(axioms) <= allowed:
            errors.append(f"WHITELIST_USES_UNPERMITTED_AXIOM: {axioms}")
        for declaration in group["declarations"]:
            if declaration in expected:
                errors.append(f"DUPLICATE_WHITELIST_DECLARATION: {declaration}")
            expected[declaration] = axioms
    return expected


def normalized_path_key(value: str) -> str:
    return unicodedata.normalize("NFC", value).casefold()


def static_checks(
    inventory: dict[str, Any], whitelist: dict[str, Any]
) -> tuple[list[str], dict[str, Any], dict[str, list[str]]]:
    errors: list[str] = []
    expected_axioms = flatten_whitelist(whitelist, errors)
    counts = inventory["expected_counts"]

    expected_modules: dict[str, str] = inventory["modules"]
    actual_paths = sorted(
        path.relative_to(ROOT).as_posix()
        for tree in (ROOT / "src", ROOT / "test")
        for path in tree.rglob("*.lean")
        if path.is_file()
    )
    expected_paths = sorted(expected_modules)
    if actual_paths != expected_paths:
        errors.append(
            "MODULE_SET_MISMATCH: "
            f"missing={sorted(set(expected_paths) - set(actual_paths))}, "
            f"extra={sorted(set(actual_paths) - set(expected_paths))}"
        )
    if len(actual_paths) != counts["modules"]:
        errors.append(f"MODULE_DENOMINATOR_MISMATCH: {len(actual_paths)} != {counts['modules']}")
    if any((ROOT / relative).is_symlink() for relative in actual_paths):
        errors.append("SYMLINKED_LEAN_MODULE")
    path_keys = [normalized_path_key(relative) for relative in actual_paths]
    if len(path_keys) != len(set(path_keys)):
        errors.append("CASE_OR_UNICODE_PATH_COLLISION")

    module_to_path = {module: path for path, module in expected_modules.items()}
    reachable: set[str] = set()
    stack = list(inventory["roots"])
    import_pattern = re.compile(r"(?m)^\s*import\s+([A-Za-z0-9_.']+)\s*$")
    while stack:
        module = stack.pop()
        if module in reachable or module not in module_to_path:
            continue
        reachable.add(module)
        active = remove_lean_comments_and_strings(
            (ROOT / module_to_path[module]).read_text(encoding="utf-8")
        )
        for imported in import_pattern.findall(active):
            if imported in module_to_path and imported not in reachable:
                stack.append(imported)
    missing_reachable = sorted(set(module_to_path) - reachable)
    if missing_reachable:
        errors.append(f"UNREACHABLE_LOCAL_MODULES: {missing_reachable}")

    expected_declarations = inventory["declarations"]
    expected_by_short: dict[str, dict[str, str]] = {}
    for row in expected_declarations:
        short = row["name"].rsplit(".", 1)[-1]
        if short in expected_by_short:
            errors.append(f"DUPLICATE_DECLARATION_BASENAME_IN_INVENTORY: {short}")
        expected_by_short[short] = row

    declaration_pattern = re.compile(r"(?m)^\s*(theorem|instance)\s+([A-Za-z0-9_']+)\b")
    instance_start_pattern = re.compile(r"(?m)^\s*instance\b")
    actual_declarations: list[dict[str, str]] = []
    named_instance_count = 0
    all_instance_count = 0
    for relative in actual_paths:
        active = remove_lean_comments_and_strings((ROOT / relative).read_text(encoding="utf-8"))
        matches = declaration_pattern.findall(active)
        named_instance_count += sum(1 for kind, _ in matches if kind == "instance")
        all_instance_count += len(instance_start_pattern.findall(active))
        for kind, short in matches:
            expected = expected_by_short.get(short)
            if expected is None:
                errors.append(f"UNREGISTERED_DECLARATION: {relative}:{kind} {short}")
                continue
            actual_declarations.append(
                {"name": expected["name"], "kind": kind, "path": relative}
            )
    if all_instance_count != named_instance_count:
        errors.append(
            f"ANONYMOUS_OR_UNPARSED_INSTANCE: starts={all_instance_count}, named={named_instance_count}"
        )

    actual_keyed = {
        (row["name"], row["kind"], row["path"]) for row in actual_declarations
    }
    expected_keyed = {
        (row["name"], row["kind"], row["path"]) for row in expected_declarations
    }
    if actual_keyed != expected_keyed or len(actual_declarations) != len(expected_declarations):
        errors.append(
            "DECLARATION_SET_MISMATCH: "
            f"missing={sorted(expected_keyed - actual_keyed)}, "
            f"extra={sorted(actual_keyed - expected_keyed)}"
        )
    if len(actual_declarations) != counts["public_theorem_named_instances"]:
        errors.append(
            "DECLARATION_DENOMINATOR_MISMATCH: "
            f"{len(actual_declarations)} != {counts['public_theorem_named_instances']}"
        )

    query_pattern = re.compile(r"(?m)^\s*#print axioms ([A-Za-z0-9_.']+)\s*$")
    query_names: list[str] = []
    for relative in actual_paths:
        if not relative.startswith("test/"):
            continue
        active = remove_lean_comments_and_strings((ROOT / relative).read_text(encoding="utf-8"))
        query_names.extend(query_pattern.findall(active))
    duplicates = sorted(name for name, count in Counter(query_names).items() if count > 1)
    if duplicates:
        errors.append(f"DUPLICATE_AXIOM_QUERIES: {duplicates}")
    if set(query_names) != set(expected_axioms):
        errors.append(
            "AXIOM_QUERY_SET_MISMATCH: "
            f"missing={sorted(set(expected_axioms) - set(query_names))}, "
            f"extra={sorted(set(query_names) - set(expected_axioms))}"
        )
    if len(query_names) != counts["axiom_queries"]:
        errors.append(f"AXIOM_QUERY_DENOMINATOR_MISMATCH: {len(query_names)} != {counts['axiom_queries']}")
    declaration_names = {row["name"] for row in expected_declarations}
    if not declaration_names <= set(expected_axioms):
        errors.append(
            f"PUBLIC_DECLARATIONS_WITHOUT_WHITELIST: {sorted(declaration_names - set(expected_axioms))}"
        )

    observed_distribution = Counter(tuple(axioms) for axioms in expected_axioms.values())
    expected_distribution = {
        tuple(): whitelist["expected_distribution"]["no_axioms"],
        ("propext",): whitelist["expected_distribution"]["propext_only"],
        ("Quot.sound", "propext"): whitelist["expected_distribution"]["propext_and_quot_sound"],
        ("Classical.choice", "Quot.sound", "propext"): whitelist["expected_distribution"]["classical_choice_propext_quot_sound"],
    }
    if observed_distribution != Counter(expected_distribution):
        errors.append(
            f"WHITELIST_DISTRIBUTION_MISMATCH: {dict(observed_distribution)} != {expected_distribution}"
        )

    report = {
        "modules": len(actual_paths),
        "reachable_modules": len(reachable),
        "public_theorem_named_instances": len(actual_declarations),
        "axiom_queries": len(query_names),
        "whitelist_entries": len(expected_axioms),
    }
    return errors, report, expected_axioms


def replay_axioms(
    whitelist: dict[str, Any],
    expected_axioms: dict[str, list[str]],
    lean_executable: str | None,
) -> tuple[list[str], dict[str, Any]]:
    errors: list[str] = []
    process_reports: list[dict[str, Any]] = []
    outputs: list[str] = []
    for relative in whitelist["audit_files"]:
        command = (
            [lean_executable, relative]
            if lean_executable
            else ["lake", "env", "lean", relative]
        )
        process = subprocess.run(command, cwd=ROOT, capture_output=True, check=False)
        raw = process.stdout + b"\n" + process.stderr
        text = raw.decode("utf-8", errors="replace")
        outputs.append(text)
        process_reports.append(
            {
                "path": relative,
                "command": " ".join(command),
                "exit_code": process.returncode,
                "output_sha256": hashlib.sha256(raw).hexdigest(),
            }
        )
        if process.returncode != 0:
            errors.append(f"LEAN_AXIOM_REPLAY_FAILED: {relative}: exit {process.returncode}")

    combined = "\n".join(outputs)
    report_pattern = re.compile(
        r"'(?P<name>[A-Za-z0-9_.']+)'\s+(?:"
        r"depends on axioms:\s*\[(?P<axioms>[^\]]*)\]"
        r"|(?P<none>does not depend on any axioms))"
    )
    actual: dict[str, list[str]] = {}
    duplicates: list[str] = []
    for match in report_pattern.finditer(combined):
        name = match.group("name")
        if name in actual:
            duplicates.append(name)
            continue
        if match.group("none"):
            axioms: list[str] = []
        else:
            axioms = sorted(
                item.strip()
                for item in match.group("axioms").split(",")
                if item.strip()
            )
        actual[name] = axioms
    if duplicates:
        errors.append(f"DUPLICATE_AXIOM_REPORTS: {sorted(duplicates)}")
    if set(actual) != set(expected_axioms):
        errors.append(
            "AXIOM_REPORT_SET_MISMATCH: "
            f"missing={sorted(set(expected_axioms) - set(actual))}, "
            f"extra={sorted(set(actual) - set(expected_axioms))}"
        )

    allowed = set(whitelist["allowed_axiom_universe"])
    deltas: list[dict[str, Any]] = []
    for name in sorted(set(actual) & set(expected_axioms)):
        actual_set = sorted(actual[name])
        expected_set = sorted(expected_axioms[name])
        if not set(actual_set) <= allowed:
            errors.append(f"UNPERMITTED_AXIOM: {name}: {actual_set}")
        if actual_set != expected_set:
            deltas.append(
                {"declaration": name, "expected": expected_set, "actual": actual_set}
            )
    if deltas:
        errors.append(f"REVIEW_REQUIRED_AXIOM_DELTA: {deltas}")

    distribution = Counter(tuple(values) for values in actual.values())
    report = {
        "status": "PASS" if not errors else "FAIL",
        "actual_queries": len(actual),
        "whitelist_match": not deltas and set(actual) == set(expected_axioms),
        "distribution": [
            {"axioms": list(axioms), "declarations": count}
            for axioms, count in sorted(distribution.items())
        ],
        "processes": process_reports,
        "deltas": deltas,
    }
    return errors, report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--run",
        action="store_true",
        help="After static checks, replay all seven audit modules and compare actual output.",
    )
    parser.add_argument(
        "--lean-executable",
        help=(
            "Use an already resolved Lean executable for bounded local replay. "
            "CI deliberately omits this option and uses lake env lean."
        ),
    )
    args = parser.parse_args()

    inventory = load_json(INVENTORY_PATH)
    whitelist = load_json(WHITELIST_PATH)
    static_errors, static_report, expected_axioms = static_checks(inventory, whitelist)
    dynamic_report: dict[str, Any] = {
        "status": "NOT_RUN",
        "reason": "Use --run after compilation to replay actual #print axioms output.",
    }
    dynamic_errors: list[str] = []
    if args.run and not static_errors:
        dynamic_errors, dynamic_report = replay_axioms(
            whitelist, expected_axioms, args.lean_executable
        )
    elif args.run:
        dynamic_report = {"status": "BLOCKED_BY_STATIC_FAILURE"}

    errors = static_errors + dynamic_errors
    result = {
        "schema_version": "1.0.0",
        "status": "PASS" if not errors else "FAIL",
        "inventory": {
            "status": "PASS" if not static_errors else "FAIL",
            **static_report,
        },
        "compilation": {
            "status": "NOT_EVALUATED_BY_THIS_SCRIPT",
            "expected_ci_command": "lake build",
        },
        "kernel": {
            "status": "NOT_EVALUATED_BY_THIS_SCRIPT",
            "expected_ci_command": "lake env leanchecker IUT1 IUT1Audit",
        },
        "axioms": dynamic_report,
        "fidelity": {
            "status": "NOT_EVALUATED_IN_CI",
            "historical_evidence_only": True,
        },
        "gate_transfer_allowed": False,
        "errors": errors,
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
