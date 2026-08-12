from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.validate_migration import git_blob_sha

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "objects" / "concepts" / "neurodiversity.json"
RESEARCH = ROOT / "migration-candidates" / "autism-neurodiversity" / "singer-2016-followup-research.json"
EDITIONS = ROOT / "migration-candidates" / "autism-neurodiversity" / "singer-edition-candidates.json"
PAIR = ROOT / "migration-candidates" / "autism-neurodiversity" / "structural-candidate.json"
BASE = "75b2aab6d6aa2646e18b4780ea0fb0380a42d009"
SOURCE_BLOB = "5a38bc4250079412dd3f4da1d598dfcab984ca66"
KINDLE_ID = "neurodiversity-source-singer-2016-kindle"
CLAIM_2 = "neurodiversity#neurodiversity-claim-2"


class Singer2016FollowupResearchTests(unittest.TestCase):
    def load(self, path: Path) -> dict:
        return json.loads(path.read_text(encoding="utf-8"))

    def test_research_is_bounded_non_authoritative_and_source_anchored(self) -> None:
        research = self.load(RESEARCH)
        self.assertEqual("1.0", research["research_version"])
        self.assertEqual(BASE, research["prepared_against_main"])
        self.assertFalse(research["authoritative"])
        self.assertFalse(research["authoritative_replacement"])
        self.assertEqual(SOURCE_BLOB, research["legacy_source_anchor"]["blob_sha"])
        self.assertEqual(SOURCE_BLOB, git_blob_sha(SOURCE))
        self.assertTrue(all(value is False for value in research["boundaries"].values()))

    def test_2016_day_level_date_is_not_promoted(self) -> None:
        date = self.load(RESEARCH)["publication_date_assessment"]
        self.assertEqual("2016-07-03", date["candidate_value"])
        self.assertEqual(
            "secondary_catalogue_candidate_still_not_ready_for_verified_enrichment",
            date["status"],
        )
        self.assertEqual("not_ready", date["decision_readiness"])
        self.assertEqual("secondary_catalogue_only", date["evidence_strength"]["exact_2016_07_03_day"])

        editions = self.load(EDITIONS)
        kindle = next(item for item in editions["candidates"] if item["id"] == KINDLE_ID)
        self.assertNotIn("publication_date", kindle)
        self.assertFalse(self.load(PAIR)["authorisations"]["neurodiversity_singer_2016_full_date_accepted"])

    def test_claim_2_research_snapshot_remains_owner_review_ready(self) -> None:
        research = self.load(RESEARCH)
        assessment = research["claim_2_binding_assessment"]
        self.assertEqual(KINDLE_ID, assessment["evidence_id"])
        self.assertEqual(CLAIM_2, assessment["claim_ref"])
        self.assertEqual("compatible", assessment["proposed_role"])
        self.assertEqual(
            "owner_review_candidate_after_stronger_edition_specific_evidence",
            assessment["status"],
        )
        self.assertEqual("owner_review_ready", assessment["decision_readiness"])
        self.assertFalse(research["boundaries"]["owner_decision_made"])
        self.assertFalse(research["boundaries"]["2016_claim_2_binding_accepted"])

    def test_followup_snapshot_and_other_blockers_remain_preserved(self) -> None:
        pair = self.load(PAIR)
        self.assertTrue(pair["authorisations"]["neurodiversity_singer_2016_followup_research_prepared"])
        blockers = {item["id"]: item for item in pair["blockers"]}
        evidence = blockers["neurodiversity-evidence-enrichment"]
        self.assertIn("2016", evidence["kind"])
        self.assertIn("2016 day-level publication date remains deliberately unaccepted", evidence["detail"])
        self.assertIn("paired-structural-relation-confidence", blockers)
        self.assertIn("autism-uncertainty-shape", blockers)
        self.assertIn("neurodiversity-uncertainty-shape", blockers)
        self.assertIn("neurodiversity-adhd-structural-edge", blockers)
        self.assertFalse(pair["authorisations"]["authoritative_v02_replacement"])

    def test_research_next_gate_remains_historical_owner_decision_candidate(self) -> None:
        research = self.load(RESEARCH)
        candidates = {item["id"]: item for item in research["next_decision_candidates"]}
        self.assertEqual(
            "owner_decision_required",
            candidates["nd-singer-2016-claim2-binding-followup"]["status"],
        )
        self.assertFalse(research["boundaries"]["owner_decision_made"])
        self.assertFalse(research["boundaries"]["2016_claim_2_binding_accepted"])


if __name__ == "__main__":
    unittest.main()
