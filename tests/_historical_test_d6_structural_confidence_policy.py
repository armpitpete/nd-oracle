from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.validate_migration import git_blob_sha

ROOT = Path(__file__).resolve().parents[1]
OWNER_DECISIONS = ROOT / "tests" / "fixtures" / "migration" / "autism" / "owner-decisions.json"
PAIR = ROOT / "migration-candidates" / "autism-neurodiversity" / "structural-candidate.json"
AUTISM = ROOT / "objects" / "concepts" / "autism.json"
NEURODIVERSITY = ROOT / "objects" / "concepts" / "neurodiversity.json"
AUTISM_BLOB = "b2d3809ecfcdb1d81c793a2401f0533a4b17ea98"
NEURODIVERSITY_BLOB = "5a38bc4250079412dd3f4da1d598dfcab984ca66"


class D6StructuralConfidencePolicyTests(unittest.TestCase):
    def test_d6_records_no_default_and_no_not_applicable_shortcut(self) -> None:
        decisions = json.loads(OWNER_DECISIONS.read_text(encoding="utf-8"))["decisions"]
        d6 = next(item for item in decisions if item["id"] == "d6-structural-relation-confidence")
        self.assertEqual("accepted", d6["status"])
        self.assertEqual("653938871190b454696df12abcc5bc0260ce19fd", d6["accepted_against_main"])
        self.assertFalse(d6["infer_or_default_confidence_authorised"])
        self.assertFalse(d6["use_not_applicable_as_validation_shortcut_authorised"])
        self.assertTrue(d6["evidence_backed_confidence_enrichment_allowed"])
        self.assertTrue(d6["separate_structural_confidence_schema_policy_allowed"])
        self.assertTrue(d6["current_candidate_confidence_must_remain_absent"])
        self.assertFalse(d6["schema_change_authorised"])
        self.assertFalse(d6["authoritative_v01_mutation_authorised"])
        self.assertFalse(d6["authoritative_v02_replacement_authorised"])

    def test_d17_avoids_manufacturing_confidence_by_emitting_no_v02_edge(self) -> None:
        candidate = json.loads(PAIR.read_text(encoding="utf-8"))
        self.assertEqual("d6-structural-relation-confidence", candidate["confidence_policy_ref"])
        self.assertEqual(
            "d17-neurodiversity-legacy-structural-disposition",
            candidate["structural_disposition_decision_ref"],
        )
        for obj in candidate["objects"]:
            relation = obj["structural_relation"]
            self.assertEqual("legacy_retained_unmapped", relation["disposition"])
            self.assertFalse(relation["emit_v02_semantic_edge"])
            self.assertNotIn("type", relation)
            self.assertNotIn("target", relation)
            self.assertNotIn("confidence", relation)
            self.assertEqual("not_required_without_v02_edge", relation["confidence_status"])
            self.assertEqual("d6-structural-relation-confidence", relation["confidence_policy_ref"])
        self.assertFalse(candidate["authorisations"]["infer_or_default_structural_confidence"])
        self.assertFalse(candidate["authorisations"]["use_not_applicable_as_confidence_shortcut"])
        self.assertFalse(candidate["authorisations"]["paired_structural_confidence_required_for_legacy_pair"])
        self.assertFalse(candidate["authorisations"]["new_semantic_graph_relation_authorised"])

    def test_authoritative_sources_remain_exact(self) -> None:
        self.assertEqual(AUTISM_BLOB, git_blob_sha(AUTISM))
        self.assertEqual(NEURODIVERSITY_BLOB, git_blob_sha(NEURODIVERSITY))


if __name__ == "__main__":
    unittest.main()
