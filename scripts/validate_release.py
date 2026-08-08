#!/usr/bin/env python3
"""Fail-closed structural validation for the public IUT-I reference package."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_CLAIMS = [f"T{i:02d}" for i in range(1, 12)]
EXPECTED_PUBLIC_THEOREM_INSTANCES = 68
EXPECTED_POLYACTION_ROLES = {
    "T01": "PREREQUISITE_ONLY",
    "T02": "PREREQUISITE_ONLY",
    "T03": "PREREQUISITE_ONLY",
    "T04": "LABEL_MODEL_ONLY",
    "T05": "ALGEBRAIC_INTERFACE_PROTOTYPE",
    "T06": "ORDINARY_ACTION_PREREQUISITE",
    "T07": "SINGLETON_POLYMORPHISM_SPECIAL_CASE",
    "T08": "CARDINALITY_ONLY",
    "T09": "ALGEBRAIC_POLYACTION_PROTOTYPE_INPUT",
    "T10": "TRANSPORT_CHECKPOINT_ONLY",
    "T11": "REGRESSION_ONLY",
}
IGNORED_DIRS = {".git", ".lake", "build", "__pycache__"}
MANIFEST_REL = "evidence/release-manifest.json"
ERRORS: list[str] = []


def fail(message: str) -> None:
    ERRORS.append(message)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def public_files() -> list[Path]:
    return sorted(
        path
        for path in ROOT.rglob("*")
        if path.is_file()
        and not any(part in IGNORED_DIRS for part in path.relative_to(ROOT).parts)
        and path.relative_to(ROOT).as_posix() != MANIFEST_REL
    )


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"invalid JSON {path.relative_to(ROOT)}: {exc}")
        return None


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except Exception as exc:
        fail(f"unreadable JSONL {path.relative_to(ROOT)}: {exc}")
        return rows
    for line_number, line in enumerate(lines, start=1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
            if not isinstance(row, dict):
                raise TypeError("row is not an object")
            rows.append(row)
        except Exception as exc:
            fail(f"invalid JSONL {path.relative_to(ROOT)}:{line_number}: {exc}")
    return rows


def check_required_files() -> None:
    required = {
        ".gitattributes",
        "README.md", "STATUS.md", "LICENSING.md", "lakefile.toml", "lean-toolchain",
        "CITATION.cff", "codemeta.json", "CONTRIBUTING.md", "LICENSE",
        "LICENSE-DOCUMENTATION.md", "NOTICE",
        "src/IUT1.lean", "src/IUT1/Tutorial.lean", "test/IUT1Audit.lean",
        "ai/schema.json", "ai/claims.jsonl", "ai/application-schema.json",
        "ai/applications.jsonl", "ai/examples.jsonl", "ai/use_cases.jsonl",
        "ai/anti_patterns.jsonl", "ai/polyaction-schema.json",
        "ai/polyaction_checkpoints.jsonl",
        "docs/poly-actions/source-and-boundary.md",
        "docs/poly-actions/algebraic-prototype.md",
        "docs/community/lana-outreach.md",
        "src/IUT1/Applications/PolyMorphismPrototype.lean",
        "test/IUT1/Applications/PolyMorphismPrototypeAxiomAudit.lean",
        "evidence/artifacts.json", "evidence/gates.json",
        "evidence/sources.json", MANIFEST_REL,
    }
    for rel in sorted(required):
        if not (ROOT / rel).is_file():
            fail(f"missing required public file {rel}")


def valid_orcid(orcid_url: str) -> bool:
    compact = re.sub(r"[^0-9X]", "", orcid_url.upper())
    if len(compact) != 16 or not compact[:15].isdigit():
        return False
    total = 0
    for digit in compact[:15]:
        total = (total + int(digit)) * 2
    result = (12 - total % 11) % 11
    expected = "X" if result == 10 else str(result)
    return compact[-1] == expected


def check_authorship_metadata() -> None:
    expected_name = "Dirk Hans Krakaur Floranes"
    expected_orcid = "https://orcid.org/0000-0002-6465-034X"
    expected_repo = "https://github.com/Krakaur/iut-lean-reference"

    codemeta = load_json(ROOT / "codemeta.json") or {}
    author = codemeta.get("author", {})
    if codemeta.get("@context") != "https://w3id.org/codemeta/3.1":
        fail("codemeta.json must use the CodeMeta 3.1 context")
    if codemeta.get("codeRepository") != expected_repo:
        fail("codemeta.json has an unexpected codeRepository")
    if codemeta.get("license") != "https://spdx.org/licenses/Apache-2.0":
        fail("codemeta.json has an unexpected software license")
    if author.get("name") != expected_name or author.get("@id") != expected_orcid:
        fail("codemeta.json author identity does not match the release identity")

    cff = (ROOT / "CITATION.cff").read_text(encoding="utf-8")
    for required in (
        'given-names: "Dirk Hans"',
        'family-names: "Krakaur Floranes"',
        f'orcid: "{expected_orcid}"',
        f'repository-code: "{expected_repo}"',
        "license: Apache-2.0",
    ):
        if required not in cff:
            fail(f"CITATION.cff lacks required metadata: {required}")
    if "0000-0000-0000-0000" in cff or not valid_orcid(expected_orcid):
        fail("CITATION.cff contains an invalid or placeholder ORCID")

    licensing = (ROOT / "LICENSING.md").read_text(encoding="utf-8")
    for required in (
        "Apache License 2.0",
        "Creative Commons Attribution 4.0 International",
        expected_orcid,
    ):
        if required not in licensing:
            fail(f"LICENSING.md lacks required attribution term: {required}")
    notice = (ROOT / "NOTICE").read_text(encoding="utf-8")
    if expected_name not in notice or expected_orcid not in notice:
        fail("NOTICE lacks the release author name or ORCID")


def lean_declaration_exists(qualified: str, lean_text: str) -> bool:
    short = qualified.rsplit(".", 1)[-1]
    pattern = re.compile(
        rf"(?m)^\s*(?:(?:@\[[^\n]+\])\s*)?(?:theorem|def|instance|structure|abbrev)\s+{re.escape(short)}\b"
    )
    return bool(pattern.search(lean_text))


def check_machine_layer() -> None:
    for path in sorted(ROOT.rglob("*.json")):
        if not any(part in IGNORED_DIRS for part in path.relative_to(ROOT).parts):
            load_json(path)

    claims = load_jsonl(ROOT / "ai" / "claims.jsonl")
    examples = load_jsonl(ROOT / "ai" / "examples.jsonl")
    applications = load_jsonl(ROOT / "ai" / "applications.jsonl")
    use_cases = load_jsonl(ROOT / "ai" / "use_cases.jsonl")
    polyaction_checkpoints = load_jsonl(ROOT / "ai" / "polyaction_checkpoints.jsonl")
    anti_patterns = load_jsonl(ROOT / "ai" / "anti_patterns.jsonl")
    sources_doc = load_json(ROOT / "evidence" / "sources.json") or {}
    source_ids = {
        item.get("source_id") for item in sources_doc.get("sources", [])
        if isinstance(item, dict)
    }

    ids = [row.get("claim_id") for row in claims]
    if ids != EXPECTED_CLAIMS:
        fail(f"claims.jsonl IDs are {ids}, expected {EXPECTED_CLAIMS}")
    if len(ids) != len(set(ids)):
        fail("claims.jsonl contains duplicate claim IDs")

    lean_text = "\n".join(
        path.read_text(encoding="utf-8")
        for tree in (ROOT / "src", ROOT / "test")
        for path in sorted(tree.rglob("*.lean"))
    )
    required_claim_fields = {
        "claim_id", "source_id", "localizers", "epistemic_status",
        "plain_statement", "lean_declarations", "dependencies",
        "discriminant", "gates", "does_not_establish",
    }
    for row in claims:
        cid = row.get("claim_id", "<unknown>")
        missing = required_claim_fields - row.keys()
        if missing:
            fail(f"{cid} lacks required fields {sorted(missing)}")
            continue
        for field in ("localizers", "epistemic_status", "lean_declarations", "does_not_establish"):
            if not isinstance(row[field], list) or not row[field]:
                fail(f"{cid}.{field} must be a nonempty array")
        if row["source_id"] not in source_ids:
            fail(f"{cid} references unknown source_id {row['source_id']}")
        for dep in row["dependencies"]:
            if dep not in EXPECTED_CLAIMS:
                fail(f"{cid} has unknown dependency {dep}")
        gates = row["gates"]
        for gate in ("semantic", "kernel", "fidelity", "replication"):
            if gates.get(gate) != "PASS":
                fail(f"{cid} does not have an explicit {gate}=PASS")
        for declaration in row["lean_declarations"]:
            if not lean_declaration_exists(declaration, lean_text):
                fail(f"{cid} references missing Lean declaration {declaration}")
        if not (ROOT / "docs" / "theorems" / f"{cid}.md").is_file():
            fail(f"{cid} lacks docs/theorems/{cid}.md")

    application_ids = [row.get("application_id") for row in applications]
    if application_ids != ["APP01"]:
        fail(f"applications.jsonl IDs are {application_ids}, expected ['APP01']")
    required_application_fields = {
        "application_id", "source_id", "localizers", "epistemic_status", "task",
        "lean_declarations", "dependencies", "positive_test", "negative_test",
        "discriminant", "gates", "does_not_establish",
    }
    for row in applications:
        aid = row.get("application_id", "<unknown>")
        missing = required_application_fields - row.keys()
        if missing:
            fail(f"{aid} lacks required fields {sorted(missing)}")
            continue
        if row["source_id"] not in source_ids:
            fail(f"{aid} references unknown source_id {row['source_id']}")
        for dep in row["dependencies"]:
            if dep not in EXPECTED_CLAIMS:
                fail(f"{aid} has unknown dependency {dep}")
        for declaration in row["lean_declarations"]:
            if not lean_declaration_exists(declaration, lean_text):
                fail(f"{aid} references missing Lean declaration {declaration}")
        for gate in ("semantic", "kernel", "fidelity", "replication"):
            if row["gates"].get(gate) != "PASS":
                fail(f"{aid} does not have an explicit {gate}=PASS")
        if not (ROOT / "docs" / "applications" / "convention-auditor.md").is_file():
            fail(f"{aid} lacks docs/applications/convention-auditor.md")

    example_ids: set[str] = set()
    for row in examples:
        eid = row.get("example_id")
        if not eid or eid in example_ids:
            fail(f"missing or duplicate example_id {eid}")
        example_ids.add(eid)
        if row.get("claim_id") not in EXPECTED_CLAIMS:
            fail(f"{eid} references unknown claim_id {row.get('claim_id')}")
        lean_refs = row.get("lean")
        if lean_refs:
            for declaration in (part.strip() for part in lean_refs.split(";")):
                if not lean_declaration_exists(declaration, lean_text):
                    fail(f"{eid} references missing Lean declaration {declaration}")

    anti_ids = [row.get("anti_pattern_id") for row in anti_patterns]
    if len(anti_ids) != len(set(anti_ids)) or any(not item for item in anti_ids):
        fail("anti_patterns.jsonl has missing or duplicate IDs")
    for row in anti_patterns:
        for field in ("anti_pattern_id", "name", "bad_inference", "rejected_by"):
            if not row.get(field):
                fail(f"anti-pattern row lacks nonempty {field}")

    use_case_ids: set[str] = set()
    for row in use_cases:
        uid = row.get("use_case_id")
        if not uid or uid in use_case_ids:
            fail(f"missing or duplicate use_case_id {uid}")
        use_case_ids.add(uid)
        if row.get("source_id") not in source_ids:
            fail(f"{uid} references unknown source_id {row.get('source_id')}")
        for field in ("localizers", "epistemic_status", "audience", "input", "output", "example", "lean", "does_not_establish"):
            if not row.get(field):
                fail(f"{uid} lacks nonempty {field}")
        for declaration in (part.strip() for part in row.get("lean", "").split(";")):
            if declaration and not lean_declaration_exists(declaration, lean_text):
                fail(f"{uid} references missing Lean declaration {declaration}")

    checkpoint_ids = [row.get("target_id") for row in polyaction_checkpoints]
    if checkpoint_ids != EXPECTED_CLAIMS:
        fail(
            "polyaction_checkpoints.jsonl IDs are "
            f"{checkpoint_ids}, expected {EXPECTED_CLAIMS}"
        )
    required_checkpoint_fields = {
        "target_id", "role", "source_id", "localizers", "epistemic_status",
        "example", "lean_declarations", "discriminant", "scientific_boundary",
        "target_gate_unchanged",
    }
    for row in polyaction_checkpoints:
        tid = row.get("target_id", "<unknown>")
        missing = required_checkpoint_fields - row.keys()
        if missing:
            fail(f"poly-action checkpoint {tid} lacks fields {sorted(missing)}")
            continue
        if row["role"] != EXPECTED_POLYACTION_ROLES.get(tid):
            fail(f"poly-action checkpoint {tid} has incorrect role {row['role']}")
        if row["source_id"] not in source_ids:
            fail(f"poly-action checkpoint {tid} references unknown source_id {row['source_id']}")
        for field in ("localizers", "epistemic_status", "lean_declarations"):
            if not isinstance(row[field], list) or not row[field]:
                fail(f"poly-action checkpoint {tid}.{field} must be a nonempty array")
        if row["target_gate_unchanged"] is not True:
            fail(f"poly-action checkpoint {tid} must preserve the target gate")
        for declaration in row["lean_declarations"]:
            if not lean_declaration_exists(declaration, lean_text):
                fail(f"poly-action checkpoint {tid} references missing Lean declaration {declaration}")
        theorem_page = ROOT / "docs" / "theorems" / f"{tid}.md"
        if theorem_page.is_file():
            page_text = theorem_page.read_text(encoding="utf-8")
            if "## Poly-action checkpoint" not in page_text:
                fail(f"{tid} lacks its Poly-action checkpoint section")
            if row["role"] not in page_text:
                fail(f"{tid} page does not expose role {row['role']}")


def check_export_hashes() -> None:
    manifest = load_json(ROOT / "evidence" / "artifacts.json") or {}
    for section in ("core", "audits", "pedagogy", "applications", "integration"):
        for item in manifest.get(section, []):
            path = ROOT / item["path"]
            if not path.is_file():
                fail(f"missing exported artifact {item['path']}")
                continue
            actual = sha256(path)
            if actual != item["sha256"]:
                fail(f"hash mismatch for {item['path']}: {actual} != {item['sha256']}")


def check_release_manifest() -> None:
    path = ROOT / MANIFEST_REL
    if not path.is_file():
        return
    doc = load_json(path) or {}
    entries = doc.get("files", [])
    recorded = [entry.get("path") for entry in entries if isinstance(entry, dict)]
    expected = [item.relative_to(ROOT).as_posix() for item in public_files()]
    if recorded != expected:
        missing = sorted(set(expected) - set(recorded))
        extra = sorted(set(recorded) - set(expected))
        fail(f"release manifest path mismatch; missing={missing}, extra={extra}")
    if len(recorded) != len(set(recorded)):
        fail("release manifest contains duplicate paths")
    for entry in entries:
        if not isinstance(entry, dict) or "path" not in entry:
            fail("release manifest contains a malformed entry")
            continue
        item = ROOT / entry["path"]
        if not item.is_file():
            continue
        if entry.get("bytes") != item.stat().st_size:
            fail(f"release manifest byte count mismatch for {entry['path']}")
        actual = sha256(item)
        if entry.get("sha256") != actual:
            fail(f"release manifest hash mismatch for {entry['path']}: {actual}")


def check_axiom_audit_denominator() -> None:
    declaration_files = sorted((ROOT / "src" / "IUT1").rglob("*.lean"))
    declaration_files += sorted((ROOT / "test" / "IUT1").rglob("*.lean"))
    public_names: list[str] = []
    declaration = re.compile(r"(?m)^\s*(theorem|instance)\s+([A-Za-z0-9_']+)\b")
    for path in declaration_files:
        public_names.extend(name for _, name in declaration.findall(path.read_text(encoding="utf-8")))
    audit_text = "\n".join(
        path.read_text(encoding="utf-8")
        for path in sorted((ROOT / "test").rglob("*.lean"))
    )
    missing = sorted(
        name for name in public_names
        if not re.search(rf"(?m)^#print axioms [A-Za-z0-9_.']*\.{re.escape(name)}\s*$", audit_text)
    )
    if missing:
        fail(f"public theorem/instance declarations lack #print axioms: {missing}")


def check_markdown_links() -> None:
    link_pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    for path in sorted(ROOT.rglob("*.md")):
        if any(part in IGNORED_DIRS for part in path.relative_to(ROOT).parts):
            continue
        for raw_target in link_pattern.findall(path.read_text(encoding="utf-8")):
            target = raw_target.strip().strip("<>")
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            file_part = target.split("#", 1)[0]
            if file_part and not (path.parent / file_part).resolve().exists():
                fail(f"broken relative link in {path.relative_to(ROOT)}: {raw_target}")


def check_public_boundary() -> None:
    forbidden_extensions = {".pdf", ".png", ".jpg", ".jpeg", ".tiff"}
    local_path = re.compile(r"[A-Za-z]:\\Users\\")
    secret = re.compile(r"(?:github_pat_[A-Za-z0-9_]{20,}|ghp_[A-Za-z0-9]{20,}|ARISTOTLE_API_KEY\s*=)")
    text_extensions = {
        ".md", ".json", ".jsonl", ".lean", ".toml", ".yml", ".yaml", ".py", ".cff"
    }
    for path in public_files():
        rel = path.relative_to(ROOT)
        if path.suffix.lower() in forbidden_extensions:
            fail(f"source/image redistribution boundary violated by {rel}")
        if path.suffix.lower() in text_extensions or path.name in {"LICENSE", "NOTICE"}:
            text = path.read_text(encoding="utf-8")
            if local_path.search(text):
                fail(f"absolute local path leaked in {rel}")
            if secret.search(text):
                fail(f"credential-shaped text leaked in {rel}")


def check_lean_escapes() -> None:
    active_escape = re.compile(r"(?m)^\s*(?:axiom|opaque|unsafe)\b|\b(?:sorry|admit|native_decide)\b")
    for tree in (ROOT / "src", ROOT / "test"):
        for path in sorted(tree.rglob("*.lean")):
            matches = active_escape.findall(path.read_text(encoding="utf-8"))
            if matches:
                fail(f"prohibited Lean escape token in {path.relative_to(ROOT)}: {matches}")


def check_gate_separation() -> None:
    gates = load_json(ROOT / "evidence" / "gates.json") or {}
    if gates.get("gate_transfer_allowed") is not False:
        fail("evidence/gates.json must state gate_transfer_allowed=false")
    for campaign in gates.get("campaigns", []):
        for field in ("semantic", "kernel", "fidelity", "cold_replication"):
            if campaign.get(field) != "PASS":
                fail(f"campaign {campaign.get('targets')} lacks explicit {field}=PASS")
    target_sets = {tuple(campaign.get("targets", [])) for campaign in gates.get("campaigns", [])}
    if ("PA01", "PA02", "PA03", "PA04", "PA05", "PA06") not in target_sets:
        fail("evidence/gates.json lacks a separate PA01-PA06 campaign")


def main() -> int:
    check_required_files()
    check_authorship_metadata()
    check_machine_layer()
    check_export_hashes()
    check_release_manifest()
    check_axiom_audit_denominator()
    check_markdown_links()
    check_public_boundary()
    check_lean_escapes()
    check_gate_separation()
    theorem_instance_count = 0
    declaration = re.compile(r"(?m)^\s*(?:theorem|instance)\s+[A-Za-z0-9_']+\b")
    declaration_files = sorted((ROOT / "src" / "IUT1").rglob("*.lean"))
    declaration_files += sorted((ROOT / "test" / "IUT1").rglob("*.lean"))
    for path in declaration_files:
        theorem_instance_count += len(declaration.findall(path.read_text(encoding="utf-8")))
    if theorem_instance_count != EXPECTED_PUBLIC_THEOREM_INSTANCES:
        fail(
            "public theorem/instance denominator is "
            f"{theorem_instance_count}, expected {EXPECTED_PUBLIC_THEOREM_INSTANCES}"
        )
    result = {
        "status": "PASS" if not ERRORS else "FAIL",
        "errors": ERRORS,
        "claims_expected": len(EXPECTED_CLAIMS),
        "public_theorem_instance_denominator": theorem_instance_count,
        "release_manifest_denominator": len(public_files()),
        "source_pdfs_redistributed": False,
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if not ERRORS else 1


if __name__ == "__main__":
    sys.exit(main())
