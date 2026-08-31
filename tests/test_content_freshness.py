from __future__ import annotations

import json
import tempfile
import unittest
from datetime import date
from pathlib import Path

from scripts import check_content_freshness


class ContentFreshnessTests(unittest.TestCase):
    def test_current_governed_corpus_is_fresh_at_candidate_date(self) -> None:
        records = check_content_freshness.audit_freshness(
            check_content_freshness.ROOT,
            as_of=date(2026, 8, 29),
        )
        self.assertGreaterEqual(len(records), 100)
        self.assertEqual([], [record for record in records if record.overdue])
        self.assertIn("evidence", {record.object_type for record in records})

    def test_resource_becomes_overdue_after_180_days(self) -> None:
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            directory = root / "objects" / "resources"
            directory.mkdir(parents=True)
            (directory / "example.json").write_text(
                json.dumps({"id": "example", "type": "resource", "provenance": {"last_reviewed": "2026-01-01"}}),
                encoding="utf-8",
            )
            records = check_content_freshness.audit_freshness(root, as_of=date(2026, 8, 28))
            self.assertEqual(1, len(records))
            self.assertTrue(records[0].overdue)
            self.assertEqual(180, records[0].max_age_days)

    def test_missing_review_date_is_overdue(self) -> None:
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            directory = root / "objects" / "questions"
            directory.mkdir(parents=True)
            (directory / "example.json").write_text(
                json.dumps({"id": "example", "type": "question", "provenance": {"last_reviewed": None}}),
                encoding="utf-8",
            )
            records = check_content_freshness.audit_freshness(root, as_of=date(2026, 8, 28))
            self.assertTrue(records[0].overdue)


if __name__ == "__main__":
    unittest.main()
