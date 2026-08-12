#!/usr/bin/env python3
"""Validate non-authoritative ND Oracle v0.1 -> v0.2 migration packages."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

try:
    from scripts.validate import v01_preservation_inventory
except ModuleNotFoundError:  # direct execution from scripts/
    from validate import v01_preservation_inventory

ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = {
    "manifest.json": ROOT / "schema" / "migration" / "manifest-v0.2.json",
    "preservation-ledger.json": ROOT / "schema" / "migration" / "preservation-ledger-v0.2.json",
    "enrichment-ledger.json": ROOT / "schema" / "migration" / "enrichment-ledger-v0.2.json",
    "dependency-ledger.json": ROOT / "schema" / "migration" / "dependency-ledger-v0.2.json",
}
READY_STATES = {"ready_for_authoritative_review", "accepted_for_authoritative_replacement"}
PLACEHOLDERS = {"", "tbd", "unknown", "n/a", "na", "placeholder", "to be determined", "not known"}


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def git_blob_sha(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def _schema_errors(name: str, value: Any) -> list[str]:
    schema = _load_json(SCHEMAS[name])
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    return [
        f"{name}: {'/'.join(str(part) for part in error.absolute_path) or '<root>'}: {error.message}"
        for error in sorted(validator.iter_errors(value), key=lambda item: list(item.absolute_path))
    ]


def _strings(value: Any):
    if isinstance(value, str):
        yield value
    elif isinstance(value, list):
        for item in value:
            yield from _strings(item)
    elif isinstance(value, dict):
        for item in value.values():
            yield from _strings(item)


def _has_placeholder(value: Any) -> bool:
    return any(text.strip().lower() in PLACEHOLDERS for text in _strings(value))


def _legacy_payload(unit: str) -> Any:
    prefix, sep, payload = unit.partition(":")
    if not sep or prefix == "object-id":
        raise ValueError("unit has no JSON legacy payload")
    return json.loads(payload)


def _candidate_json(package_dir: Path) -> list[dict]:
    candidate_dir = package_dir / "candidate"
    if not candidate_dir.exists():
        return []
    values: list[dict] = []
    for path in sorted(candidate_dir.rglob("*.json")):
        value = _load_json(path)
        if isinstance(value, dict):
            values.append(value)
    return values


def _entry_source_object_id(entry: dict, manifest: dict, errors: list[str]) -> str | None:
    source_id = entry.get("source_object_id")
    if source_id:
        return source_id
    sources = manifest["sources"]
    if len(sources) == 1:
        return sources[0]["object_id"]
    errors.append(
        f"preservation unit {entry.get('unit', '<missing>')}: multi-source package requires source_object_id"
    )
    return None


def validate_package(package_dir: Path, root: Path = ROOT) -> list[str]:
    package_dir = Path(package_dir)
    errors: list[str] = []
    docs: dict[str, Any] = {}

    for name in SCHEMAS:
        path = package_dir / name
        try:
            docs[name] = _load_json(path)
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"{name}: cannot load: {exc}")
            continue
        errors.extend(_schema_errors(name, docs[name]))

    if errors or len(docs) != len(SCHEMAS):
        return errors

    manifest = docs["manifest.json"]
    preservation = docs["preservation-ledger.json"]
    enrichment = docs["enrichment-ledger.json"]
    dependencies = docs["dependency-ledger.json"]

    expected_units: set[tuple[str, str]] = set()
    ecosystem_questions: set[str] = set()
    source_ids = {source["object_id"] for source in manifest["sources"]}
    if len(source_ids) != len(manifest["sources"]):
        errors.append("manifest.json: source object ids must be unique")

    for source in manifest["sources"]:
        source_path = root / source["path"]
        try:
            source_obj = _load_json(source_path)
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"source {source['path']}: cannot load: {exc}")
            continue
        actual_blob = git_blob_sha(source_path)
        if actual_blob != source["blob_sha"]:
            errors.append(
                f"source {source['path']}: blob drift: expected {source['blob_sha']} but found {actual_blob}"
            )
        if source_obj.get("schema_version") != source["schema_version"]:
            errors.append(f"source {source['path']}: schema version anchor does not match")
        if source_obj.get("id") != source["object_id"]:
            errors.append(f"source {source['path']}: object id anchor does not match")
        expected_units.update(
            (source["object_id"], unit) for unit in v01_preservation_inventory(source_obj)
        )
        for entry in source_obj.get("ecosystem_entry_points", []):
            ecosystem_questions.update(entry.get("questions", []))

    entries = preservation["entries"]
    entry_keys: list[tuple[str, str]] = []
    for entry in entries:
        source_id = _entry_source_object_id(entry, manifest, errors)
        if source_id is None:
            continue
        if source_id not in source_ids:
            errors.append(
                f"preservation unit {entry['unit']}: source_object_id {source_id} is not a manifest source"
            )
        entry_keys.append((source_id, entry["unit"]))

    if len(entry_keys) != len(set(entry_keys)):
        errors.append("preservation-ledger.json: every source-scoped preservation unit must appear exactly once")
    actual_units = set(entry_keys)
    missing = sorted(expected_units - actual_units)
    unknown = sorted(actual_units - expected_units)
    if missing:
        errors.append(f"preservation-ledger.json: omitted preservation units: {missing!r}")
    if unknown:
        errors.append(f"preservation-ledger.json: unknown preservation units: {unknown!r}")

    enrich_by_id = {entry["id"]: entry for entry in enrichment["entries"]}
    if len(enrich_by_id) != len(enrichment["entries"]):
        errors.append("enrichment-ledger.json: duplicate enrichment id")
    dependency_by_id = {entry["id"]: entry for entry in dependencies["entries"]}
    if len(dependency_by_id) != len(dependencies["entries"]):
        errors.append("dependency-ledger.json: duplicate dependency id")

    for item in enrichment["entries"]:
        if item["review_state"] == "verified":
            if not item["evidence_route"]:
                errors.append(f"enrichment {item['id']}: verified enrichment requires an evidence route")
            if item["value_origin"] not in {"verified_evidence", "owner_decision"}:
                errors.append(f"enrichment {item['id']}: verified enrichment has invalid value origin")
            if item.get("proposed_value") is None or _has_placeholder(item.get("proposed_value")):
                errors.append(f"enrichment {item['id']}: placeholder or missing value cannot satisfy enrichment")

    for entry in entries:
        disposition = entry["disposition"]
        if disposition == "represented_with_verified_enrichment":
            ref = entry.get("enrichment_ref")
            target = enrich_by_id.get(ref)
            if target is None or target.get("review_state") != "verified":
                errors.append(f"preservation unit {entry['unit']}: verified enrichment disposition lacks verified enrichment")
        elif disposition == "owner_decision_required":
            if not entry.get("unresolved_reason"):
                errors.append(f"preservation unit {entry['unit']}: owner decision requires unresolved reason")
        elif disposition == "structural_dependency":
            ref = entry.get("dependency_ref")
            if ref not in dependency_by_id:
                errors.append(f"preservation unit {entry['unit']}: structural dependency reference is missing")
        elif disposition == "legacy_retained_unmapped":
            if "legacy_value" not in entry:
                errors.append(f"preservation unit {entry['unit']}: legacy-unmapped unit must retain legacy_value")
            else:
                try:
                    expected = _legacy_payload(entry["unit"])
                except (ValueError, json.JSONDecodeError):
                    errors.append(f"preservation unit {entry['unit']}: cannot verify retained legacy value")
                else:
                    if entry["legacy_value"] != expected:
                        errors.append(f"preservation unit {entry['unit']}: retained legacy value does not match source unit")
        elif disposition == "rejected_with_reason":
            if not entry.get("owner_decision_ref") or not entry.get("rejection_reason") or not entry.get("reopening_condition"):
                errors.append(f"preservation unit {entry['unit']}: rejection requires owner decision, reason, and reopening condition")

        if entry["unit"].startswith("relation:") and '"type":"related_to"' in entry["unit"]:
            destination = (entry.get("candidate_destination") or "").lower()
            if "associated_with" in destination and not entry.get("owner_decision_ref"):
                errors.append(f"preservation unit {entry['unit']}: related_to cannot auto-map to associated_with")

    candidates = _candidate_json(package_dir)
    for candidate in candidates:
        if candidate.get("type") == "question" and not candidate.get("migration_owner_decision_ref"):
            candidate_text = set(_strings(candidate))
            promoted = sorted(candidate_text & ecosystem_questions)
            if promoted:
                errors.append(f"candidate Question auto-promotes ecosystem entry text without owner decision: {promoted!r}")

    status = manifest["package_status"]
    pending_enrichment = [item["id"] for item in enrichment["entries"] if item["review_state"] == "pending"]
    unresolved_dependencies = [item["id"] for item in dependencies["entries"] if item["resolution_status"] != "resolved"]
    unresolved_dispositions = [
        entry["unit"]
        for entry in entries
        if entry["disposition"] in {"owner_decision_required", "structural_dependency", "legacy_retained_unmapped"}
    ]
    if status in READY_STATES:
        if pending_enrichment:
            errors.append(f"manifest.json: {status} blocked by pending enrichment {pending_enrichment!r}")
        if unresolved_dependencies:
            errors.append(f"manifest.json: {status} blocked by structural dependencies {unresolved_dependencies!r}")
        if unresolved_dispositions:
            errors.append(f"manifest.json: {status} blocked by unresolved preservation dispositions")

    return errors


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if len(args) != 1:
        print("usage: python scripts/validate_migration.py <migration-package-directory>", file=sys.stderr)
        return 2
    errors = validate_package(Path(args[0]))
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print(f"Migration package valid: {args[0]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
