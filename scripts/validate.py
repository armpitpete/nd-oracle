#!/usr/bin/env python3
"""Dependency-free structural and graph checks for ND Oracle v0.1."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OBJECTS = ROOT / "objects"
REQUIRED = {
    "schema_version", "id", "type", "name", "status", "summary", "scope",
    "claims", "sources", "uncertainties", "perspectives", "relations",
    "ecosystem_entry_points", "provenance",
}
ID_PATTERN = re.compile(r"^[a-z][a-z0-9-]*$")
ALLOWED_CONFIDENCE = {"high", "moderate", "low", "contested", "not_applicable"}


def validate_object(path: Path, obj: dict, all_ids: set[str]) -> list[str]:
    errors: list[str] = []
    label = path.relative_to(ROOT).as_posix()
    missing = REQUIRED - obj.keys()
    if missing:
        errors.append(f"{label}: missing fields {sorted(missing)}")
        return errors
    if obj["schema_version"] != "0.1":
        errors.append(f"{label}: schema_version must be 0.1")
    if not ID_PATTERN.fullmatch(obj["id"]):
        errors.append(f"{label}: invalid stable id {obj['id']!r}")
    if path.stem != obj["id"]:
        errors.append(f"{label}: filename must match object id")

    source_ids = {item.get("id") for item in obj["sources"]}
    uncertainty_ids = {item.get("id") for item in obj["uncertainties"]}
    claim_ids = {item.get("id") for item in obj["claims"]}
    if len(source_ids) != len(obj["sources"]):
        errors.append(f"{label}: duplicate source id")
    if len(uncertainty_ids) != len(obj["uncertainties"]):
        errors.append(f"{label}: duplicate uncertainty id")
    if len(claim_ids) != len(obj["claims"]):
        errors.append(f"{label}: duplicate claim id")

    for claim in obj["claims"]:
        cid = claim.get("id", "<missing>")
        if claim.get("confidence") not in ALLOWED_CONFIDENCE:
            errors.append(f"{label}: {cid} has invalid confidence")
        if not claim.get("source_ids"):
            errors.append(f"{label}: {cid} has no evidence route")
        if not claim.get("uncertainty_ids"):
            errors.append(f"{label}: {cid} has no uncertainty route")
        for sid in claim.get("source_ids", []):
            if sid not in source_ids:
                errors.append(f"{label}: {cid} references missing source {sid}")
        for uid in claim.get("uncertainty_ids", []):
            if uid not in uncertainty_ids:
                errors.append(f"{label}: {cid} references missing uncertainty {uid}")

    for source in obj["sources"]:
        for supported in source.get("supports", []):
            perspective_ids = {item.get("id") for item in obj["perspectives"]}
            if supported not in claim_ids | perspective_ids:
                errors.append(f"{label}: source {source.get('id')} supports missing item {supported}")
        if not str(source.get("url", "")).startswith("https://"):
            errors.append(f"{label}: source {source.get('id')} requires an HTTPS URL")

    for perspective in obj["perspectives"]:
        for sid in perspective.get("source_ids", []):
            if sid not in source_ids:
                errors.append(f"{label}: perspective {perspective.get('id')} references missing source {sid}")

    for relation in obj["relations"]:
        if relation.get("target_id") not in all_ids:
            errors.append(f"{label}: relation references missing object {relation.get('target_id')}")
    return errors


def main() -> int:
    paths = sorted(OBJECTS.rglob("*.json"))
    if not paths:
        print("ERROR: no knowledge objects found", file=sys.stderr)
        return 1
    loaded: list[tuple[Path, dict]] = []
    errors: list[str] = []
    for path in paths:
        try:
            loaded.append((path, json.loads(path.read_text(encoding="utf-8"))))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"{path}: {exc}")
    ids = [obj.get("id") for _, obj in loaded]
    if len(ids) != len(set(ids)):
        errors.append("duplicate object id across repository")
    all_ids = set(ids)
    for path, obj in loaded:
        errors.extend(validate_object(path, obj, all_ids))
    if errors:
        print("Validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print(f"Validated {len(loaded)} objects; all evidence, uncertainty, perspective, and graph routes resolve.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
