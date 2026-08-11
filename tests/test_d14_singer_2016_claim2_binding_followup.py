from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.validate_migration import git_blob_sha

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "objects" / "concepts" / "neurodiversity.json"
DECISIONS = ROOT / "migration-candidates" / "autism-neurodiversity" / "owner-decisions.json"
RESEARCH = ROOT / "migration-candidates" / "autism-neurodiversity" / "singer-2016-followup-research.json"
EDITIONS = ROOT / "migration-candidates" / "autism-neurodiversity" / "singer-edition-candidates.json"
PAIR = ROOT / "migration-candidates" / "autism-neurodiversity" / "structural-candidate.json"
D13_ID = "d13-singer-edition-specific-contribution-bindings"
D14_ID = "d14-singer-2016-claim2-binding-followup"
D14_BASE = "e916d56ba25ce761afd1a6a587c2f403a9f44b0d"
SOURCE_BLOB = "5a38bc4250079412dd3f4da1d598dfcab984ca66"
KINDLE_ID = "neurodiversity-source-singer-2016-kindle"
CLAIM_1 = "neurodiversity#neurodiversity-claim-1"
CLAIM_2 = "neurodiversity#neurodiversity-claim-2"


class D14Singer2016Claim2BindingFollowupTests(unittest.TestCase):
    def load(self, path: Path) -> dict:
        return json.loads(path.read_text(encoding="utf-8"))

    def decision(self) -> dict:
        decisions = self.load(DECISIONS)["decisions"]
        return next(item for item in decisions if item["id"] == D14_ID)

    def test_d14_records_exact_owner_accepted_binding_and_boundaries(self) -> None:
        decision = self.decision()
        self.assertEqual("accepted", decision["status"])
        self.assertEqual(D14_BASE, decision["accepted_against_main"])
        self.assertEqual(
            "nd-singer-2016-claim2-binding-followup",
            decision["supersedes_research_decision_candidate"]["id"],
        )
        binding = decision["accepted_binding"]
        self.assertEqual(KINDLE_ID, binding["evidence_id"])
        self.assertEqual(CLAIM_2, binding["claim_ref"])
        self.assertEqual("compatible", binding["role"])
        self.assertTrue(binding["followup_research_ref"])
        self.assertTrue(decision["preserve_2016_full_publication_date_unresolved"])
        self.assertFalse(decision["accept_2016_full_date"])
        self.assertFalse(decision["automatic_claim_support_copying"])
        self.assertTrue(decision["preserve_authoritative_v01_source_unchanged"])
        self.assertFalse(decision["authoritative_evidence_contribution_creation_authorised"])
        self.assertFalse(decision["authoritative_v01_mutation_authorised"])
        self.assertFalse(decision["authoritative_v02_replacement_authorised"])
        self.assertFalse(decision["schema_change_authorised"])
        self.assertFalse(decision["publication_or_deployment_authorised"])

    def test_candidate_moves_only_2016_claim2_from_pending_to_accepted(self) -> None:
        record = self.load(EDITIONS)
        self.assertFalse(record["authoritative"])
        self.assertIn(D14_ID, record["accepted_enrichment_decision_refs"])
        kindle = next(item for item in record["candidates"] if item["id"] == KINDLE_ID)
        accepted = {
            (item["claim_ref"], item["role"], item["decision_ref"])
            for item in kindle["accepted_contribution_bindings"]
        }
        self.assertEqual(
            {
                (CLAIM_1, "compatible", D13_ID),
                (CLAIM_2, "compatible", D14_ID),
            },
            accepted,
        )
        claim2 = next(item for item in kindle["accepted_contribution_bindings"] if item["claim_ref"] == CLAIM_2)
        self.assertTrue(claim2["followup_research_ref"])
        self.assertEqual([], kindle["pending_contribution_bindings"])
        self.assertNotIn("publication_date", kindle)
        self.assertEqual(
            "secondary_catalogue_candidate_still_not_ready_for_verified_enrichment",
            kindle["date_research_status"],
        )
        self.assertNotIn("contributions", kindle)
        self.assertFalse(record["boundaries"]["claim_support_copying_authorised"])
        self.assertFalse(record["boundaries"]["authoritative_evidence_creation_authorised"])

    def test_pair_records_d14_without_closing_unrelated_blockers(self) -> None:
        pair = self.load(PAIR)
        self.assertIn(D14_ID, pair["accepted_owner_decisions"])
        auth = pair["authorisations"]
        self.assertTrue(auth["neurodiversity_singer_contribution_bindings_accepted"])
        self.assertTrue(auth["neurodiversity_singer_selected_contribution_bindings_accepted"])
        self.assertTrue(auth["neurodiversity_singer_2016_claim_2_contribution_binding_accepted"])
        self.assertFalse(auth["neurodiversity_singer_2016_full_date_accepted"])
        self.assertFalse(auth["neurodiversity_singer_auto_duplicate_claim_support"])
        self.assertFalse(auth["authoritative_neurodiversity_v01_mutation"])
        self.assertFalse(auth["authoritative_v02_replacement"])

        blockers = {item["id"]: item for item in pair["blockers"]}
        evidence = blockers["neurodiversity-evidence-enrichment"]
        self.assertEqual("four_singer_bindings_accepted_2016_date_pending", evidence["kind"])
        self.assertIn("D14 accepts the remaining 2016 Kindle -> Claim 2 compatible binding", evidence["detail"])
        self.assertIn("2016 day-level publication date remains deliberately unaccepted", evidence["detail"])
        self.assertIn("paired-structural-relation-confidence", blockers)
        self.assertIn("autism-uncertainty-shape", blockers)
        self.assertIn("neurodiversity-uncertainty-shape", blockers)
        self.assertIn("neurodiversity-adhd-structural-edge", blockers)

    def test_followup_research_remains_historical_pre_d14_snapshot(self) -> None:
        research = self.load(RESEARCH)
        assessment = research["claim_2_binding_assessment"]
        self.assertEqual("owner_review_candidate_after_stronger_edition_specific_evidence", assessment["status"])
        self.assertEqual("owner_review_ready", assessment["decision_readiness"])
        candidates = {item["id"]: item for item in research["next_decision_candidates"]}
        self.assertEqual(
            "owner_decision_required",
            candidates["nd-singer-2016-claim2-binding-followup"]["status"],
        )
        self.assertFalse(research["boundaries"]["owner_decision_made"])
        self.assertFalse(research["boundaries"]["2016_claim_2_binding_accepted"])
        self.assertFalse(research["boundaries"]["2016_full_date_accepted"])

    def test_authoritative_v01_is_byte_identical(self) -> None:
        self.assertEqual(SOURCE_BLOB, git_blob_sha(SOURCE))


if __name__ == "__main__":
    unittest.main()
