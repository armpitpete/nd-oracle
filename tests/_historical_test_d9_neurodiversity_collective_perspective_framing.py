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
D9_BASE = "3365190d8acc00c80439fa079f13de17c1346612"
D9_ID = "d9-neurodiversity-collective-perspective-framing"
PERSPECTIVE_ID = "neurodiversity-perspective-collective"
EXPECTED_FIELDS = {
    "held_by.scope": "Botha, Chapman, Giwa Onaiwu, Kapp, Stannard Ashley and Walker as an international group of autistic scholars writing on the historical origins of neurodiversity; not a statement representing all autistic people or all neurodiversity scholarship.",
    "reasoning": "The authors compare dated archival and published evidence from autistic online-community discussion, Singer's 1998 thesis, Blume's 1997 and 1998 writing, and a reported 1996 InLv post, and conclude that the concept and theorising of neurodiversity have multiple, collective origins.",
    "scope": "Historical attribution of the origins and early theorising of neurodiversity; excludes ownership of later meanings, a complete history of every contributor, and representation of all contemporary neurodiversity positions.",
}


class D9NeurodiversityCollectivePerspectiveFramingTests(unittest.TestCase):
    def load(self, path: Path) -> dict:
        return json.loads(path.read_text(encoding="utf-8"))

    def d9(self) -> dict:
        decisions = self.load(DECISIONS)["decisions"]
        return next(item for item in decisions if item["id"] == D9_ID)

    def test_d9_records_exact_owner_acceptance(self) -> None:
        decision = self.d9()
        self.assertEqual("accepted", decision["status"])
        self.assertEqual(D9_BASE, decision["accepted_against_main"])
        self.assertEqual(PERSPECTIVE_ID, decision["perspective_id"])
        self.assertEqual(EXPECTED_FIELDS, decision["accepted_fields"])
        self.assertEqual("nd-collective-perspective-framing", decision["supersedes_research_decision_candidate"]["id"])

    def test_research_snapshot_matches_but_remains_historical(self) -> None:
        research = self.load(RESEARCH)
        proposal = research["sources"]["neurodiversity-source-botha"]["perspective_proposals"][PERSPECTIVE_ID]
        self.assertEqual("owner_decision_required", proposal["status"])
        self.assertEqual(EXPECTED_FIELDS["held_by.scope"], proposal["held_by_scope"])
        self.assertEqual(EXPECTED_FIELDS["reasoning"], proposal["reasoning"])
        self.assertEqual(EXPECTED_FIELDS["scope"], proposal["scope"])
        candidates = {item["id"]: item for item in research["decision_candidates"]}
        self.assertEqual("owner_decision_required", candidates["nd-collective-perspective-framing"]["status"])

    def test_authoritative_neurodiversity_source_is_unchanged(self) -> None:
        self.assertEqual(SOURCE_BLOB, git_blob_sha(SOURCE))
        source = self.load(SOURCE)
        perspective = next(item for item in source["perspectives"] if item["id"] == PERSPECTIVE_ID)
        self.assertNotIn("reasoning", perspective)
        self.assertNotIn("scope", perspective)

    def test_pair_preserves_d9_without_freezing_later_governance_state(self) -> None:
        pair = self.load(PAIR)
        self.assertIn(D9_ID, pair["accepted_owner_decisions"])
        self.assertTrue(pair["authorisations"]["neurodiversity_collective_perspective_framing_accepted"])
        self.assertTrue(any(item["id"] == "neurodiversity-uncertainty-shape" for item in pair["blockers"]))
        self.assertTrue(any(item["id"] == "neurodiversity-adhd-structural-edge" for item in pair["blockers"]))
        relations = [item["structural_relation"] for item in pair["objects"]]
        self.assertTrue(all("confidence" not in relation for relation in relations))
        self.assertFalse(pair["authorisations"]["authoritative_neurodiversity_v01_mutation"])
        self.assertFalse(pair["authorisations"]["authoritative_v02_replacement"])


if __name__ == "__main__":
    unittest.main()
