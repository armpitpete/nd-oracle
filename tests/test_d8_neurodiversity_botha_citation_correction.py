from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.validate_migration import git_blob_sha

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "objects" / "concepts" / "neurodiversity.json"
DECISIONS = ROOT / "migration-candidates" / "autism-neurodiversity" / "owner-decisions.json"
RESEARCH = ROOT / "migration-candidates" / "autism-neurodiversity" / "neurodiversity-enrichment-research.json"
PAIR = ROOT / "migration-candidates" / "autism-neurodiversity" / "structural-candidate.json"
NEURODIVERSITY_BLOB = "5a38bc4250079412dd3f4da1d598dfcab984ca66"
ACCEPTED_MAIN = "4b473f0130d8346c053089cbb86f9baedc549d3d"
LEGACY_DOI = "10.1080/09687599.2024.2327837"
ACCEPTED_DOI = "10.1177/13623613241237871"
D8_ID = "d8-neurodiversity-botha-citation-correction"


class D8NeurodiversityBothaCitationCorrectionTests(unittest.TestCase):
    def load(self, path: Path) -> dict:
        return json.loads(path.read_text(encoding="utf-8"))

    def d8(self) -> dict:
        decisions = self.load(DECISIONS)["decisions"]
        return next(item for item in decisions if item["id"] == D8_ID)

    def test_d8_records_exact_bounded_acceptance(self) -> None:
        d8 = self.d8()
        self.assertEqual("accepted", d8["status"])
        self.assertEqual(ACCEPTED_MAIN, d8["accepted_against_main"])
        self.assertEqual("neurodiversity-source-botha", d8["source_id"])
        self.assertEqual(ACCEPTED_DOI, d8["accepted_doi"])
        self.assertIn(ACCEPTED_DOI, d8["accepted_citation"])
        self.assertTrue(d8["preserve_legacy_v01_citation_and_doi"])
        self.assertEqual(LEGACY_DOI, d8["legacy_v01_doi"])
        self.assertFalse(d8["authoritative_v01_mutation_authorised"])
        self.assertFalse(d8["authoritative_v02_replacement_authorised"])
        self.assertFalse(d8["schema_change_authorised"])
        self.assertFalse(d8["publication_or_deployment_authorised"])

    def test_authoritative_v01_source_remains_exactly_unchanged(self) -> None:
        self.assertEqual(NEURODIVERSITY_BLOB, git_blob_sha(SOURCE))
        source = self.load(SOURCE)
        botha = next(item for item in source["sources"] if item["id"] == "neurodiversity-source-botha")
        self.assertEqual(LEGACY_DOI, botha["doi"])
        self.assertNotIn(ACCEPTED_DOI, botha["citation"])

    def test_d8_supersedes_only_botha_research_decision_candidate(self) -> None:
        d8 = self.d8()
        self.assertEqual(
            {
                "path": "migration-candidates/autism-neurodiversity/neurodiversity-enrichment-research.json",
                "id": "nd-botha-citation-correction",
            },
            d8["supersedes_research_decision_candidate"],
        )

        research = self.load(RESEARCH)
        candidates = {item["id"]: item for item in research["decision_candidates"]}
        self.assertEqual("owner_decision_required", candidates["nd-botha-citation-correction"]["status"])
        self.assertEqual("owner_decision_required", candidates["nd-singer-edition-reconciliation"]["status"])
        self.assertEqual("owner_decision_required", candidates["nd-paradigm-perspective-framing"]["status"])
        self.assertEqual("owner_decision_required", candidates["nd-collective-perspective-framing"]["status"])

    def test_paired_candidate_preserves_d8_and_unrelated_blockers(self) -> None:
        pair = self.load(PAIR)
        self.assertIn(D8_ID, pair["accepted_owner_decisions"])
        self.assertIn(
            "migration-candidates/autism-neurodiversity/owner-decisions.json",
            pair["owner_decision_refs"],
        )
        self.assertTrue(pair["authorisations"]["neurodiversity_botha_citation_correction_accepted"])
        self.assertFalse(pair["authorisations"]["neurodiversity_research_accepts_other_pending_owner_decisions"])

        blockers = {item["id"]: item for item in pair["blockers"]}
        self.assertIn("Singer date/edition identity remains unresolved", blockers["neurodiversity-evidence-enrichment"]["detail"])
        self.assertEqual("owner_decision", blockers["neurodiversity-uncertainty-shape"]["kind"])
        self.assertEqual("structural_dependency", blockers["neurodiversity-adhd-structural-edge"]["kind"])
        relations = [item["structural_relation"] for item in pair["objects"]]
        self.assertTrue(all("confidence" not in relation for relation in relations))


if __name__ == "__main__":
    unittest.main()
