#!/usr/bin/env python3
"""JSON Schema, governance-route, and graph checks for ND Oracle v0.1."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
OBJECTS = ROOT / "objects"
SCHEMA_PATH = ROOT / "schema" / "object-v0.1.json"
ALLOWED_CONFIDENCE = {"high", "moderate", "low", "contested", "not_applicable"}


def validate_object(path: Path, obj: dict, all_ids: set[str]) -> list[str]:
    errors: list[str] = []
    label = path.relative_to(ROOT).as_posix()
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
    try:
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: cannot load schema: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:
        print(f"ERROR: invalid schema: {exc}", file=sys.stderr)
        return 1
    schema_validator = Draft202012Validator(schema, format_checker=FormatChecker())
    paths = sorted(OBJECTS.rglob("*.json"))
    if not paths:
        print("ERROR: no knowledge objects found", file=sys.stderr)
        return 1
    loaded: list[tuple[Path, dict]] = []
    errors: list[str] = []
    for path in paths:
        try:
            obj = json.loads(path.read_text(encoding="utf-8"))
            schema_errors = sorted(schema_validator.iter_errors(obj), key=lambda item: list(item.absolute_path))
            if schema_errors:
                label = path.relative_to(ROOT).as_posix()
                for error in schema_errors:
                    location = ".".join(str(part) for part in error.absolute_path) or "<root>"
                    errors.append(f"{label}: schema {location}: {error.message}")
            elif isinstance(obj, dict):
                loaded.append((path, obj))
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
    print(f"Validated {len(loaded)} objects against schema v0.1; all evidence, uncertainty, perspective, and graph routes resolve.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
