#!/usr/bin/env python3
"""Surface ND Oracle content that is due for re-review.

This check is deliberately metadata-based and network-independent. `provenance.last_reviewed`
is the governed record of when the object and its access/source route were last checked.
A separate review may use the web, but CI must not make publication depend on transient network
availability.

Evidence uses source-kind-specific review intervals. These intervals govern review of the Oracle's
interpretation and source route; they do not imply that an older paper/book has become invalid.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OBJECTS_DIR = ROOT / "objects"
MAX_AGE_DAYS = {
    "resource": 180,
    "question": 365,
    "concept": 365,
    "evidence": 365,
    "perspective": 365,
    "experience": 365,
}
EVIDENCE_SOURCE_KIND_MAX_AGE_DAYS = {
    "authoritative_guidance": 180,
    "commercial": 180,
    "community": 180,
    "practical": 180,
    "dataset": 365,
    "other": 365,
    "peer_reviewed": 730,
    "lived_experience": 730,
    "book": 1095,
    "historical": 1095,
}


@dataclass(frozen=True)
class FreshnessRecord:
    object_id: str
    object_type: str
    path: Path
    last_reviewed: date | None
    age_days: int | None
    max_age_days: int

    @property
    def overdue(self) -> bool:
        return self.last_reviewed is None or self.age_days is None or self.age_days > self.max_age_days


def _load_objects(root: Path = ROOT) -> list[tuple[Path, dict]]:
    records: list[tuple[Path, dict]] = []
    objects_dir = root / "objects"
    if not objects_dir.is_dir():
        return records
    for path in sorted(objects_dir.glob("*/*.json")):
        with path.open("r", encoding="utf-8") as handle:
            records.append((path, json.load(handle)))
    return records


def _max_age_for_object(obj: dict) -> int:
    object_type = str(obj.get("type", "unknown"))
    if object_type == "evidence":
        source_kind = str(obj.get("source_kind", "other"))
        return EVIDENCE_SOURCE_KIND_MAX_AGE_DAYS.get(source_kind, EVIDENCE_SOURCE_KIND_MAX_AGE_DAYS["other"])
    return MAX_AGE_DAYS.get(object_type, 365)


def audit_freshness(root: Path = ROOT, *, as_of: date | None = None) -> list[FreshnessRecord]:
    if as_of is None:
        as_of = date.today()
    output: list[FreshnessRecord] = []
    for path, obj in _load_objects(root):
        object_type = str(obj.get("type", "unknown"))
        max_age = _max_age_for_object(obj)
        raw = obj.get("provenance", {}).get("last_reviewed")
        reviewed: date | None
        try:
            reviewed = date.fromisoformat(raw) if raw else None
        except (TypeError, ValueError):
            reviewed = None
        age = (as_of - reviewed).days if reviewed is not None else None
        output.append(
            FreshnessRecord(
                object_id=str(obj.get("id", path.stem)),
                object_type=object_type,
                path=path,
                last_reviewed=reviewed,
                age_days=age,
                max_age_days=max_age,
            )
        )
    return output


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="List governed ND Oracle content due for re-review.")
    parser.add_argument("--as-of", help="Override today's date with YYYY-MM-DD for deterministic review/audit runs.")
    parser.add_argument(
        "--fail-overdue",
        action="store_true",
        help="Exit non-zero when any object is overdue or lacks a valid last_reviewed date.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    as_of = date.fromisoformat(args.as_of) if args.as_of else date.today()
    records = audit_freshness(ROOT, as_of=as_of)
    overdue = [record for record in records if record.overdue]
    for record in records:
        if record.overdue:
            reviewed = record.last_reviewed.isoformat() if record.last_reviewed else "MISSING/INVALID"
            age = str(record.age_days) if record.age_days is not None else "unknown"
            print(
                f"OVERDUE {record.object_type} {record.object_id}: last_reviewed={reviewed}; "
                f"age_days={age}; limit={record.max_age_days}; path={record.path.relative_to(ROOT)}"
            )
    evidence_limits = ", ".join(
        f"{kind}={days}d" for kind, days in sorted(EVIDENCE_SOURCE_KIND_MAX_AGE_DAYS.items())
    )
    print(
        f"Freshness audit: {len(records)} governed objects checked; {len(overdue)} overdue "
        f"as of {as_of.isoformat()}. Resource limit={MAX_AGE_DAYS['resource']} days; "
        f"Evidence source-kind limits: {evidence_limits}; other current content=365 days."
    )
    if args.fail_overdue and overdue:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
