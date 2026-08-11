from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.validate_migration import git_blob_sha

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "objects" / "concepts" / "neurodiversity.json"
DECISIONS = ROOT / "migration-candidates" / "autism-neurodiversity" / "owner-decisions.json"
RESEARCH = ROOT / "migration-candidates" / "autism-neurodiversity" / "neurodiversity-enrichment-research.json"
EDITIONS = ROOT / "migration-candidates" / "autism-neurodiversity" / "singer-edition-candidates.json"
PAIR = ROOT / "migration-candidates" / "autism-neurodiversity" / "structural-candidate.json"
SOURCE_BLOB = "5a38bc4250079412dd3f4da1d598dfcab984ca66"
D11_BASE = "ae12681b8fb0d84348bda2347d805d8e44d2165c"
D11_ID = "d11-singer-edition-identity-preservation"
CANDIDATE_IDS = {
    "neurodiversity-source-singer-2016-kindle",
    "neurodiversity-source-singer-2017-revised-print",
}


class D11SingerEditionIdentityPreservationTests(unittest.TestCase):
    def load(self, path: Path) -> dict:
        return json.loads(path.read_text(encoding="utf-8"))

    def d11(self) -> dict:
        decisions = self.load(DECISIONS)["decisions"]
        return next(item for item in decisions if item["id"] == D11_ID)

    def test_d11_records_exact_preservation_rule(self) -> None:
        decision = self.d11()
        self.assertEqual("accepted", decision["status"])
        self.assertEqual(D11_BASE, decision["accepted_against_main"])
        self.assertEqual("neurodiversity-source-singer", decision["legacy_source_id"])
        self.assertEqual(CANDIDATE_IDS, set(decision["candidate_evidence_ids"]))
        self.assertTrue(decision["preserve_separate_evidence_identities"])
        self.assertFalse(decision["select_single_edition"])
        self.assertFalse(decision["combine_editions"])
        self.assertTrue(decision["preserve_authoritative_v01_source_unchanged"])
        self.assertFalse(decision["automatic_claim_support_duplication"])
        self.assertTrue(decision["edition_specific_evidence_required_for_each_contribution"])
        self.assertEqual("nd-singer-edition-reconciliation", decision["supersedes_research_decision_candidate"]["id"])
        self.assertFalse(decision["authoritative_evidence_authorised"])
        self.assertFalse(decision["authoritative_v01_mutation_authorised"])
        self.assertFalse(decision["authoritative_v02_replacement_authorised"])

    def test_two_non_authoritative_identity_candidates_are_preserved_separately(self) -> None:
        record = self.load(EDITIONS)
        self.assertFalse(record["authoritative"])
        self.assertEqual(D11_ID, record["decision_ref"])
        candidates = {item["id"]: item for item in record["candidates"]}
        self.assertEqual(CANDIDATE_IDS, set(candidates))
        self.assertEqual("2016 Kindle edition", candidates["neurodiversity-source-singer-2016-kindle"]["edition_identity"])
        self.assertEqual(2016, candidates["neurodiversity-source-singer-2016-kindle"]["publication_year"])
        self.assertEqual("Kindle", candidates["neurodiversity-source-singer-2016-kindle"]["format"])
        self.assertEqual("revised 2017 print edition", candidates["neurodiversity-source-singer-2017-revised-print"]["edition_identity"])
        self.assertEqual(2017, candidates["neurodiversity-source-singer-2017-revised-print"]["publication_year"])
        self.assertEqual("print", candidates["neurodiversity-source-singer-2017-revised-print"]["format"])
        for candidate in candidates.values():
            self.assertEqual("not_accepted_by_d11", candidate["full_schema_date_status"])
            self.assertEqual("edition_specific_evidence_required", candidate["contribution_status"])
            self.assertNotIn("contributions", candidate)
        self.assertFalse(record["boundaries"]["claim_support_copying_authorised"])

    def test_authoritative_v01_source_and_historical_research_snapshot_remain_unchanged(self) -> None:
        self.assertEqual(SOURCE_BLOB, git_blob_sha(SOURCE))
        source = self.load(SOURCE)
        legacy = next(item for item in source["sources"] if item["id"] == "neurodiversity-source-singer")
        self.assertIn("(2016)", legacy["citation"])
        self.assertEqual("https://wellcomecollection.org/works/ywrdd8ff", legacy["url"])

        research = self.load(RESEARCH)
        singer = research["sources"]["neurodiversity-source-singer"]
        self.assertEqual("pending_owner_reconciliation", singer["metadata"]["date"]["status"])
        candidates = {item["id"]: item for item in research["decision_candidates"]}
        self.assertEqual("owner_decision_required", candidates["nd-singer-edition-reconciliation"]["status"])

    def test_pair_binds_d11_without_copying_claim_support_or_closing_other_blockers(self) -> None:
        pair = self.load(PAIR)
        self.assertIn(D11_ID, pair["accepted_owner_decisions"])
        self.assertTrue(pair["authorisations"]["neurodiversity_singer_edition_identity_split_accepted"])
        self.assertFalse(pair["authorisations"]["neurodiversity_singer_select_single_edition"])
        self.assertFalse(pair["authorisations"]["neurodiversity_singer_combine_editions"])
        self.assertFalse(pair["authorisations"]["neurodiversity_singer_auto_duplicate_claim_support"])
        blockers = {item["id"]: item for item in pair["blockers"]}
        evidence = blockers["neurodiversity-evidence-enrichment"]
        self.assertEqual("identity_split_accepted_contributions_pending", evidence["kind"])
        self.assertIn("edition-specific evidential support", evidence["detail"])
        self.assertIn("paired-structural-relation-confidence", blockers)
        self.assertIn("autism-uncertainty-shape", blockers)
        self.assertIn("neurodiversity-uncertainty-shape", blockers)
        self.assertIn("neurodiversity-adhd-structural-edge", blockers)
        relations = [item["structural_relation"] for item in pair["objects"]]
        self.assertTrue(all("confidence" not in relation for relation in relations))
        self.assertFalse(pair["authorisations"]["authoritative_neurodiversity_v01_mutation"])
        self.assertFalse(pair["authorisations"]["authoritative_v02_replacement"])


if __name__ == "__main__":
    unittest.main()
