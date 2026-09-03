from __future__ import annotations

import unittest
from datetime import date

from scripts import check_content_freshness


class EvidenceFreshnessCompatibilityV1Tests(unittest.TestCase):
    def test_existing_object_freshness_audit_retains_retrospective_semantics(self) -> None:
        records = check_content_freshness.audit_freshness(check_content_freshness.ROOT, as_of=date(2026, 8, 29))
        self.assertEqual([], [record for record in records if record.overdue])

    def test_normalized_evidence_source_kind_policy_is_present(self) -> None:
        self.assertEqual(180, check_content_freshness.EVIDENCE_SOURCE_KIND_MAX_AGE_DAYS["authoritative_guidance"])
        self.assertEqual(730, check_content_freshness.EVIDENCE_SOURCE_KIND_MAX_AGE_DAYS["peer_reviewed"])
        self.assertEqual(1095, check_content_freshness.EVIDENCE_SOURCE_KIND_MAX_AGE_DAYS["historical"])


if __name__ == "__main__":
    unittest.main()
