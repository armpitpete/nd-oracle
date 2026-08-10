#!/usr/bin/env python3
"""JSON Schema, governance-route, and graph checks for ND Oracle v0.1."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
ALLOWED_CONFIDENCE = {"high", "moderate", "low", "contested", "not_applicable"}


def validate_object(path: Path, obj: dict, all_ids: set[str], root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    label = path.relative_to(root).as_posix()
    if path.stem != obj["id"]:
        errors.append(f"{label}: filename must match object id")

    source_ids = {item.get("id") for item in obj["sources"]}
    uncertainty_ids = {item.get("id") for item in obj["uncertainties"]}
    claim_ids = {item.get("id") for item in obj["claims"]}
    perspective_ids = {item.get("id") for item in obj["perspectives"]}
    sources_by_id = {item.get("id"): item for item in obj["sources"]}
    claims_by_id = {item.get("id"): item for item in obj["claims"]}
    perspectives_by_id = {item.get("id"): item for item in obj["perspectives"]}
    if len(source_ids) != len(obj["sources"]):
        errors.append(f"{label}: duplicate source id")
    if len(uncertainty_ids) != len(obj["uncertainties"]):
        errors.append(f"{label}: duplicate uncertainty id")
    if len(claim_ids) != len(obj["claims"]):
        errors.append(f"{label}: duplicate claim id")
    if len(perspective_ids) != len(obj["perspectives"]):
        errors.append(f"{label}: duplicate perspective id")
    internal_ids = [
        item.get("id")
        for category in ("claims", "sources", "uncertainties", "perspectives")
        for item in obj[category]
    ]
    if len(internal_ids) != len(set(internal_ids)):
        errors.append(f"{label}: internal ids must be unique across the object")

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
            elif cid not in sources_by_id[sid].get("supports", []):
                errors.append(f"{label}: source {sid} does not list claim {cid} in supports")
        for uid in claim.get("uncertainty_ids", []):
            if uid not in uncertainty_ids:
                errors.append(f"{label}: {cid} references missing uncertainty {uid}")

    for source in obj["sources"]:
        for supported in source.get("supports", []):
            if supported not in claim_ids | perspective_ids:
                errors.append(f"{label}: source {source.get('id')} supports missing item {supported}")
            elif supported in claims_by_id and source.get("id") not in claims_by_id[supported].get("source_ids", []):
                errors.append(f"{label}: claim {supported} does not reference supporting source {source.get('id')}")
            elif supported in perspectives_by_id and source.get("id") not in perspectives_by_id[supported].get("source_ids", []):
                errors.append(f"{label}: perspective {supported} does not reference supporting source {source.get('id')}")
        if not str(source.get("url", "")).startswith("https://"):
            errors.append(f"{label}: source {source.get('id')} requires an HTTPS URL")

    for perspective in obj["perspectives"]:
        for sid in perspective.get("source_ids", []):
            if sid not in source_ids:
                errors.append(f"{label}: perspective {perspective.get('id')} references missing source {sid}")
            elif perspective.get("id") not in sources_by_id[sid].get("supports", []):
                errors.append(f"{label}: source {sid} does not list perspective {perspective.get('id')} in supports")

    for relation in obj["relations"]:
        if relation.get("target_id") not in all_ids:
            errors.append(f"{label}: relation references missing object {relation.get('target_id')}")
    return errors


def validate_repository(root: Path = ROOT) -> tuple[int, list[str]]:
    objects = root / "objects"
    schema_path = root / "schema" / "object-v0.1.json"
    try:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
    except (OSError, json.JSONDecodeError) as exc:
        return 0, [f"cannot load schema: {exc}"]
    except Exception as exc:
        return 0, [f"invalid schema: {exc}"]
    schema_validator = Draft202012Validator(schema, format_checker=FormatChecker())
    paths = sorted(objects.rglob("*.json"))
    if not paths:
        return 0, ["no knowledge objects found"]
    loaded: list[tuple[Path, dict]] = []
    errors: list[str] = []
    for path in paths:
        try:
            obj = json.loads(path.read_text(encoding="utf-8"))
            schema_errors = sorted(schema_validator.iter_errors(obj), key=lambda item: list(item.absolute_path))
            if schema_errors:
                label = path.relative_to(root).as_posix()
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
        errors.extend(validate_object(path, obj, all_ids, root))
    return len(loaded), errors


def main() -> int:
    object_count, errors = validate_repository()
    if errors:
        print("Validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print(f"Validated {object_count} objects against schema v0.1; all evidence, uncertainty, perspective, and graph routes resolve.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
