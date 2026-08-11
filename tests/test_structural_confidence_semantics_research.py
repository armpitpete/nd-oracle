import hashlib
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESEARCH = ROOT / "migration-candidates" / "autism-neurodiversity" / "structural-confidence-semantics-research.json"
COMMON = ROOT / "schema" / "common-v0.2.json"
AUTISM = ROOT / "objects" / "concepts" / "autism.json"
NEURODIVERSITY = ROOT / "objects" / "concepts" / "neurodiversity.json"
ADHD = ROOT / "objects" / "concepts" / "adhd.json"
D6_FIXTURE = ROOT / "tests" / "fixtures" / "migration" / "autism" / "owner-decisions.json"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def git_blob_sha(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


class StructuralConfidenceSemanticsResearchTests(unittest.TestCase):
    def test_research_is_non_authoritative_and_bound_to_current_main(self) -> None:
        research = load(RESEARCH)
        self.assertEqual(research["research_version"], "1.0")
        self.assertEqual(
            research["prepared_against_main"],
            "31c244ecff0a52c53c38f60cc57815587e9b0856",
        )
        self.assertFalse(research["authoritative"])
        self.assertFalse(research["authoritative_replacement"])
        self.assertTrue(all(value is False for value in research["boundaries"].values()))

    def test_schema_and_authoritative_sources_remain_exact(self) -> None:
        self.assertEqual(git_blob_sha(COMMON), "ce0141ee7031f21fa2bd72b2faa3371aed3e622b")
        self.assertEqual(git_blob_sha(AUTISM), "b2d3809ecfcdb1d81c793a2401f0533a4b17ea98")
        self.assertEqual(git_blob_sha(NEURODIVERSITY), "5a38bc4250079412dd3f4da1d598dfcab984ca66")
        self.assertEqual(git_blob_sha(ADHD), "719f26a9af773cd1bcf670df4d12ed5f6bcf0a23")
        self.assertEqual(git_blob_sha(D6_FIXTURE), "595f221e2f8d622dc94fc63bfdc8b34c1ebe3f56")

    def test_legacy_notes_are_discourse_association_not_explicit_taxonomy_claims(self) -> None:
        autism = load(AUTISM)
        neurodiversity = load(NEURODIVERSITY)
        adhd = load(ADHD)

        autism_edge = next(r for r in autism["relations"] if r["target_id"] == "neurodiversity")
        adhd_edge = next(r for r in adhd["relations"] if r["target_id"] == "neurodiversity")
        nd_autism = next(r for r in neurodiversity["relations"] if r["target_id"] == "autism")
        nd_adhd = next(r for r in neurodiversity["relations"] if r["target_id"] == "adhd")

        self.assertEqual(autism_edge["note"], "Autism is commonly situated within neurodiversity discourse.")
        self.assertEqual(adhd_edge["note"], "ADHD is commonly situated within neurodiversity discourse.")
        self.assertEqual(nd_autism["note"], "Autism is commonly discussed within the neurodiversity ecosystem.")
        self.assertEqual(nd_adhd["note"], "ADHD is commonly discussed within the neurodiversity ecosystem.")

    def test_d6_still_forbids_confidence_shortcuts(self) -> None:
        decisions = load(D6_FIXTURE)["decisions"]
        d6 = next(item for item in decisions if item["id"] == "d6-structural-relation-confidence")
        self.assertEqual(d6["status"], "accepted")
        self.assertFalse(d6["infer_or_default_confidence_authorised"])
        self.assertFalse(d6["use_not_applicable_as_validation_shortcut_authorised"])
        self.assertTrue(d6["evidence_backed_confidence_enrichment_allowed"])
        self.assertTrue(d6["separate_structural_confidence_schema_policy_allowed"])
        self.assertTrue(d6["current_candidate_confidence_must_remain_absent"])

    def test_research_rejects_current_confidence_enrichment_and_schema_shortcuts(self) -> None:
        research = load(RESEARCH)
        options = {item["id"]: item for item in research["options"]}
        self.assertEqual(options["evidence-backed-confidence-on-current-edge"]["status"], "not_ready")
        self.assertEqual(options["use-not-applicable"]["status"], "rejected")
        self.assertEqual(options["default-or-infer-confidence"]["status"], "rejected")
        self.assertEqual(options["make-confidence-optional-without-explicit-state"]["status"], "rejected")
        self.assertEqual(options["review-relation-semantics-before-confidence"]["status"], "recommended")

    def test_future_explicit_assessment_state_is_only_plausible_not_accepted(self) -> None:
        research = load(RESEARCH)
        options = {item["id"]: item for item in research["options"]}
        future = options["explicit-relation-confidence-assessment-state"]
        self.assertEqual(future["status"], "plausible_future_schema_policy")
        self.assertEqual(
            future["candidate_shape"]["confidence_assessment_state"],
            ["assessed", "legacy_not_recorded"],
        )
        self.assertFalse(research["boundaries"]["schema_change_authorised"])
        self.assertFalse(research["boundaries"]["validator_change_authorised"])

    def test_external_evidence_is_bounded_to_terminology_findings(self) -> None:
        research = load(RESEARCH)
        evidence = {item["id"]: item for item in research["external_evidence"]}
        self.assertEqual(
            set(evidence),
            {
                "nas-autism-neurodiversity",
                "nhs-autism-definition",
                "nhs-england-adhd-taskforce-neurodiversity",
            },
        )
        for item in evidence.values():
            self.assertEqual(item["accessed"], "2026-08-11")
            self.assertTrue(item["url"].startswith("https://"))
            self.assertTrue(item["relevant_findings"])

    def test_owner_decision_candidate_is_semantic_review_priority_only(self) -> None:
        research = load(RESEARCH)
        decision = research["decision_candidate"]
        self.assertEqual(decision["id"], "nd-structural-semantics-before-confidence")
        self.assertEqual(decision["status"], "owner_decision_required")
        self.assertIn("do not yet choose a replacement relation type", decision["recommended_action"].lower())
        self.assertIn("do not yet choose a replacement relation type", decision["recommended_action"].lower())
        self.assertFalse(research["boundaries"]["relation_type_change_authorised"])
        self.assertFalse(research["boundaries"]["relation_target_change_authorised"])
        self.assertFalse(research["boundaries"]["confidence_enrichment_authorised"])


if __name__ == "__main__":
    unittest.main()
