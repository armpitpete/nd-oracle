import hashlib
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DECISIONS = ROOT / "migration-candidates" / "autism-neurodiversity" / "owner-decisions.json"
REVIEW = ROOT / "migration-candidates" / "autism-neurodiversity" / "relation-semantics-review.json"
COMMON = ROOT / "schema" / "common-v0.2.json"
AUTISM = ROOT / "objects" / "concepts" / "autism.json"
NEURODIVERSITY = ROOT / "objects" / "concepts" / "neurodiversity.json"
ADHD = ROOT / "objects" / "concepts" / "adhd.json"
DOC = ROOT / "docs" / "migration-proofs" / "D17_NEURODIVERSITY_LEGACY_STRUCTURAL_DISPOSITION.md"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def git_blob_sha(path: Path) -> str:
    data = path.read_bytes()
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


class D17NeurodiversityLegacyStructuralDispositionTests(unittest.TestCase):
    def test_d17_records_owner_acceptance_against_post_review_main(self) -> None:
        decisions = {item["id"]: item for item in load(DECISIONS)["decisions"]}
        d17 = decisions["d17-neurodiversity-legacy-structural-disposition"]
        self.assertEqual(d17["status"], "accepted")
        self.assertEqual(d17["accepted_on"], "2026-08-11")
        self.assertEqual(
            d17["accepted_against_main"],
            "586f9589c4c14a0bcb7a84bc0c579bfef94f6d7c",
        )
        self.assertEqual(
            d17["supersedes_research_decision_candidate"],
            {
                "path": "migration-candidates/autism-neurodiversity/relation-semantics-review.json",
                "id": "nd-neurodiversity-legacy-structural-disposition",
            },
        )

    def test_d17_accepts_lossless_unmapped_disposition_only(self) -> None:
        decisions = {item["id"]: item for item in load(DECISIONS)["decisions"]}
        d17 = decisions["d17-neurodiversity-legacy-structural-disposition"]
        disposition = d17["accepted_disposition"]
        self.assertTrue(disposition["preserve_reciprocal_legacy_records_together"])
        self.assertEqual(disposition["migration_status"], "legacy_retained_unmapped")
        self.assertTrue(disposition["preserve_exact_legacy_type_target_and_note"])
        self.assertFalse(disposition["emit_v02_taxonomy_edge"])
        self.assertTrue(disposition["preserve_d5_record_historically"])
        self.assertTrue(disposition["preserve_d6_record_historically"])
        self.assertTrue(disposition["supersede_d5_mapping_assumption_only"])
        self.assertTrue(disposition["future_semantic_graph_link_is_separate_enrichment"])
        self.assertTrue(disposition["adhd_consistency_test_only"])

        for field in (
            "paired_candidate_mutation_authorised",
            "schema_change_authorised",
            "validator_change_authorised",
            "replacement_relation_authorised",
            "relation_confidence_authorised",
            "new_relation_enrichment_authorised",
            "authoritative_v01_mutation_authorised",
            "authoritative_v02_replacement_authorised",
            "adhd_scope_expansion_authorised",
            "publication_or_deployment_authorised",
        ):
            self.assertFalse(d17[field], field)

    def test_research_candidate_remains_historical_and_unmodified(self) -> None:
        self.assertEqual(
            git_blob_sha(REVIEW),
            "45513bd4ad8918c9598bea7cd276cd345ac4c6ff",
        )
        review = load(REVIEW)
        self.assertEqual(
            review["decision_candidate"]["id"],
            "nd-neurodiversity-legacy-structural-disposition",
        )
        self.assertEqual(review["decision_candidate"]["status"], "owner_decision_required")
        self.assertEqual(
            review["recommended_direction"]["id"],
            "preserve-legacy-pair-without-v02-taxonomy",
        )

    def test_decision_record_proof_preserves_the_original_implementation_boundary(self) -> None:
        doc = DOC.read_text(encoding="utf-8")
        self.assertIn("legacy_retained_unmapped", doc)
        self.assertIn("do **not** emit", doc)
        self.assertIn("mutation of `structural-candidate.json`", doc)
        self.assertIn("Those remain separately protected gates.", doc)
        self.assertIn("586f9589c4c14a0bcb7a84bc0c579bfef94f6d7c", doc)

    def test_schema_and_authoritative_objects_remain_unchanged(self) -> None:
        self.assertEqual(git_blob_sha(COMMON), "ce0141ee7031f21fa2bd72b2faa3371aed3e622b")
        self.assertEqual(git_blob_sha(AUTISM), "b2d3809ecfcdb1d81c793a2401f0533a4b17ea98")
        self.assertEqual(git_blob_sha(NEURODIVERSITY), "5a38bc4250079412dd3f4da1d598dfcab984ca66")
        self.assertEqual(git_blob_sha(ADHD), "719f26a9af773cd1bcf670df4d12ed5f6bcf0a23")


if __name__ == "__main__":
    unittest.main()
