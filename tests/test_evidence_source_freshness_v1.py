from __future__ import annotations

import json
import tempfile
import unittest
from datetime import date
from pathlib import Path

from scripts import evidence_source_freshness


class EvidenceSourceFreshnessV1Tests(unittest.TestCase):
    def write_json(self, root: Path, relative: str, obj: dict) -> None:
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(obj), encoding="utf-8")

    def write_policy(self, root: Path) -> None:
        path = root / "contracts" / "evidence-layer-v1.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps({"freshness": {"source_kind_max_age_days": {"peer_reviewed": 730, "authoritative_guidance": 180, "community": 180, "other": 365}}}), encoding="utf-8")

    def test_mutable_guidance_and_stable_research_have_different_review_cadence(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); self.write_policy(root)
            self.write_json(root, "objects/evidence/guidance.json", {"id":"guidance","type":"evidence","schema_version":"0.2","source_kind":"authoritative_guidance","provenance":{"last_reviewed":"2026-02-01"}})
            self.write_json(root, "objects/evidence/paper.json", {"id":"paper","type":"evidence","schema_version":"0.2","source_kind":"peer_reviewed","provenance":{"last_reviewed":"2025-01-01"}})
            records = {record.evidence_id: record for record in evidence_source_freshness.audit_evidence_source_freshness(root, as_of=date(2026,9,3))}
            self.assertTrue(records["guidance"].overdue)
            self.assertFalse(records["paper"].overdue)
            self.assertEqual(180, records["guidance"].max_age_days)
            self.assertEqual(730, records["paper"].max_age_days)

    def test_legacy_source_inherits_parent_concept_review_date(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); self.write_policy(root)
            self.write_json(root, "objects/concepts/example.json", {"id":"example","type":"concept","schema_version":"0.1","provenance":{"last_reviewed":"2026-08-01"},"sources":[{"id":"community-source","kind":"community"}]})
            record = evidence_source_freshness.audit_evidence_source_freshness(root, as_of=date(2026,9,3))[0]
            self.assertEqual("legacy:example:community-source", record.evidence_id)
            self.assertEqual("legacy_v0.1_embedded", record.evidence_model)
            self.assertFalse(record.overdue)

    def test_unknown_source_kind_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); self.write_policy(root)
            self.write_json(root, "objects/evidence/example.json", {"id":"example","type":"evidence","schema_version":"0.2","source_kind":"mystery","provenance":{"last_reviewed":"2026-09-01"}})
            with self.assertRaisesRegex(ValueError, "Unknown Evidence source_kind"):
                evidence_source_freshness.audit_evidence_source_freshness(root, as_of=date(2026,9,3))

    def test_retrospective_as_of_date_does_not_redefine_later_review_as_overdue(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); self.write_policy(root)
            self.write_json(root, "objects/evidence/example.json", {"id":"example","type":"evidence","schema_version":"0.2","source_kind":"peer_reviewed","provenance":{"last_reviewed":"2026-09-02"}})
            record = evidence_source_freshness.audit_evidence_source_freshness(root, as_of=date(2026,8,29))[0]
            self.assertLess(record.age_days, 0)
            self.assertFalse(record.overdue)


if __name__ == "__main__":
    unittest.main()
