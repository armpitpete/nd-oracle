import hashlib
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DECISIONS = ROOT / "migration-candidates" / "autism-neurodiversity" / "owner-decisions.json"
PAIR = ROOT / "migration-candidates" / "autism-neurodiversity" / "structural-candidate.json"
CANDIDATE = ROOT / "migration-candidates" / "autism-neurodiversity" / "embedded-uncertainty-schema-implementation-candidate.json"
COMMON = ROOT / "schema" / "common-v0.2.json"
DOC = ROOT / "docs" / "migration-proofs" / "D16_EMBEDDED_UNCERTAINTY_SCHEMA_IMPLEMENTATION.md"
AUTISM = ROOT / "objects" / "concepts" / "autism.json"
NEURODIVERSITY = ROOT / "objects" / "concepts" / "neurodiversity.json"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def git_blob_sha(path: Path) -> str:
    data = path.read_bytes()
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


class D16EmbeddedUncertaintySchemaImplementationTests(unittest.TestCase):
    def test_d16_records_exact_acceptance_against_post_d15_main(self) -> None:
        decisions = {item["id"]: item for item in load(DECISIONS)["decisions"]}
        d16 = decisions["d16-embedded-uncertainty-schema-implementation"]
        self.assertEqual(d16["status"], "accepted")
        self.assertEqual(d16["accepted_on"], "2026-08-11")
        self.assertEqual(
            d16["accepted_against_main"],
            "1bc63e07c7da026d2a2cba36bb05eb72980e7f19",
        )
        self.assertEqual(
            d16["supersedes_implementation_candidate"],
            {
                "path": "migration-candidates/autism-neurodiversity/embedded-uncertainty-schema-implementation-candidate.json",
                "id": "nd-embedded-uncertainty-schema-implementation",
            },
        )

    def test_d16_accepts_exact_shape_without_semantic_shortcuts(self) -> None:
        decisions = {item["id"]: item for item in load(DECISIONS)["decisions"]}
        d16 = decisions["d16-embedded-uncertainty-schema-implementation"]
        design = d16["accepted_exact_design"]
        self.assertEqual(design["text_field"], "text")
        self.assertTrue(design["text_is_neutral"])
        self.assertEqual(
            design["reopening_or_reduction_conditions_field"],
            "reopening_or_reduction_conditions",
        )
        self.assertTrue(design["conditions_are_canonical_plural_array"])
        self.assertTrue(design["conditions_preserve_order"])
        self.assertTrue(design["conditions_preserve_duplicates"])
        self.assertEqual(
            design["status_vocabulary"],
            ["open", "partially_resolved", "none_identified"],
        )
        self.assertEqual(design["status_mapping_policy"], "identity_only")
        self.assertFalse(design["compatibility_union"])
        self.assertTrue(d16["schema_change_authorised"])
        self.assertTrue(d16["validator_change_authorised"])
        for field in (
            "authoritative_v01_mutation_authorised",
            "authoritative_v02_replacement_authorised",
            "automatic_question_promotion_authorised",
            "uncertainty_split_authorised",
            "list_flattening_authorised",
            "status_remapping_authorised",
            "new_uncertainty_status_semantics_authorised",
            "publication_or_deployment_authorised",
        ):
            self.assertFalse(d16[field], field)

    def test_candidate_and_pair_are_bound_to_d16(self) -> None:
        candidate = load(CANDIDATE)
        self.assertEqual(
            candidate["accepted_owner_decision"],
            "d16-embedded-uncertainty-schema-implementation",
        )
        self.assertEqual(candidate["decision_candidate"]["status"], "accepted")

        pair = load(PAIR)
        self.assertIn(
            "d16-embedded-uncertainty-schema-implementation",
            pair["accepted_owner_decisions"],
        )
        blockers = {item["id"]: item for item in pair["blockers"]}
        for blocker_id in ("autism-uncertainty-shape", "neurodiversity-uncertainty-shape"):
            blocker = blockers[blocker_id]
            self.assertEqual(blocker["kind"], "accepted_schema_implementation")
            self.assertEqual(
                blocker["decision_ref"],
                "d16-embedded-uncertainty-schema-implementation",
            )
        auth = pair["authorisations"]
        self.assertTrue(auth["embedded_uncertainty_schema_implementation_accepted"])
        self.assertTrue(auth["embedded_uncertainty_schema_change_authorised"])
        self.assertTrue(auth["embedded_uncertainty_validator_change_authorised"])
        self.assertFalse(auth["authoritative_v02_replacement"])
        self.assertFalse(auth["automatic_question_promotion_authorised"])
        self.assertFalse(auth["uncertainty_split_authorised"])
        self.assertFalse(auth["uncertainty_list_flattening_authorised"])
        self.assertFalse(auth["uncertainty_status_remapping_authorised"])

    def test_schema_is_exact_d16_shape(self) -> None:
        common = load(COMMON)
        uncertainty = common["$defs"]["uncertainty"]
        self.assertEqual(
            uncertainty["required"],
            ["id", "text", "why_it_matters", "reopening_or_reduction_conditions", "status"],
        )
        conditions = uncertainty["properties"]["reopening_or_reduction_conditions"]
        self.assertEqual(conditions["type"], "array")
        self.assertEqual(conditions["minItems"], 1)
        self.assertNotIn("uniqueItems", conditions)
        self.assertEqual(
            common["$defs"]["uncertaintyStatus"]["enum"],
            ["open", "partially_resolved", "none_identified"],
        )
        self.assertNotIn("statement", uncertainty["properties"])
        self.assertNotIn("reopening_or_reduction_condition", uncertainty["properties"])

    def test_authoritative_pair_sources_remain_unchanged(self) -> None:
        self.assertEqual(git_blob_sha(AUTISM), "b2d3809ecfcdb1d81c793a2401f0533a4b17ea98")
        self.assertEqual(git_blob_sha(NEURODIVERSITY), "5a38bc4250079412dd3f4da1d598dfcab984ca66")
        doc = DOC.read_text(encoding="utf-8")
        self.assertIn("owner exact implementation accepted", doc)
        self.assertIn("authoritative migration not authorised", doc)
        self.assertIn("accepted_schema_implementation", doc)


if __name__ == "__main__":
    unittest.main()
