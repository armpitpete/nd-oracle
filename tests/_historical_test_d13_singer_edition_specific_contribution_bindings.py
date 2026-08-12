from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.validate_migration import git_blob_sha

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "objects" / "concepts" / "neurodiversity.json"
DECISIONS = ROOT / "migration-candidates" / "autism-neurodiversity" / "owner-decisions.json"
RESEARCH = ROOT / "migration-candidates" / "autism-neurodiversity" / "singer-edition-enrichment-research.json"
EDITIONS = ROOT / "migration-candidates" / "autism-neurodiversity" / "singer-edition-candidates.json"
PAIR = ROOT / "migration-candidates" / "autism-neurodiversity" / "structural-candidate.json"
D13_ID = "d13-singer-edition-specific-contribution-bindings"
D13_BASE = "84087c7a86f0efda4db6fc1f0ff29c468dab82e8"
SOURCE_BLOB = "5a38bc4250079412dd3f4da1d598dfcab984ca66"
KINDLE_ID = "neurodiversity-source-singer-2016-kindle"
PRINT_ID = "neurodiversity-source-singer-2017-revised-print"
CLAIM_1 = "neurodiversity#neurodiversity-claim-1"
CLAIM_2 = "neurodiversity#neurodiversity-claim-2"


class D13SingerEditionSpecificContributionBindingsTests(unittest.TestCase):
    def load(self, path: Path) -> dict:
        return json.loads(path.read_text(encoding="utf-8"))

    def decision(self) -> dict:
        decisions = self.load(DECISIONS)["decisions"]
        return next(item for item in decisions if item["id"] == D13_ID)

    def test_d13_records_exact_three_accepted_bindings_and_one_pending(self) -> None:
        decision = self.decision()
        self.assertEqual("accepted", decision["status"])
        self.assertEqual(D13_BASE, decision["accepted_against_main"])
        self.assertEqual(
            "nd-singer-edition-specific-contribution-bindings",
            decision["supersedes_research_decision_candidate"]["id"],
        )
        accepted = {
            (item["evidence_id"], item["claim_ref"], item["role"])
            for item in decision["accepted_bindings"]
        }
        self.assertEqual(
            {
                (KINDLE_ID, CLAIM_1, "compatible"),
                (PRINT_ID, CLAIM_1, "compatible"),
                (PRINT_ID, CLAIM_2, "compatible"),
            },
            accepted,
        )
        pending = decision["pending_binding"]
        self.assertEqual(KINDLE_ID, pending["evidence_id"])
        self.assertEqual(CLAIM_2, pending["claim_ref"])
        self.assertEqual("compatible", pending["role"])
        self.assertEqual("pending_stronger_direct_text_evidence", pending["status"])
        self.assertFalse(decision["automatic_claim_support_copying"])
        self.assertTrue(decision["preserve_authoritative_v01_source_unchanged"])
        self.assertFalse(decision["authoritative_evidence_contribution_creation_authorised"])
        self.assertFalse(decision["authoritative_v01_mutation_authorised"])
        self.assertFalse(decision["authoritative_v02_replacement_authorised"])

    def test_candidate_state_preserves_d13_bindings_after_later_decisions(self) -> None:
        record = self.load(EDITIONS)
        self.assertFalse(record["authoritative"])
        self.assertIn(D13_ID, record["accepted_enrichment_decision_refs"])
        candidates = {item["id"]: item for item in record["candidates"]}
        kindle = candidates[KINDLE_ID]
        printed = candidates[PRINT_ID]

        kindle_accepted = {
            (item["claim_ref"], item["role"], item["decision_ref"])
            for item in kindle["accepted_contribution_bindings"]
        }
        self.assertIn((CLAIM_1, "compatible", D13_ID), kindle_accepted)
        self.assertNotIn((CLAIM_2, "compatible", D13_ID), kindle_accepted)

        printed_accepted = {
            (item["claim_ref"], item["role"], item["decision_ref"])
            for item in printed["accepted_contribution_bindings"]
        }
        self.assertEqual(
            {
                (CLAIM_1, "compatible", D13_ID),
                (CLAIM_2, "compatible", D13_ID),
            },
            printed_accepted,
        )
        self.assertEqual([], printed["pending_contribution_bindings"])
        self.assertNotIn("contributions", kindle)
        self.assertNotIn("contributions", printed)
        self.assertFalse(record["boundaries"]["claim_support_copying_authorised"])

    def test_historical_research_snapshot_remains_unrewritten(self) -> None:
        research = self.load(RESEARCH)
        decision_candidates = {item["id"]: item for item in research["next_decision_candidates"]}
        self.assertEqual(
            "owner_decision_required",
            decision_candidates["nd-singer-edition-specific-contribution-bindings"]["status"],
        )
        kindle = research["edition_assessments"][KINDLE_ID]["contribution_bindings"]
        printed = research["edition_assessments"][PRINT_ID]["contribution_bindings"]
        self.assertEqual("owner_review_candidate", kindle["neurodiversity-claim-1"]["status"])
        self.assertEqual(
            "owner_review_candidate_with_direct_text_preferred",
            kindle["neurodiversity-claim-2"]["status"],
        )
        self.assertEqual("owner_review_candidate", printed["neurodiversity-claim-1"]["status"])
        self.assertEqual("owner_review_candidate", printed["neurodiversity-claim-2"]["status"])

    def test_pair_preserves_d13_and_other_blockers_after_later_decisions(self) -> None:
        pair = self.load(PAIR)
        self.assertIn(D13_ID, pair["accepted_owner_decisions"])
        self.assertTrue(pair["authorisations"]["neurodiversity_singer_selected_contribution_bindings_accepted"])
        self.assertFalse(pair["authorisations"]["neurodiversity_singer_auto_duplicate_claim_support"])
        blockers = {item["id"]: item for item in pair["blockers"]}
        evidence = blockers["neurodiversity-evidence-enrichment"]
        self.assertIn("D13 accepts three edition-specific compatible bindings", evidence["detail"])
        self.assertIn("2016", evidence["detail"])
        self.assertIn("paired-structural-relation-confidence", blockers)
        self.assertIn("autism-uncertainty-shape", blockers)
        self.assertIn("neurodiversity-uncertainty-shape", blockers)
        self.assertIn("neurodiversity-adhd-structural-edge", blockers)
        self.assertFalse(pair["authorisations"]["authoritative_neurodiversity_v01_mutation"])
        self.assertFalse(pair["authorisations"]["authoritative_v02_replacement"])

    def test_authoritative_v01_is_byte_identical(self) -> None:
        self.assertEqual(SOURCE_BLOB, git_blob_sha(SOURCE))


if __name__ == "__main__":
    unittest.main()
