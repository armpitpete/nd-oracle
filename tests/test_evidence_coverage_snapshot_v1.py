from __future__ import annotations
import json
import unittest
from datetime import date
from pathlib import Path
from scripts import evidence_coverage
ROOT = Path(__file__).resolve().parents[1]
class EvidenceCoverageSnapshotV1Tests(unittest.TestCase):
    def test_snapshot_is_exact_reproducible_projection(self) -> None:
        snapshot = json.loads((ROOT / "reports" / "EVIDENCE_COVERAGE_v1.json").read_text(encoding="utf-8"))
        as_of = date.fromisoformat(snapshot["summary"]["as_of"])
        self.assertEqual(snapshot, evidence_coverage.build_registry(ROOT, as_of=as_of))
if __name__ == "__main__":
    unittest.main()
