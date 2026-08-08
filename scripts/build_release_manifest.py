#!/usr/bin/env python3
"""Regenerate the deterministic public-file manifest (the manifest excludes itself)."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "evidence" / "release-manifest.json"
IGNORED_DIRS = {".git", ".lake", "build", "__pycache__"}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


files = sorted(
    path for path in ROOT.rglob("*")
    if path.is_file()
    and path != OUTPUT
    and not any(part in IGNORED_DIRS for part in path.relative_to(ROOT).parts)
)
document = {
    "schema_version": "1.0.0",
    "self_exclusion": "evidence/release-manifest.json is excluded to avoid a recursive hash",
    "ignored_directories": sorted(IGNORED_DIRS),
    "files": [
        {
            "path": path.relative_to(ROOT).as_posix(),
            "bytes": path.stat().st_size,
            "sha256": sha256(path),
        }
        for path in files
    ],
}
OUTPUT.write_bytes(
    (json.dumps(document, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
)
print(json.dumps({"status": "GENERATED", "files": len(files), "output": OUTPUT.name}))
