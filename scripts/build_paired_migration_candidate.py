#!/usr/bin/env python3
"""Build the non-authoritative Autism + Neurodiversity paired migration candidate.

The builder is deliberately conservative. It preserves all v0.1 inventory units,
reuses accepted Autism migration decisions, records Neurodiversity gaps without
inventing semantics, and emits only a partial structural-pair candidate rather
than pretending that the current blockers form valid authoritative v0.2 objects.
"""

from __future__ import annotations

import argparse
import copy
import json
import shutil
from pathlib import Path
from typing import Any

try:
    from scripts.validate import v01_preservation_inventory
    from scripts.validate_migration import git_blob_sha
except ModuleNotFoundError:  # direct execution from scripts/
    from validate import v01_preservation_inventory
    from validate_migration import git_blob_sha

ROOT = Path(__file__).resolve().parents[1]
BASE_COMMIT = "1b7e4261c70bd6a86346d34a1f08abf90c3deece"
AUTISM_SOURCE = ROOT / "objects" / "concepts" / "autism.json"
NEURODIVERSITY_SOURCE = ROOT / "objects" / "concepts" / "neurodiversity.json"
AUTISM_FIXTURE = ROOT / "tests" / "fixtures" / "migration" / "autism"
PAIR_SPEC = ROOT / "migration-candidates" / "autism-neurodiversity" / "structural-candidate.json"


def _load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _legacy_payload(unit: str) -> Any:
    prefix, sep, payload = unit.partition(":")
    if not sep or prefix == "object-id":
        raise ValueError(f"unit has no JSON legacy payload: {unit}")
    return json.loads(payload)


def _source_unit(source: dict) -> str:
    return "source:" + json.dumps(source, sort_keys=True, separators=(",", ":"))


def _perspective_unit(perspective: dict) -> str:
    return "perspective:" + json.dumps(perspective, sort_keys=True, separators=(",", ":"))


def _relation_unit(relation: dict) -> str:
    return "relation:" + json.dumps(relation, sort_keys=True, separators=(",", ":"))


def _pending_enrichment(entry_id: str, target_field: str, trigger_unit: str, *, owner_decision: bool = False) -> dict:
    return {
        "id": entry_id,
        "target_field": target_field,
        "trigger_unit": trigger_unit,
        "proposed_value": None,
        "evidence_route": [],
        "value_origin": "owner_decision" if owner_decision else "pending",
        "supplied_by": "Paired candidate preparation; required evidence or owner decision remains outstanding.",
        "review_state": "pending",
        "limitations": [
            "Required v0.2 semantics are absent from the anchored v0.1 source and have not been fabricated for this candidate."
        ],
    }


def _scoped_autism_preservation() -> list[dict]:
    ledger = _load(AUTISM_FIXTURE / "preservation-ledger.json")
    entries: list[dict] = []
    for item in ledger["entries"]:
        scoped = copy.deepcopy(item)
        scoped["source_object_id"] = "autism"
        entries.append(scoped)
    return entries


def _neurodiversity_preservation(source: dict) -> list[dict]:
    entries: list[dict] = []
    exact_prefixes = (
        "object-id:",
        "summary:",
        "alias:",
        "scope-includes:",
        "scope-excludes:",
        "claim:",
        "claim-source-route:",
        "claim-uncertainty-route:",
        "provenance:",
    )
    for unit in sorted(v01_preservation_inventory(source)):
        item: dict[str, Any] = {"source_object_id": "neurodiversity", "unit": unit}
        if unit.startswith(exact_prefixes):
            item.update(
                disposition="represented_exactly",
                candidate_destination=(
                    "paired candidate preservation route; full v0.2 object remains blocked where required semantics are absent"
                ),
            )
        elif unit.startswith("source:"):
            item.update(
                disposition="owner_decision_required",
                unresolved_reason=(
                    "v0.2 Evidence requires verified title/date/authorship and claim-specific Evidence Contribution semantics; "
                    "the legacy source identity remains preserved while enrichment is pending."
                ),
            )
        elif unit.startswith("uncertainty:"):
            item.update(
                disposition="owner_decision_required",
                unresolved_reason=(
                    "Neurodiversity uses list-valued what_would_reduce_it data; no owner decision has authorised a current "
                    "v0.2 single-string representation or a schema-policy extension for this source object."
                ),
                legacy_value=_legacy_payload(unit),
            )
        elif unit.startswith("perspective:"):
            item.update(
                disposition="owner_decision_required",
                unresolved_reason=(
                    "v0.2 Perspective requires holder scope, reasoning and Perspective scope not deterministically present in v0.1."
                ),
            )
        elif unit.startswith("ecosystem-entry:"):
            item.update(
                disposition="legacy_retained_unmapped",
                unresolved_reason=(
                    "The migration compatibility contract provides no accepted v0.2 Concept home for ecosystem_entry_points; "
                    "retain the exact legacy entry and do not auto-promote embedded questions."
                ),
                legacy_value=_legacy_payload(unit),
            )
        elif unit.startswith("relation:"):
            relation = _legacy_payload(unit)
            target = relation.get("target_id")
            if relation.get("type") == "broader_than" and target == "autism":
                item.update(
                    disposition="structural_dependency",
                    dependency_ref="dependency-autism-neurodiversity",
                    unresolved_reason=(
                        "D5 requires the reciprocal Autism/Neurodiversity pair, but the current v0.2 relation confidence is still absent from v0.1."
                    ),
                )
            elif relation.get("type") == "broader_than" and target == "adhd":
                item.update(
                    disposition="structural_dependency",
                    dependency_ref="dependency-neurodiversity-adhd",
                    unresolved_reason=(
                        "Neurodiversity also has a structural edge to ADHD. D5 did not authorise expanding this paired candidate to ADHD."
                    ),
                )
            else:
                item.update(
                    disposition="owner_decision_required",
                    unresolved_reason="No deterministic migration rule has been accepted for this relation.",
                )
        else:
            raise ValueError(f"unclassified Neurodiversity preservation unit: {unit}")
        entries.append(item)
    return entries


def _neurodiversity_enrichment(source: dict) -> list[dict]:
    entries: list[dict] = []
    for evidence in source["sources"]:
        trigger = _source_unit(evidence)
        eid = evidence["id"]
        for field in ("title", "date", "authorship"):
            entries.append(
                _pending_enrichment(
                    f"enrich-{eid}-{field}",
                    f"evidence:{eid}.{field}",
                    trigger,
                )
            )

    sources_by_id = {item["id"]: item for item in source["sources"]}
    for claim in source["claims"]:
        cid = claim["id"]
        for evidence_id in claim["source_ids"]:
            trigger = f"claim-source-route:{cid}->{evidence_id}"
            for field in ("role", "finding", "population-or-context", "methodology"):
                target_field = field.replace("-", "_")
                entries.append(
                    _pending_enrichment(
                        f"enrich-{evidence_id}-{cid}-{field}",
                        f"evidence:{evidence_id}.contributions[{cid}].{target_field}",
                        trigger,
                    )
                )
            if evidence_id not in sources_by_id:
                raise ValueError(f"claim {cid} references missing source {evidence_id}")

    for perspective in source["perspectives"]:
        trigger = _perspective_unit(perspective)
        pid = perspective["id"]
        for field in ("held-by-scope", "reasoning", "scope"):
            target_field = "held_by.scope" if field == "held-by-scope" else field
            entries.append(
                _pending_enrichment(
                    f"enrich-{pid}-{field}",
                    f"perspective:{pid}.{target_field}",
                    trigger,
                    owner_decision=True,
                )
            )

    autism_relation = next(
        item for item in _load(AUTISM_SOURCE)["relations"]
        if item["type"] == "narrower_than" and item["target_id"] == "neurodiversity"
    )
    neuro_relation = next(
        item for item in source["relations"]
        if item["type"] == "broader_than" and item["target_id"] == "autism"
    )
    entries.append(
        _pending_enrichment(
            "decide-autism-neurodiversity-structural-confidence",
            "paired-structural-relation:autism<->neurodiversity.confidence",
            _relation_unit(autism_relation) + " | " + _relation_unit(neuro_relation),
            owner_decision=True,
        )
    )
    return entries


def build_candidate(destination: Path) -> Path:
    destination = Path(destination)
    destination.mkdir(parents=True, exist_ok=True)

    autism = _load(AUTISM_SOURCE)
    neurodiversity = _load(NEURODIVERSITY_SOURCE)
    pair_spec = _load(PAIR_SPEC)

    manifest = {
        "migration_contract_version": "0.2",
        "source_repository_commit": BASE_COMMIT,
        "sources": [
            {
                "path": "objects/concepts/autism.json",
                "blob_sha": git_blob_sha(AUTISM_SOURCE),
                "schema_version": "0.1",
                "object_id": "autism",
            },
            {
                "path": "objects/concepts/neurodiversity.json",
                "blob_sha": git_blob_sha(NEURODIVERSITY_SOURCE),
                "schema_version": "0.1",
                "object_id": "neurodiversity",
            },
        ],
        "candidate_object_ids": ["autism", "neurodiversity"],
        "package_status": "owner_decision_pending",
        "created": "2026-08-11",
        "updated": "2026-08-11",
        "authoritative_replacement": False,
    }
    _write_json(destination / "manifest.json", manifest)

    preservation = {
        "migration_contract_version": "0.2",
        "entries": _scoped_autism_preservation() + _neurodiversity_preservation(neurodiversity),
    }
    _write_json(destination / "preservation-ledger.json", preservation)

    autism_enrichment = _load(AUTISM_FIXTURE / "enrichment-ledger.json")
    enrichment = {
        "migration_contract_version": "0.2",
        "entries": copy.deepcopy(autism_enrichment["entries"]) + _neurodiversity_enrichment(neurodiversity),
    }
    _write_json(destination / "enrichment-ledger.json", enrichment)

    autism_dependencies = _load(AUTISM_FIXTURE / "dependency-ledger.json")
    pair_dependency = copy.deepcopy(autism_dependencies["entries"][0])
    pair_dependency.setdefault("resolution_evidence", []).append(
        "D5 paired structural candidate prepared from exact Autism and Neurodiversity v0.1 blobs; relation confidence remains unresolved, so the dependency is not closed."
    )
    dependencies = {
        "migration_contract_version": "0.2",
        "entries": [
            pair_dependency,
            {
                "id": "dependency-neurodiversity-adhd",
                "source_object": "neurodiversity",
                "relation": "broader_than",
                "dependent_object": "adhd",
                "reason": (
                    "Neurodiversity v0.1 contains broader_than -> adhd. Full structural closure of a future Neurodiversity v0.2 object requires the reciprocal ADHD side, but D5 authorises only the Autism/Neurodiversity pair."
                ),
                "resolution_status": "unresolved",
                "resolution_evidence": [
                    "objects/concepts/neurodiversity.json@blob:5a38bc4250079412dd3f4da1d598dfcab984ca66 contains v0.1 broader_than -> adhd.",
                    "ADHD is intentionally outside this D5 paired candidate and has not been migrated or mutated."
                ],
            },
        ],
    }
    _write_json(destination / "dependency-ledger.json", dependencies)

    candidate_dir = destination / "candidate"
    candidate_dir.mkdir(parents=True, exist_ok=True)
    _write_json(candidate_dir / "structural-pair.json", pair_spec)

    owner_decisions = AUTISM_FIXTURE / "owner-decisions.json"
    if owner_decisions.exists():
        shutil.copyfile(owner_decisions, destination / "owner-decisions.json")

    decision_log = (AUTISM_FIXTURE / "decision-log.md").read_text(encoding="utf-8")
    decision_log += """

## Paired candidate preparation — 2026-08-11

D5 authorises preparation of a non-authoritative Autism + Neurodiversity paired structural candidate only. The exact source anchors are Autism blob `b2d3809ecfcdb1d81c793a2401f0533a4b17ea98` and Neurodiversity blob `5a38bc4250079412dd3f4da1d598dfcab984ca66`, against repository main `1b7e4261c70bd6a86346d34a1f08abf90c3deece`.

The reciprocal legacy relation is preserved in `candidate/structural-pair.json`. No relation confidence is invented: both v0.1 relations lack that v0.2-required field, so structural confidence remains an owner-decision blocker. The D5 Autism/Neurodiversity dependency therefore remains unresolved until an exact paired v0.2 candidate can validate without weakening reciprocity.

Neurodiversity also contains `broader_than -> adhd`. That edge is recorded as a separate structural dependency and is not silently dropped, but ADHD is not added to this candidate because D5 did not authorise expanding the migration unit beyond the accepted pair.

The package also preserves the existing Autism blockers and inventories Neurodiversity-specific Evidence, uncertainty and Perspective gaps without fabricating missing semantics. No authoritative v0.1 object is changed and no authoritative v0.2 replacement is authorised.
"""
    (destination / "decision-log.md").write_text(decision_log, encoding="utf-8")
    return destination


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("destination", type=Path)
    args = parser.parse_args()
    build_candidate(args.destination)
    print(args.destination)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
