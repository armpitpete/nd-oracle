from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / "migration-candidates" / "autism-neurodiversity" / "relation-semantics-review.json"
PAIR = ROOT / "migration-candidates" / "autism-neurodiversity" / "structural-candidate.json"
AUTISM = ROOT / "objects" / "concepts" / "autism.json"
NEURODIVERSITY = ROOT / "objects" / "concepts" / "neurodiversity.json"
ADHD = ROOT / "objects" / "concepts" / "adhd.json"
COMMON = ROOT / "schema" / "common-v0.2.json"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def git_blob_sha(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


class NeurodiversityRelationSemanticsReviewTests(unittest.TestCase):
    def test_review_is_non_authoritative_and_bound_to_post_pr55_main(self) -> None:
        review = load(REVIEW)
        self.assertEqual("1.0", review["review_version"])
        self.assertEqual(
            "52ef8fad6da75b8fa772a3bfabfe9d7a89c6981b",
            review["prepared_against_main"],
        )
        self.assertFalse(review["authoritative"])
        self.assertFalse(review["authoritative_replacement"])
        self.assertTrue(all(value is False for value in review["boundaries"].values()))

    def test_review_does_not_mutate_current_candidate_schema_or_sources(self) -> None:
        self.assertEqual("c4ee90bbe829b85a4022e7d8ef48caa4692bd903", git_blob_sha(PAIR))
        self.assertEqual("ce0141ee7031f21fa2bd72b2faa3371aed3e622b", git_blob_sha(COMMON))
        self.assertEqual("b2d3809ecfcdb1d81c793a2401f0533a4b17ea98", git_blob_sha(AUTISM))
        self.assertEqual("5a38bc4250079412dd3f4da1d598dfcab984ca66", git_blob_sha(NEURODIVERSITY))
        self.assertEqual("719f26a9af773cd1bcf670df4d12ed5f6bcf0a23", git_blob_sha(ADHD))

    def test_legacy_type_and_note_are_both_preserved_in_review(self) -> None:
        review = load(REVIEW)
        anchors = review["repository_anchors"]
        self.assertEqual("narrower_than", anchors["autism"]["legacy_relation"]["type"])
        self.assertEqual(
            "Autism is commonly situated within neurodiversity discourse.",
            anchors["autism"]["legacy_relation"]["note"],
        )
        self.assertEqual(
            "broader_than",
            anchors["neurodiversity"]["legacy_relation_to_autism"]["type"],
        )
        self.assertEqual(
            "Autism is commonly discussed within the neurodiversity ecosystem.",
            anchors["neurodiversity"]["legacy_relation_to_autism"]["note"],
        )

    def test_option_test_prefers_legacy_retained_unmapped(self) -> None:
        review = load(REVIEW)
        options = {item["id"]: item for item in review["options"]}
        self.assertEqual(
            "rejected_as_lossless_migration",
            options["retain-v02-taxonomy-pair"]["status"],
        )
        self.assertEqual(
            "not_preferred_as_lossless_migration",
            options["map-to-associated-with"]["status"],
        )
        self.assertEqual(
            "not_recommended_now",
            options["add-situated-within-discourse-relation-type"]["status"],
        )
        self.assertEqual(
            "recommended_migration_disposition",
            options["legacy-retained-unmapped-no-direct-v02-edge"]["status"],
        )
        self.assertEqual(
            "plausible_separate_enrichment",
            options["new-described-by-neurodiversity-paradigm"]["status"],
        )

    def test_adhd_is_consistency_test_not_scope_expansion(self) -> None:
        review = load(REVIEW)
        check = review["adhd_consistency_test"]
        self.assertEqual("same_semantic_mismatch_observed", check["result"])
        self.assertFalse(check["migration_scope_expanded"])
        self.assertFalse(review["boundaries"]["adhd_scope_expansion_authorised"])

    def test_d5_history_is_preserved_while_mapping_assumption_is_reopened(self) -> None:
        review = load(REVIEW)
        finding = review["semantic_findings"]["d5_consequence"]
        self.assertIn("both sides", finding)
        self.assertIn("reopened", finding)
        self.assertFalse(review["boundaries"]["d5_record_rewritten"])

    def test_confidence_is_deferred_until_a_new_relation_is_accepted(self) -> None:
        review = load(REVIEW)
        self.assertIn(
            "Only after a new relation type/target is explicitly accepted",
            review["recommended_direction"]["confidence_next_step"],
        )
        self.assertFalse(review["boundaries"]["confidence_value_authorised"])
        self.assertFalse(review["boundaries"]["new_relation_enrichment_authorised"])

    def test_owner_decision_candidate_is_disposition_only(self) -> None:
        review = load(REVIEW)
        decision = review["decision_candidate"]
        self.assertEqual("nd-neurodiversity-legacy-structural-disposition", decision["id"])
        self.assertEqual("owner_decision_required", decision["status"])
        self.assertIn("legacy-retained-unmapped", decision["recommended_acceptance"])
        self.assertIn("ADHD remains a consistency test only", decision["recommended_acceptance"])
        self.assertIn("paired candidate mutation", decision["does_not_authorise"])
        self.assertIn("relation confidence", decision["does_not_authorise"])
        self.assertIn("authoritative v0.2 replacement", decision["does_not_authorise"])


if __name__ == "__main__":
    unittest.main()
