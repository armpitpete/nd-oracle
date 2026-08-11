#!/usr/bin/env python3
"""JSON Schema, governance-route, and graph checks for ND Oracle v0.1 + v0.2."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Iterable

from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parents[1]
ALLOWED_CONFIDENCE = {"high", "moderate", "low", "contested", "not_applicable"}
V02_TYPES = {"concept", "evidence", "question", "resource", "perspective", "experience"}
V02_DIRECTORIES = {
    "concept": "concepts",
    "evidence": "evidence",
    "question": "questions",
    "resource": "resources",
    "perspective": "perspectives",
    "experience": "experiences",
}
STRUCTURAL_INVERSES = {"broader_than": "narrower_than", "narrower_than": "broader_than"}


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _relative_label(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def load_schema_validators(root: Path = ROOT) -> tuple[dict[str, Draft202012Validator], list[str]]:
    errors: list[str] = []
    schema_dir = root / "schema"
    schema_paths = [
        schema_dir / "object-v0.1.json",
        schema_dir / "common-v0.2.json",
        schema_dir / "object-v0.2.json",
        *(schema_dir / "types" / f"{name}-v0.2.json" for name in sorted(V02_TYPES)),
    ]
    schemas: dict[Path, dict] = {}
    for path in schema_paths:
        try:
            schema = _load_json(path)
            Draft202012Validator.check_schema(schema)
            schemas[path] = schema
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"cannot load schema {_relative_label(path, root)}: {exc}")
        except Exception as exc:
            errors.append(f"invalid schema {_relative_label(path, root)}: {exc}")
    if errors:
        return {}, errors

    registry = Registry()
    for schema in schemas.values():
        schema_id = schema.get("$id")
        if schema_id:
            registry = registry.with_resource(schema_id, Resource.from_contents(schema))

    checker = FormatChecker()
    return {
        "0.1": Draft202012Validator(schemas[schema_dir / "object-v0.1.json"], format_checker=checker),
        "0.2": Draft202012Validator(
            schemas[schema_dir / "object-v0.2.json"],
            registry=registry,
            format_checker=checker,
        ),
    }, []


def validate_v01_object(path: Path, obj: dict, all_ids: set[str], root: Path = ROOT) -> list[str]:
    """Preserve the established v0.1 semantic checks unchanged."""
    errors: list[str] = []
    label = _relative_label(path, root)
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


validate_object = validate_v01_object


def _expected_directory(path: Path, fixture_root: Path | None, root: Path) -> str | None:
    if fixture_root is not None:
        try:
            rel = path.relative_to(fixture_root)
            return rel.parts[0] if len(rel.parts) > 1 else None
        except ValueError:
            pass
    try:
        rel = path.relative_to(root / "objects")
        return rel.parts[0] if len(rel.parts) > 1 else None
    except ValueError:
        return None


def _claim_records(obj: dict) -> dict[str, dict]:
    return {item.get("id"): item for item in obj.get("claims", []) if item.get("id")}


def _embedded_ids_v02(obj: dict) -> list[str]:
    ids: list[str] = []
    for claim in obj.get("claims", []):
        if claim.get("id"):
            ids.append(claim["id"])
        ids.extend(item["id"] for item in claim.get("uncertainties", []) if item.get("id"))
    for relation in obj.get("relations", []):
        ids.extend(item["id"] for item in relation.get("uncertainties", []) if item.get("id"))
    for contribution in obj.get("contributions", []):
        if contribution.get("id"):
            ids.append(contribution["id"])
        ids.extend(item["id"] for item in contribution.get("limitations", []) if item.get("id"))
    return ids


def _resolve_typed_ref(label: str, ref: dict, objects_by_id: dict[str, dict], errors: list[str], context: str) -> None:
    target_id = ref.get("id")
    target_type = ref.get("type")
    target = objects_by_id.get(target_id)
    if target is None:
        errors.append(f"{label}: {context} references missing object {target_id}")
    elif target.get("type") != target_type:
        errors.append(f"{label}: {context} expects {target_type} {target_id} but found {target.get('type')}")


def _require_typed_id(label: str, target_id: str, expected_type: str, objects_by_id: dict[str, dict], errors: list[str], context: str) -> None:
    target = objects_by_id.get(target_id)
    if target is None:
        errors.append(f"{label}: {context} references missing {expected_type} {target_id}")
    elif target.get("type") != expected_type or target.get("schema_version") != "0.2":
        errors.append(f"{label}: {context} expects v0.2 {expected_type} {target_id} but found {target.get('schema_version')} {target.get('type')}")


def _parse_claim_ref(label: str, claim_ref: str, objects_by_id: dict[str, dict], errors: list[str], context: str) -> tuple[dict | None, dict | None]:
    if not re.fullmatch(r"[a-z][a-z0-9-]*#[a-z][a-z0-9-]*", claim_ref or ""):
        errors.append(f"{label}: {context} has malformed claim reference {claim_ref}")
        return None, None
    object_id, claim_id = claim_ref.split("#", 1)
    target = objects_by_id.get(object_id)
    if target is None:
        errors.append(f"{label}: {context} references missing claim owner {object_id}")
        return None, None
    if target.get("schema_version") != "0.2" or target.get("type") not in {"concept", "resource"}:
        errors.append(f"{label}: {context} references object {object_id} that is not a v0.2 claim owner")
        return target, None
    claim = _claim_records(target).get(claim_id)
    if claim is None:
        errors.append(f"{label}: {context} references missing claim {claim_ref}")
    return target, claim


def validate_v02_object(path: Path, obj: dict, objects_by_id: dict[str, dict], root: Path = ROOT, fixture_root: Path | None = None) -> list[str]:
    errors: list[str] = []
    label = _relative_label(path, root)
    object_id = obj.get("id")
    object_type = obj.get("type")

    if path.stem != object_id:
        errors.append(f"{label}: filename must match object id")
    expected_dir = V02_DIRECTORIES.get(object_type)
    actual_dir = _expected_directory(path, fixture_root, root)
    if expected_dir and actual_dir != expected_dir:
        errors.append(f"{label}: {object_type} object must be stored under {expected_dir}/")

    if object_type not in {"concept", "resource"} and "claims" in obj:
        errors.append(f"{label}: {object_type} objects may not own claims in v0.2")

    local_ids = _embedded_ids_v02(obj)
    if len(local_ids) != len(set(local_ids)):
        errors.append(f"{label}: duplicate local id within object")

    for claim in obj.get("claims", []):
        claim_ref = f"{object_id}#{claim.get('id')}"
        for evidence_id in claim.get("evidence_ids", []):
            _require_typed_id(label, evidence_id, "evidence", objects_by_id, errors, f"claim {claim.get('id')}")
            evidence = objects_by_id.get(evidence_id)
            if evidence and evidence.get("type") == "evidence":
                if not any(c.get("claim_ref") == claim_ref for c in evidence.get("contributions", [])):
                    errors.append(f"{label}: evidence {evidence_id} has no contribution for claim {claim_ref}")
        for question_id in claim.get("question_ids", []):
            _require_typed_id(label, question_id, "question", objects_by_id, errors, f"claim {claim.get('id')}")

    for question_id in obj.get("question_ids", []):
        _require_typed_id(label, question_id, "question", objects_by_id, errors, object_type)
    for evidence_id in obj.get("evidence_ids", []):
        _require_typed_id(label, evidence_id, "evidence", objects_by_id, errors, object_type)
    for experience_id in obj.get("experience_ids", []):
        _require_typed_id(label, experience_id, "experience", objects_by_id, errors, object_type)
    for evidence_id in obj.get("resolution_evidence_ids", []):
        _require_typed_id(label, evidence_id, "evidence", objects_by_id, errors, "question resolution")

    for field in ("related_objects", "supporting_material_refs", "disagreement_refs"):
        for ref in obj.get(field, []):
            _resolve_typed_ref(label, ref, objects_by_id, errors, field)

    if object_type == "evidence":
        for contribution in obj.get("contributions", []):
            claim_ref = contribution.get("claim_ref", "")
            _, claim = _parse_claim_ref(label, claim_ref, objects_by_id, errors, f"contribution {contribution.get('id')}")
            if claim is not None and object_id not in claim.get("evidence_ids", []):
                errors.append(f"{label}: claim {claim_ref} does not reference evidence {object_id}")

    for relation in obj.get("relations", []):
        target_ref = relation.get("target", {})
        _resolve_typed_ref(label, target_ref, objects_by_id, errors, f"relation {relation.get('type')}")
        for evidence_id in relation.get("evidence_ids", []):
            _require_typed_id(label, evidence_id, "evidence", objects_by_id, errors, f"relation {relation.get('type')}")
        for question_id in relation.get("question_ids", []):
            _require_typed_id(label, question_id, "question", objects_by_id, errors, f"relation {relation.get('type')}")

        inverse = STRUCTURAL_INVERSES.get(relation.get("type"))
        if inverse:
            if object_type != "concept" or target_ref.get("type") != "concept":
                errors.append(f"{label}: structural relation {relation.get('type')} must connect concepts")
                continue
            target = objects_by_id.get(target_ref.get("id"))
            if target is not None and target.get("type") == "concept":
                reciprocal = any(candidate.get("type") == inverse and candidate.get("target", {}).get("type") == "concept" and candidate.get("target", {}).get("id") == object_id for candidate in target.get("relations", []))
                if not reciprocal:
                    errors.append(f"{label}: {relation.get('type')} to {target_ref.get('id')} requires reciprocal {inverse}")
    return errors


def v01_preservation_inventory(obj: dict) -> set[str]:
    """Return deterministic preservation units for a v0.1 concept without performing migration."""
    units: set[str] = set()
    units.add(f"object-id:{obj.get('id')}")
    units.add("summary:" + json.dumps(obj.get("summary"), sort_keys=True))
    for alias in obj.get("aliases", []):
        units.add("alias:" + json.dumps(alias, sort_keys=True))
    scope = obj.get("scope", {})
    for value in scope.get("includes", []):
        units.add("scope-includes:" + json.dumps(value, sort_keys=True))
    for value in scope.get("excludes", []):
        units.add("scope-excludes:" + json.dumps(value, sort_keys=True))
    for claim in obj.get("claims", []):
        cid = claim.get("id")
        units.add("claim:" + json.dumps({"id": cid, "text": claim.get("text"), "confidence": claim.get("confidence")}, sort_keys=True))
        for source_id in claim.get("source_ids", []):
            units.add(f"claim-source-route:{cid}->{source_id}")
        for uncertainty_id in claim.get("uncertainty_ids", []):
            units.add(f"claim-uncertainty-route:{cid}->{uncertainty_id}")
    for source in obj.get("sources", []):
        units.add("source:" + json.dumps(source, sort_keys=True, separators=(",", ":")))
    for uncertainty in obj.get("uncertainties", []):
        units.add("uncertainty:" + json.dumps(uncertainty, sort_keys=True, separators=(",", ":")))
    for perspective in obj.get("perspectives", []):
        units.add("perspective:" + json.dumps(perspective, sort_keys=True, separators=(",", ":")))
    for relation in obj.get("relations", []):
        units.add("relation:" + json.dumps(relation, sort_keys=True, separators=(",", ":")))
    for entry in obj.get("ecosystem_entry_points", []):
        units.add("ecosystem-entry:" + json.dumps(entry, sort_keys=True, separators=(",", ":")))
    for key, value in sorted(obj.get("provenance", {}).items()):
        units.add(f"provenance:{key}=" + json.dumps(value, sort_keys=True))
    return units


def missing_v01_preservation_units(obj: dict, preserved_units: set[str]) -> list[str]:
    """Identify unaccounted-for v0.1 semantic units in a migration proof manifest."""
    return sorted(v01_preservation_inventory(obj) - set(preserved_units))


def _load_object_paths(paths: Iterable[Path], root: Path, errors: list[str]) -> list[tuple[Path, dict]]:
    loaded: list[tuple[Path, dict]] = []
    for path in sorted(paths):
        try:
            obj = _load_json(path)
            if not isinstance(obj, dict):
                errors.append(f"{_relative_label(path, root)}: top level must be an object")
            else:
                loaded.append((path, obj))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"{_relative_label(path, root)}: {exc}")
    return loaded


def validate_repository(root: Path = ROOT, fixture_root: Path | None = None) -> tuple[int, list[str]]:
    validators, errors = load_schema_validators(root)
    if errors:
        return 0, errors

    authoritative_paths = sorted((root / "objects").rglob("*.json"))
    if not authoritative_paths:
        return 0, ["no knowledge objects found"]

    loaded = _load_object_paths(authoritative_paths, root, errors)
    if fixture_root is not None:
        loaded.extend(_load_object_paths(sorted(fixture_root.rglob("*.json")), root, errors))

    schema_valid: list[tuple[Path, dict]] = []
    for path, obj in loaded:
        version = obj.get("schema_version")
        validator = validators.get(version)
        label = _relative_label(path, root)
        if validator is None:
            errors.append(f"{label}: unsupported schema_version {version!r}")
            continue
        schema_errors = sorted(validator.iter_errors(obj), key=lambda item: [str(part) for part in item.absolute_path])
        if schema_errors:
            for error in schema_errors:
                location = ".".join(str(part) for part in error.absolute_path) or "<root>"
                errors.append(f"{label}: schema {location}: {error.message}")
        else:
            schema_valid.append((path, obj))

    ids = [obj.get("id") for _, obj in schema_valid]
    if len(ids) != len(set(ids)):
        errors.append("duplicate object id across repository")
    objects_by_id = {obj.get("id"): obj for _, obj in schema_valid if obj.get("id")}
    all_ids = set(objects_by_id)

    for path, obj in schema_valid:
        if obj.get("schema_version") == "0.1":
            expected = _expected_directory(path, fixture_root, root)
            if obj.get("type") != "concept" or expected != "concepts":
                errors.append(f"{_relative_label(path, root)}: v0.1 objects must be concepts under concepts/")
            errors.extend(validate_v01_object(path, obj, all_ids, root))
        else:
            errors.extend(validate_v02_object(path, obj, objects_by_id, root, fixture_root))

    return len(authoritative_paths), errors


def main() -> int:
    object_count, errors = validate_repository()
    if errors:
        print("Validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print(f"Validated {object_count} authoritative objects across supported schema versions; all governed evidence, uncertainty, perspective, reference, and graph routes resolve.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
