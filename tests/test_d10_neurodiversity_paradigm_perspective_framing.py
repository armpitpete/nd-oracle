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
SOURCE_BLOB = "5a38bc4250079412dd3f4da1d598dfcab984ca66"
D10_BASE = "de2d111cb465d30c03b90f99eb4f43781be9b16c"
D10_ID = "d10-neurodiversity-paradigm-perspective-framing"
PERSPECTIVE_ID = "neurodiversity-perspective-paradigm"
EXPECTED_FIELDS = {
    "held_by.scope": "Neurodiversity advocates and scholars using disability-rights, sociological and inclusion-oriented framings; not a claim that all neurodivergent people, clinicians, researchers or advocates hold one position.",
    "reasoning": "Singer's work situates neurological variation within disability-rights, social-constructionist and feminist analysis, combines autobiographical and autistic-community observation, and argues for balancing medical accounts with sociological or adaptive understandings rather than treating diagnosis as the whole meaning of difference.",
    "scope": "A social and political framing of neurological variation, disability, rights, environment, inclusion and movement-building; excludes individual diagnosis, person-specific support prescriptions and any claim that all neurological differences are beneficial.",
}


class D10NeurodiversityParadigmPerspectiveFramingTests(unittest.TestCase):
    def load(self, path: Path) -> dict:
        return json.loads(path.read_text(encoding="utf-8"))

    def d10(self) -> dict:
        decisions = self.load(DECISIONS)["decisions"]
        return next(item for item in decisions if item["id"] == D10_ID)

    def test_d10_records_exact_owner_acceptance(self) -> None:
        decision = self.d10()
        self.assertEqual("accepted", decision["status"])
        self.assertEqual(D10_BASE, decision["accepted_against_main"])
        self.assertEqual(PERSPECTIVE_ID, decision["perspective_id"])
        self.assertEqual(EXPECTED_FIELDS, decision["accepted_fields"])
        self.assertEqual("nd-paradigm-perspective-framing", decision["supersedes_research_decision_candidate"]["id"])
        self.assertFalse(decision["authoritative_perspective_authorised"])
        self.assertFalse(decision["authoritative_v01_mutation_authorised"])
        self.assertFalse(decision["authoritative_v02_replacement_authorised"])
        self.assertFalse(decision["schema_change_authorised"])
        self.assertFalse(decision["publication_or_deployment_authorised"])

    def test_research_snapshot_matches_but_remains_historical(self) -> None:
        research = self.load(RESEARCH)
        proposal = research["sources"]["neurodiversity-source-singer"]["perspective_proposals"][PERSPECTIVE_ID]
        self.assertEqual("owner_decision_required", proposal["status"])
        self.assertEqual(EXPECTED_FIELDS["held_by.scope"], proposal["held_by_scope"])
        self.assertEqual(EXPECTED_FIELDS["reasoning"], proposal["reasoning"])
        self.assertEqual(EXPECTED_FIELDS["scope"], proposal["scope"])
        candidates = {item["id"]: item for item in research["decision_candidates"]}
        self.assertEqual("owner_decision_required", candidates["nd-paradigm-perspective-framing"]["status"])

    def test_authoritative_neurodiversity_source_is_unchanged(self) -> None:
        self.assertEqual(SOURCE_BLOB, git_blob_sha(SOURCE))
        source = self.load(SOURCE)
        perspective = next(item for item in source["perspectives"] if item["id"] == PERSPECTIVE_ID)
        self.assertNotIn("reasoning", perspective)
        self.assertNotIn("scope", perspective)

    def test_pair_binds_d10_and_closes_only_perspective_framing_blocker(self) -> None:
        pair = self.load(PAIR)
        self.assertIn(D10_ID, pair["accepted_owner_decisions"])
        self.assertTrue(pair["authorisations"]["neurodiversity_paradigm_perspective_framing_accepted"])
        self.assertTrue(pair["authorisations"]["neurodiversity_collective_perspective_framing_accepted"])
        self.assertTrue(pair["authorisations"]["neurodiversity_all_perspective_framings_accepted"])
        blockers = {item["id"]: item for item in pair["blockers"]}
        self.assertNotIn("neurodiversity-perspective-framing", blockers)
        self.assertIn("paired-structural-relation-confidence", blockers)
        self.assertIn("autism-uncertainty-shape", blockers)
        self.assertIn("neurodiversity-evidence-enrichment", blockers)
        self.assertIn("neurodiversity-uncertainty-shape", blockers)
        self.assertIn("neurodiversity-adhd-structural-edge", blockers)
        self.assertIn("Singer date/edition identity remains unresolved", blockers["neurodiversity-evidence-enrichment"]["detail"])
        relations = [item["structural_relation"] for item in pair["objects"]]
        self.assertTrue(all("confidence" not in relation for relation in relations))
        self.assertFalse(pair["authorisations"]["authoritative_neurodiversity_v01_mutation"])
        self.assertFalse(pair["authorisations"]["authoritative_v02_replacement"])


if __name__ == "__main__":
    unittest.main()
