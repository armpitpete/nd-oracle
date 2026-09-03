#!/usr/bin/env python3
"""Audit review freshness for every governed Evidence source record."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "contracts" / "evidence-layer-v1.json"


@dataclass(frozen=True)
class EvidenceSourceFreshnessRecord:
    evidence_id: str
    evidence_model: str
    source_kind: str
    path: Path
    last_reviewed: date | None
    age_days: int | None
    max_age_days: int

    @property
    def overdue(self) -> bool:
        return self.last_reviewed is None or self.age_days is None or self.age_days > self.max_age_days


def _policy(root: Path) -> dict[str, int]:
    path = root / "contracts" / "evidence-layer-v1.json"
    raw = json.loads(path.read_text(encoding="utf-8"))["freshness"]["source_kind_max_age_days"]
    return {str(key): int(value) for key, value in raw.items()}


def _review_date(obj: dict) -> date | None:
    raw = obj.get("provenance", {}).get("last_reviewed")
    try:
        return date.fromisoformat(raw) if raw else None
    except (TypeError, ValueError):
        return None


def audit_evidence_source_freshness(root: Path = ROOT, *, as_of: date | None = None) -> list[EvidenceSourceFreshnessRecord]:
    if as_of is None:
        as_of = date.today()
    policy = _policy(root)
    records: list[EvidenceSourceFreshnessRecord] = []
    for path in sorted((root / "objects").glob("*/*.json")):
        obj = json.loads(path.read_text(encoding="utf-8"))
        reviewed = _review_date(obj)
        age = (as_of - reviewed).days if reviewed is not None else None
        if obj.get("type") == "concept" and obj.get("schema_version") == "0.1":
            for source in obj.get("sources", []):
                kind = str(source.get("kind", "other"))
                if kind not in policy:
                    raise ValueError(f"Unknown Evidence source_kind for freshness policy: {kind}")
                records.append(EvidenceSourceFreshnessRecord(
                    evidence_id=f"legacy:{obj['id']}:{source.get('id')}",
                    evidence_model="legacy_v0.1_embedded",
                    source_kind=kind,
                    path=path,
                    last_reviewed=reviewed,
                    age_days=age,
                    max_age_days=policy[kind],
                ))
        elif obj.get("type") == "evidence" and obj.get("schema_version") == "0.2":
            kind = str(obj.get("source_kind", "other"))
            if kind not in policy:
                raise ValueError(f"Unknown Evidence source_kind for freshness policy: {kind}")
            records.append(EvidenceSourceFreshnessRecord(
                evidence_id=str(obj.get("id", path.stem)),
                evidence_model="normalized_v0.2",
                source_kind=kind,
                path=path,
                last_reviewed=reviewed,
                age_days=age,
                max_age_days=policy[kind],
            ))
    return sorted(records, key=lambda record: record.evidence_id)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Audit all governed Evidence source review dates.")
    parser.add_argument("--as-of", help="Override today's date with YYYY-MM-DD.")
    parser.add_argument("--fail-overdue", action="store_true")
    args = parser.parse_args(argv)
    as_of = date.fromisoformat(args.as_of) if args.as_of else date.today()
    records = audit_evidence_source_freshness(ROOT, as_of=as_of)
    overdue = [record for record in records if record.overdue]
    for record in overdue:
        reviewed = record.last_reviewed.isoformat() if record.last_reviewed else "MISSING/INVALID"
        age = str(record.age_days) if record.age_days is not None else "unknown"
        print(
            f"OVERDUE EVIDENCE SOURCE {record.evidence_id}: model={record.evidence_model}; "
            f"source_kind={record.source_kind}; last_reviewed={reviewed}; age_days={age}; "
            f"limit={record.max_age_days}; path={record.path.relative_to(ROOT)}"
        )
    print(f"Evidence source freshness audit: {len(records)} governed source records checked; {len(overdue)} overdue as of {as_of.isoformat()}.")
    return 1 if args.fail_overdue and overdue else 0


if __name__ == "__main__":
    raise SystemExit(main())
