from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.validate_migration import git_blob_sha

ROOT = Path(__file__).resolve().parents[1]
DECISIONS = ROOT / "tests" / "fixtures" / "migration" / "autism" / "owner-decisions.json"
CANDIDATE = ROOT / "migration-candidates" / "autism-neurodiversity" / "structural-candidate.json"
AUTISM = ROOT / "objects" / "concepts" / "autism.json"
AUTISM_BLOB = "b2d3809ecfcdb1d81c793a2401f0533a4b17ea98"

HELD_BY_SCOPE = "WHO institutional global public-health guidance on autism; not a statement representing all clinicians, autistic people, families, researchers or WHO Member States individually."
REASONING = "WHO frames autism as diverse, with variable and evolving abilities and needs, and links health and quality of life to accessible, inclusive, person-responsive services plus community and societal support."
SCOPE = "Global public-health description of autism, health and care needs, inclusion and support across the life course; excludes individual diagnosis and does not purport to capture the full range of autistic lived experience or community perspectives."


class D7AutismWhoPerspectiveFramingTests(unittest.TestCase):
    def test_d7_accepts_exact_three_fields_only_for_future_non_authoritative_candidate(self) -> None:
        decisions = json.loads(DECISIONS.read_text(encoding="utf-8"))["decisions"]
        d7 = {item["id"]: item for item in decisions}["d7-autism-who-perspective-framing"]
        self.assertEqual("accepted", d7["status"])
        self.assertEqual("cae42eaf485f91f2920dcc1a15176bc335286719", d7["accepted_against_main"])
        self.assertEqual("autism-perspective-clinical", d7["perspective_id"])
        self.assertEqual(
            {"held_by.scope": HELD_BY_SCOPE, "reasoning": REASONING, "scope": SCOPE},
            d7["accepted_fields"],
        )
        self.assertFalse(d7["authoritative_perspective_authorised"])
        self.assertFalse(d7["authoritative_v01_mutation_authorised"])
        self.assertFalse(d7["authoritative_v02_replacement_authorised"])
        self.assertFalse(d7["publication_or_deployment_authorised"])
        self.assertEqual(AUTISM_BLOB, git_blob_sha(AUTISM))

    def test_paired_candidate_no_longer_lists_autism_perspective_as_blocker(self) -> None:
        candidate = json.loads(CANDIDATE.read_text(encoding="utf-8"))
        self.assertIn("d7-autism-who-perspective-framing", candidate["accepted_owner_decisions"])
        blocker_ids = {item["id"] for item in candidate["blockers"]}
        self.assertNotIn("autism-perspective-framing", blocker_ids)
        self.assertTrue(candidate["authorisations"]["autism_who_perspective_framing_accepted"])
        self.assertFalse(candidate["authoritative"])
        self.assertFalse(candidate["authorisations"]["authoritative_v02_replacement"])


if __name__ == "__main__":
    unittest.main()
