#!/usr/bin/env python3
"""Generate a machine-readable Evidence coverage registry for ND Oracle.

This inventory intentionally supports both evidence models currently accepted
by the repository:
- v0.1 Concepts with embedded source records and reciprocal source_ids/supports;
- v0.2 Concepts/Resources with top-level Evidence objects and claim-specific
  Evidence Contributions.

The registry is an audit/projection. It does not migrate or strengthen claims.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OBJECTS = ROOT / "objects"

TRIAGE_TERMS = {
    "possible_diagnostic": ("diagnos", "diagnostic", "criterion", "criteria"),
    "possible_efficacy": ("effective", "efficacy", "improve", "reduces", "reduce ", "benefit"),
    "possible_safety": ("safe", "safety", "harm", "adverse", "risk"),
    "possible_legal_or_entitlement": ("legal", "law", "eligible", "eligibility", "entitlement", "required"),
    "possible_prevalence": ("prevalence", "percent", "percentage", "common", "majority"),
    "possible_causal_or_mechanistic": ("cause", "causal", "mechanism", "leads to", "results in"),
}


def _load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _object_files(root: Path) -> list[Path]:
    objects = root / "objects"
    if not objects.is_dir():
        return []
    return sorted(objects.glob("*/*.json"))


def _triage_flags(text: str) -> list[str]:
    lowered = text.casefold()
    return sorted(
        label
        for label, terms in TRIAGE_TERMS.items()
        if any(term in lowered for term in terms)
    )


def _claim_review_state(obj: dict[str, Any], as_of: date) -> dict[str, Any]:
    raw = obj.get("provenance", {}).get("last_reviewed")
    try:
        reviewed = date.fromisoformat(raw) if raw else None
    except (TypeError, ValueError):
        reviewed = None
    return {
        "last_reviewed": reviewed.isoformat() if reviewed else None,
        "review_age_days": (as_of - reviewed).days if reviewed else None,
    }


def build_registry(root: Path = ROOT, *, as_of: date | None = None) -> dict[str, Any]:
    if as_of is None:
        as_of = date.today()

    objects_by_id: dict[str, dict[str, Any]] = {}
    object_paths: dict[str, str] = {}
    for path in _object_files(root):
        obj = _load(path)
        object_id = obj.get("id")
        if object_id:
            objects_by_id[object_id] = obj
            object_paths[object_id] = path.relative_to(root).as_posix()

    evidence_objects = {
        object_id: obj
        for object_id, obj in objects_by_id.items()
        if obj.get("schema_version") == "0.2" and obj.get("type") == "evidence"
    }

    source_catalog: dict[str, dict[str, Any]] = {}
    claim_rows: list[dict[str, Any]] = []
    errors: list[str] = []

    for owner_id, obj in sorted(objects_by_id.items()):
        if obj.get("type") not in {"concept", "resource"}:
            continue
        schema_version = obj.get("schema_version")
        claims = obj.get("claims", [])
        review = _claim_review_state(obj, as_of)

        if schema_version == "0.1":
            source_map = {source.get("id"): source for source in obj.get("sources", [])}
            for source_id, source in sorted(source_map.items()):
                key = f"legacy:{owner_id}:{source_id}"
                source_catalog[key] = {
                    "evidence_model": "legacy_v0.1_embedded",
                    "evidence_id": key,
                    "source_id": source_id,
                    "owner_id": owner_id,
                    "owner_path": object_paths[owner_id],
                    "source_kind": source.get("kind"),
                    "citation": source.get("citation"),
                    "locator": {"type": "url", "value": source.get("url")} if source.get("url") else None,
                    "doi": source.get("doi"),
                    "accessed": source.get("accessed"),
                    "referenced_by_claims": [],
                }

            for claim in claims:
                claim_id = claim.get("id")
                claim_ref = f"{owner_id}#{claim_id}"
                source_ids = list(claim.get("source_ids", []))
                missing = [source_id for source_id in source_ids if source_id not in source_map]
                nonreciprocal = [
                    source_id
                    for source_id in source_ids
                    if source_id in source_map and claim_id not in source_map[source_id].get("supports", [])
                ]
                for source_id in source_ids:
                    key = f"legacy:{owner_id}:{source_id}"
                    if key in source_catalog:
                        source_catalog[key]["referenced_by_claims"].append(claim_ref)

                uncertainty_ids = list(claim.get("uncertainty_ids", []))
                covered = bool(source_ids) and not missing and not nonreciprocal and bool(uncertainty_ids)
                if not covered:
                    errors.append(
                        f"{claim_ref}: legacy coverage gap missing={missing} nonreciprocal={nonreciprocal} "
                        f"uncertainty_routes={len(uncertainty_ids)}"
                    )
                claim_rows.append(
                    {
                        "claim_ref": claim_ref,
                        "owner_id": owner_id,
                        "owner_type": obj.get("type"),
                        "owner_path": object_paths[owner_id],
                        "schema_version": "0.1",
                        "evidence_model": "legacy_v0.1_embedded",
                        "claim_text": claim.get("text"),
                        "confidence": claim.get("confidence"),
                        "coverage_status": "covered" if covered else "gap",
                        "evidence_routes": [f"legacy:{owner_id}:{source_id}" for source_id in source_ids],
                        "source_count": len(source_ids),
                        "source_kinds": sorted(
                            {source_map[source_id].get("kind") for source_id in source_ids if source_id in source_map}
                        ),
                        "contribution_roles": [],
                        "uncertainty_route_count": len(uncertainty_ids),
                        "triage_flags": _triage_flags(str(claim.get("text", ""))),
                        "semantic_classification": "editorial_not_machine_inferred",
                        **review,
                    }
                )
            continue

        if schema_version == "0.2":
            for claim in claims:
                claim_id = claim.get("id")
                claim_ref = f"{owner_id}#{claim_id}"
                evidence_ids = list(claim.get("evidence_ids", []))
                source_kinds: set[str] = set()
                roles: list[str] = []
                missing: list[str] = []
                missing_contributions: list[str] = []
                for evidence_id in evidence_ids:
                    evidence = evidence_objects.get(evidence_id)
                    if evidence is None:
                        missing.append(evidence_id)
                        continue
                    source_kinds.add(str(evidence.get("source_kind")))
                    matches = [
                        contribution
                        for contribution in evidence.get("contributions", [])
                        if contribution.get("claim_ref") == claim_ref
                    ]
                    if not matches:
                        missing_contributions.append(evidence_id)
                    roles.extend(
                        str(contribution.get("role"))
                        for contribution in matches
                        if contribution.get("role")
                    )
                uncertainties = list(claim.get("uncertainties", []))
                covered = (
                    bool(evidence_ids)
                    and not missing
                    and not missing_contributions
                    and bool(uncertainties)
                )
                if not covered:
                    errors.append(
                        f"{claim_ref}: v0.2 coverage gap missing={missing} "
                        f"missing_contributions={missing_contributions} uncertainties={len(uncertainties)}"
                    )
                claim_rows.append(
                    {
                        "claim_ref": claim_ref,
                        "owner_id": owner_id,
                        "owner_type": obj.get("type"),
                        "owner_path": object_paths[owner_id],
                        "schema_version": "0.2",
                        "evidence_model": "normalized_v0.2",
                        "claim_text": claim.get("text"),
                        "confidence": claim.get("confidence"),
                        "coverage_status": "covered" if covered else "gap",
                        "evidence_routes": evidence_ids,
                        "source_count": len(evidence_ids),
                        "source_kinds": sorted(source_kinds),
                        "contribution_roles": sorted(set(roles)),
                        "uncertainty_route_count": len(uncertainties),
                        "triage_flags": _triage_flags(str(claim.get("text", ""))),
                        "semantic_classification": "editorial_not_machine_inferred",
                        **review,
                    }
                )

    for evidence_id, evidence in sorted(evidence_objects.items()):
        source_catalog[evidence_id] = {
            "evidence_model": "normalized_v0.2",
            "evidence_id": evidence_id,
            "owner_id": None,
            "owner_path": object_paths[evidence_id],
            "source_kind": evidence.get("source_kind"),
            "citation": evidence.get("citation"),
            "locator": evidence.get("locator"),
            "doi": evidence.get("locator", {}).get("value")
            if evidence.get("locator", {}).get("type") == "doi"
            else None,
            "accessed": evidence.get("accessed"),
            "referenced_by_claims": sorted(
                {
                    contribution.get("claim_ref")
                    for contribution in evidence.get("contributions", [])
                    if contribution.get("claim_ref")
                }
            ),
        }

    source_kind_counts = Counter(
        str(source.get("source_kind"))
        for source in source_catalog.values()
        if source.get("source_kind")
    )
    evidence_model_counts = Counter(row["evidence_model"] for row in claim_rows)
    confidence_counts = Counter(str(row.get("confidence")) for row in claim_rows)
    triage_counts = Counter(flag for row in claim_rows for flag in row["triage_flags"])
    coverage_counts = Counter(row["coverage_status"] for row in claim_rows)

    normalized_orphans = sorted(
        evidence_id
        for evidence_id, evidence in evidence_objects.items()
        if not evidence.get("contributions")
        or not source_catalog[evidence_id]["referenced_by_claims"]
    )
    if normalized_orphans:
        errors.extend(f"{evidence_id}: normalized Evidence object has no claim contribution" for evidence_id in normalized_orphans)

    summary = {
        "as_of": as_of.isoformat(),
        "total_claims": len(claim_rows),
        "covered_claims": coverage_counts.get("covered", 0),
        "gap_claims": coverage_counts.get("gap", 0),
        "claims_with_multiple_source_routes": sum(row["source_count"] >= 2 for row in claim_rows),
        "legacy_v0.1_claims": evidence_model_counts.get("legacy_v0.1_embedded", 0),
        "normalized_v0.2_claims": evidence_model_counts.get("normalized_v0.2", 0),
        "legacy_embedded_sources": sum(
            source["evidence_model"] == "legacy_v0.1_embedded"
            for source in source_catalog.values()
        ),
        "normalized_evidence_objects": len(evidence_objects),
        "total_governed_source_records": len(source_catalog),
        "normalized_orphan_evidence_objects": normalized_orphans,
        "source_kind_counts": dict(sorted(source_kind_counts.items())),
        "confidence_counts": dict(sorted(confidence_counts.items())),
        "triage_flag_counts": dict(sorted(triage_counts.items())),
    }

    return {
        "version": "1.0",
        "purpose": (
            "Machine-readable claim/evidence coverage projection across accepted v0.1 embedded "
            "sources and v0.2 normalized Evidence Contributions. Metrics are audit signals, not truth scores."
        ),
        "summary": summary,
        "claims": sorted(claim_rows, key=lambda row: row["claim_ref"]),
        "sources": sorted(source_catalog.values(), key=lambda row: row["evidence_id"]),
        "errors": sorted(errors),
    }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate ND Oracle Evidence coverage registry.")
    parser.add_argument("--as-of", help="Use YYYY-MM-DD instead of today's date.")
    parser.add_argument("--output", type=Path, help="Write JSON registry to this path.")
    parser.add_argument("--summary", action="store_true", help="Print only the summary JSON.")
    parser.add_argument("--fail-gaps", action="store_true", help="Exit non-zero when coverage errors exist.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    as_of = date.fromisoformat(args.as_of) if args.as_of else date.today()
    registry = build_registry(ROOT, as_of=as_of)
    payload = registry["summary"] if args.summary else registry
    text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")
    if args.fail_gaps and registry["errors"]:
        for error in registry["errors"]:
            print(f"EVIDENCE COVERAGE ERROR: {error}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
