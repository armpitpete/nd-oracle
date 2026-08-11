from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.validate_migration import git_blob_sha

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "objects" / "concepts" / "neurodiversity.json"
RESEARCH = ROOT / "migration-candidates" / "autism-neurodiversity" / "singer-edition-enrichment-research.json"
EDITIONS = ROOT / "migration-candidates" / "autism-neurodiversity" / "singer-edition-candidates.json"
PAIR = ROOT / "migration-candidates" / "autism-neurodiversity" / "structural-candidate.json"
BASE = "0c685304b185794c344eb29c1976ee7811714380"
SOURCE_BLOB = "5a38bc4250079412dd3f4da1d598dfcab984ca66"


class SingerEditionEnrichmentResearchTests(unittest.TestCase):
    def load(self, path: Path) -> dict:
        return json.loads(path.read_text(encoding="utf-8"))

    def test_research_is_non_authoritative_and_source_anchored(self) -> None:
        research = self.load(RESEARCH)
        self.assertEqual("1.0", research["research_version"])
        self.assertEqual(BASE, research["prepared_against_main"])
        self.assertFalse(research["authoritative"])
        self.assertFalse(research["authoritative_replacement"])
        self.assertEqual(SOURCE_BLOB, research["legacy_source_anchor"]["blob_sha"])
        self.assertEqual(SOURCE_BLOB, git_blob_sha(SOURCE))
        self.assertTrue(all(value is False for value in research["boundaries"].values()))

    def test_date_evidence_strength_is_not_flattened(self) -> None:
        research = self.load(RESEARCH)["edition_assessments"]
        kindle = research["neurodiversity-source-singer-2016-kindle"]["publication_date"]
        printed = research["neurodiversity-source-singer-2017-revised-print"]["publication_date"]
        self.assertEqual("2016-07-03", kindle["proposed_value"])
        self.assertEqual("secondary_catalogue_candidate_not_yet_verified_enrichment", kindle["status"])
        self.assertEqual("2017-09-05", printed["proposed_value"])
        self.assertEqual("corroborated_catalogue_candidate", printed["status"])
        self.assertNotEqual(kindle["status"], printed["status"])

    def test_contribution_bindings_are_edition_specific_and_bounded(self) -> None:
        research = self.load(RESEARCH)["edition_assessments"]
        kindle = research["neurodiversity-source-singer-2016-kindle"]["contribution_bindings"]
        printed = research["neurodiversity-source-singer-2017-revised-print"]["contribution_bindings"]
        self.assertEqual("owner_review_candidate", kindle["neurodiversity-claim-1"]["status"])
        self.assertEqual("owner_review_candidate_with_direct_text_preferred", kindle["neurodiversity-claim-2"]["status"])
        self.assertEqual("owner_review_candidate", printed["neurodiversity-claim-1"]["status"])
        self.assertEqual("owner_review_candidate", printed["neurodiversity-claim-2"]["status"])
        for edition in (kindle, printed):
            for binding in edition.values():
                self.assertEqual("compatible", binding["proposed_role"])
                self.assertTrue(binding["edition_specific_routes"])
                self.assertTrue(binding["source_research_ref"])

    def test_d11_identity_record_remains_non_authoritative_and_does_not_gain_contributions(self) -> None:
        editions = self.load(EDITIONS)
        self.assertFalse(editions["authoritative"])
        self.assertIn(
            "migration-candidates/autism-neurodiversity/singer-edition-enrichment-research.json",
            editions["research_refs"],
        )
        for candidate in editions["candidates"]:
            self.assertEqual("not_accepted_by_d11", candidate["full_schema_date_status"])
            self.assertEqual("edition_specific_evidence_required", candidate["contribution_status"])
            self.assertNotIn("contributions", candidate)
        self.assertFalse(editions["boundaries"]["claim_support_copying_authorised"])

    def test_pair_records_research_without_closing_other_blockers(self) -> None:
        pair = self.load(PAIR)
        self.assertTrue(pair["authorisations"]["neurodiversity_singer_enrichment_research_prepared"])
        evidence = next(item for item in pair["blockers"] if item["id"] == "neurodiversity-evidence-enrichment")
        self.assertEqual("edition_enrichment_research_prepared_owner_review_pending", evidence["kind"])
        blockers = {item["id"] for item in pair["blockers"]}
        self.assertIn("paired-structural-relation-confidence", blockers)
        self.assertIn("autism-uncertainty-shape", blockers)
        self.assertIn("neurodiversity-uncertainty-shape", blockers)
        self.assertIn("neurodiversity-adhd-structural-edge", blockers)
        self.assertFalse(pair["authorisations"]["authoritative_v02_replacement"])


if __name__ == "__main__":
    unittest.main()
