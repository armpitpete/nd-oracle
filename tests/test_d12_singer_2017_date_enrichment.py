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
D12_ID = "d12-singer-2017-date-enrichment"
D12_BASE = "f56355b7edaec7fad020bebeab0d80ec04ebc37e"
SOURCE_BLOB = "5a38bc4250079412dd3f4da1d598dfcab984ca66"
PRINT_ID = "neurodiversity-source-singer-2017-revised-print"
KINDLE_ID = "neurodiversity-source-singer-2016-kindle"


class D12Singer2017DateEnrichmentTests(unittest.TestCase):
    def load(self, path: Path) -> dict:
        return json.loads(path.read_text(encoding="utf-8"))

    def test_d12_records_exact_accepted_date_and_boundaries(self) -> None:
        decisions = self.load(DECISIONS)["decisions"]
        decision = next(item for item in decisions if item["id"] == D12_ID)
        self.assertEqual("accepted", decision["status"])
        self.assertEqual(D12_BASE, decision["accepted_against_main"])
        self.assertEqual(PRINT_ID, decision["evidence_id"])
        self.assertEqual("2017-09-05", decision["accepted_full_publication_date"])
        self.assertEqual(
            "nd-singer-2017-date-enrichment",
            decision["supersedes_research_decision_candidate"]["id"],
        )
        self.assertTrue(decision["preserve_authoritative_v01_source_unchanged"])
        self.assertFalse(decision["accept_2016_full_date"])
        self.assertFalse(decision["accept_any_contribution_binding"])
        self.assertFalse(decision["authoritative_evidence_authorised"])
        self.assertFalse(decision["authoritative_v01_mutation_authorised"])
        self.assertFalse(decision["authoritative_v02_replacement_authorised"])

    def test_only_2017_candidate_gains_accepted_full_date(self) -> None:
        record = self.load(EDITIONS)
        self.assertFalse(record["authoritative"])
        self.assertIn(D12_ID, record["accepted_enrichment_decision_refs"])
        candidates = {item["id"]: item for item in record["candidates"]}
        printed = candidates[PRINT_ID]
        kindle = candidates[KINDLE_ID]
        self.assertEqual("2017-09-05", printed["publication_date"])
        self.assertEqual(
            "accepted_by_d12_for_future_non_authoritative_candidate",
            printed["full_schema_date_status"],
        )
        self.assertEqual(D12_ID, printed["date_decision_ref"])
        self.assertNotIn("publication_date", kindle)
        self.assertEqual("not_accepted_by_d11", kindle["full_schema_date_status"])

    def test_no_contribution_binding_is_accepted_or_copied(self) -> None:
        record = self.load(EDITIONS)
        for candidate in record["candidates"]:
            self.assertEqual("edition_specific_evidence_required", candidate["contribution_status"])
            self.assertNotIn("contributions", candidate)
        self.assertFalse(record["boundaries"]["claim_support_copying_authorised"])

    def test_historical_research_snapshot_is_preserved(self) -> None:
        research = self.load(RESEARCH)
        printed = research["edition_assessments"][PRINT_ID]["publication_date"]
        kindle = research["edition_assessments"][KINDLE_ID]["publication_date"]
        self.assertEqual("corroborated_catalogue_candidate", printed["status"])
        self.assertEqual("2017-09-05", printed["proposed_value"])
        self.assertEqual("secondary_catalogue_candidate_not_yet_verified_enrichment", kindle["status"])
        decisions = {item["id"]: item for item in research["next_decision_candidates"]}
        self.assertEqual("owner_decision_required", decisions["nd-singer-2017-date-enrichment"]["status"])

    def test_pair_binds_d12_and_preserves_all_other_blockers(self) -> None:
        pair = self.load(PAIR)
        self.assertIn(D12_ID, pair["accepted_owner_decisions"])
        self.assertTrue(pair["authorisations"]["neurodiversity_singer_2017_full_date_accepted"])
        self.assertFalse(pair["authorisations"]["neurodiversity_singer_2016_full_date_accepted"])
        self.assertFalse(pair["authorisations"]["neurodiversity_singer_contribution_bindings_accepted"])
        blockers = {item["id"]: item for item in pair["blockers"]}
        evidence = blockers["neurodiversity-evidence-enrichment"]
        self.assertEqual("2017_date_accepted_contribution_review_pending", evidence["kind"])
        self.assertIn("No Singer contribution binding is accepted", evidence["detail"])
        self.assertIn("paired-structural-relation-confidence", blockers)
        self.assertIn("autism-uncertainty-shape", blockers)
        self.assertIn("neurodiversity-uncertainty-shape", blockers)
        self.assertIn("neurodiversity-adhd-structural-edge", blockers)
        self.assertFalse(pair["authorisations"]["authoritative_v02_replacement"])

    def test_authoritative_v01_is_byte_identical(self) -> None:
        self.assertEqual(SOURCE_BLOB, git_blob_sha(SOURCE))


if __name__ == "__main__":
    unittest.main()
