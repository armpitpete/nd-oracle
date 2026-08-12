from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.validate_migration import git_blob_sha

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "objects" / "concepts" / "neurodiversity.json"
RESEARCH = ROOT / "migration-candidates" / "autism-neurodiversity" / "neurodiversity-enrichment-research.json"
PAIR = ROOT / "migration-candidates" / "autism-neurodiversity" / "structural-candidate.json"
NEURODIVERSITY_BLOB = "5a38bc4250079412dd3f4da1d598dfcab984ca66"
RESEARCH_BASE = "26ee009309efd624c9da661bd168522a3089932c"


class NeurodiversityEnrichmentResearchTests(unittest.TestCase):
    def load(self, path: Path) -> dict:
        return json.loads(path.read_text(encoding="utf-8"))

    def test_research_is_non_authoritative_and_source_anchored(self) -> None:
        research = self.load(RESEARCH)
        self.assertEqual("1.0", research["research_version"])
        self.assertEqual(RESEARCH_BASE, research["prepared_against_main"])
        self.assertFalse(research["authoritative"])
        self.assertFalse(research["authoritative_replacement"])
        self.assertEqual(NEURODIVERSITY_BLOB, research["source_anchors"]["neurodiversity"]["blob_sha"])
        self.assertEqual(NEURODIVERSITY_BLOB, git_blob_sha(SOURCE))
        self.assertTrue(all(value is False for value in research["boundaries"].values()))

    def test_singer_metadata_preserves_edition_conflict(self) -> None:
        research = self.load(RESEARCH)
        singer = research["sources"]["neurodiversity-source-singer"]
        self.assertEqual("NeuroDiversity: The Birth of an Idea", singer["metadata"]["title"]["value"])
        self.assertEqual("Judy Singer", singer["metadata"]["authorship"]["value"])
        self.assertEqual("pending_owner_reconciliation", singer["metadata"]["date"]["status"])
        self.assertIsNone(singer["metadata"]["date"]["value"])
        decisions = {item["id"]: item for item in research["decision_candidates"]}
        self.assertEqual("owner_decision_required", decisions["nd-singer-edition-reconciliation"]["status"])
        source = self.load(SOURCE)
        legacy = next(item for item in source["sources"] if item["id"] == "neurodiversity-source-singer")
        self.assertIn("(2016)", legacy["citation"])
        self.assertEqual("https://wellcomecollection.org/works/ywrdd8ff", legacy["url"])

    def test_botha_metadata_and_citation_correction_are_evidence_backed_only(self) -> None:
        research = self.load(RESEARCH)
        botha = research["sources"]["neurodiversity-source-botha"]
        self.assertEqual("2024-03-12", botha["metadata"]["date"]["value"])
        self.assertIn("Monique Botha", botha["metadata"]["authorship"]["value"])
        correction = botha["metadata"]["citation_correction"]
        self.assertEqual("verified_proposal_owner_acceptance_required", correction["status"])
        self.assertIn("10.1177/13623613241237871", correction["value"])
        source = self.load(SOURCE)
        legacy = next(item for item in source["sources"] if item["id"] == "neurodiversity-source-botha")
        self.assertEqual("10.1080/09687599.2024.2327837", legacy["doi"])
        decisions = {item["id"]: item for item in research["decision_candidates"]}
        self.assertEqual("owner_decision_required", decisions["nd-botha-citation-correction"]["status"])

    def test_claim_contribution_roles_and_limitations_remain_bounded(self) -> None:
        research = self.load(RESEARCH)
        singer = research["sources"]["neurodiversity-source-singer"]["contributions"]
        botha = research["sources"]["neurodiversity-source-botha"]["contributions"]
        self.assertEqual("compatible", singer["neurodiversity-claim-1"]["role"])
        self.assertEqual("compatible", singer["neurodiversity-claim-2"]["role"])
        self.assertEqual("supportive", botha["neurodiversity-claim-1"]["role"])
        for contribution in [*singer.values(), *botha.values()]:
            self.assertTrue(contribution["finding"])
            self.assertTrue(contribution["population_or_context"])
            self.assertTrue(contribution["methodology"])
            self.assertTrue(contribution["limitations"])
            limitation = contribution["limitations"][0]
            self.assertEqual(
                {"statement", "why_it_matters", "reopening_or_reduction_condition"},
                set(limitation),
            )

    def test_research_snapshot_preserves_perspective_proposals_and_structural_boundaries(self) -> None:
        research = self.load(RESEARCH)
        singer_p = research["sources"]["neurodiversity-source-singer"]["perspective_proposals"]["neurodiversity-perspective-paradigm"]
        botha_p = research["sources"]["neurodiversity-source-botha"]["perspective_proposals"]["neurodiversity-perspective-collective"]
        self.assertEqual("owner_decision_required", singer_p["status"])
        self.assertEqual("owner_decision_required", botha_p["status"])
        self.assertTrue(singer_p["held_by_scope"] and singer_p["reasoning"] and singer_p["scope"])
        self.assertTrue(botha_p["held_by_scope"] and botha_p["reasoning"] and botha_p["scope"])

        source = self.load(SOURCE)
        self.assertTrue(all(isinstance(item["what_would_reduce_it"], list) for item in source["uncertainties"]))
        self.assertTrue(any(item["type"] == "broader_than" and item["target_id"] == "adhd" for item in source["relations"]))

        pair = self.load(PAIR)
        self.assertIn("migration-candidates/autism-neurodiversity/neurodiversity-enrichment-research.json", pair["research_refs"])
        by_id = {item["id"]: item for item in pair["blockers"]}
        self.assertIn("neurodiversity-evidence-enrichment", by_id)
        self.assertIn("neurodiversity-uncertainty-shape", by_id)
        self.assertEqual("structural_dependency", by_id["neurodiversity-adhd-structural-edge"]["kind"])
        relations = [item["structural_relation"] for item in pair["objects"]]
        self.assertTrue(all("confidence" not in relation for relation in relations))
        self.assertFalse(pair["authorisations"]["neurodiversity_research_accepts_pending_owner_decisions"])


if __name__ == "__main__":
    unittest.main()
