import hashlib
import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
COMMON = ROOT / "schema" / "common-v0.2.json"
CONTRACT = ROOT / "schema" / "schema-v0.2.md"
CANDIDATE = ROOT / "migration-candidates" / "autism-neurodiversity" / "embedded-uncertainty-schema-implementation-candidate.json"
RESEARCH = ROOT / "migration-candidates" / "autism-neurodiversity" / "uncertainty-shape-research.json"
D15_DOC = ROOT / "docs" / "migration-proofs" / "D15_EMBEDDED_UNCERTAINTY_LOSSLESS_POLICY.md"
FIXTURE_CONCEPT = ROOT / "tests" / "fixtures" / "v0.2" / "concepts" / "fixture-concept.json"

SOURCE_BLOBS = {
    "autism": (ROOT / "objects" / "concepts" / "autism.json", "b2d3809ecfcdb1d81c793a2401f0533a4b17ea98"),
    "neurodiversity": (ROOT / "objects" / "concepts" / "neurodiversity.json", "5a38bc4250079412dd3f4da1d598dfcab984ca66"),
    "adhd": (ROOT / "objects" / "concepts" / "adhd.json", "719f26a9af773cd1bcf670df4d12ed5f6bcf0a23"),
    "executive-function": (ROOT / "objects" / "concepts" / "executive-function.json", "f67e1a73e89245f9e6c6c2a34d4acc47169b8273"),
    "sensory-processing": (ROOT / "objects" / "concepts" / "sensory-processing.json", "7626d61a2844aae88ce6811760dfe97b5baa94bc"),
}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def git_blob_sha(path: Path) -> str:
    data = path.read_bytes()
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def uncertainty_validator() -> Draft202012Validator:
    common = load(COMMON)
    schema = {
        "$schema": common["$schema"],
        "$defs": common["$defs"],
        "$ref": "#/$defs/uncertainty",
    }
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema)


def map_v01_uncertainty(legacy: dict) -> dict:
    return {
        "id": legacy["id"],
        "text": legacy["question"],
        "why_it_matters": legacy["why_it_matters"],
        "reopening_or_reduction_conditions": list(legacy["what_would_reduce_it"]),
        "status": legacy["status"],
    }


class EmbeddedUncertaintySchemaCandidateTests(unittest.TestCase):
    def test_candidate_is_bounded_and_requires_owner_decision(self) -> None:
        candidate = load(CANDIDATE)
        self.assertEqual(candidate["candidate_version"], "1.0")
        self.assertEqual(
            candidate["prepared_against_main"],
            "1bc63e07c7da026d2a2cba36bb05eb72980e7f19",
        )
        self.assertFalse(candidate["authoritative"])
        self.assertFalse(candidate["authoritative_replacement"])
        self.assertEqual(
            candidate["governing_owner_decision"],
            "d15-embedded-uncertainty-lossless-representation",
        )
        self.assertEqual(
            candidate["decision_candidate"]["id"],
            "nd-embedded-uncertainty-schema-implementation",
        )
        self.assertEqual(candidate["decision_candidate"]["status"], "owner_decision_required")
        self.assertTrue(all(value is False for value in candidate["boundaries"].values()))

    def test_exact_schema_shape_matches_candidate(self) -> None:
        common = load(COMMON)
        uncertainty = common["$defs"]["uncertainty"]
        self.assertEqual(
            uncertainty["required"],
            ["id", "text", "why_it_matters", "reopening_or_reduction_conditions", "status"],
        )
        self.assertEqual(
            common["$defs"]["uncertaintyStatus"]["enum"],
            ["open", "partially_resolved", "none_identified"],
        )
        conditions = uncertainty["properties"]["reopening_or_reduction_conditions"]
        self.assertEqual(conditions["type"], "array")
        self.assertEqual(conditions["minItems"], 1)
        self.assertNotIn("uniqueItems", conditions)
        self.assertEqual(conditions["items"]["$ref"], "#/$defs/nonBlankString")
        self.assertNotIn("statement", uncertainty["properties"])
        self.assertNotIn("reopening_or_reduction_condition", uncertainty["properties"])
        self.assertEqual(git_blob_sha(COMMON), "ce0141ee7031f21fa2bd72b2faa3371aed3e622b")

    def test_all_current_authoritative_v01_uncertainties_map_verbatim_and_validate(self) -> None:
        validator = uncertainty_validator()
        total = 0
        for path, expected_blob in SOURCE_BLOBS.values():
            self.assertEqual(git_blob_sha(path), expected_blob)
            obj = load(path)
            for legacy in obj["uncertainties"]:
                total += 1
                mapped = map_v01_uncertainty(legacy)
                self.assertEqual([], list(validator.iter_errors(mapped)))
                self.assertEqual(mapped["id"], legacy["id"])
                self.assertEqual(mapped["text"], legacy["question"])
                self.assertEqual(mapped["why_it_matters"], legacy["why_it_matters"])
                self.assertEqual(
                    mapped["reopening_or_reduction_conditions"],
                    legacy["what_would_reduce_it"],
                )
                self.assertEqual(mapped["status"], legacy["status"])
        self.assertEqual(total, 10)

    def test_schema_valid_v01_duplicate_routes_can_be_preserved_without_normalisation(self) -> None:
        legacy = {
            "id": "duplicate-route-test",
            "question": "Could two recorded routes be textually identical?",
            "why_it_matters": "Lossless migration must not silently deduplicate source state.",
            "what_would_reduce_it": ["Same recorded route.", "Same recorded route."],
            "status": "partially_resolved",
        }
        mapped = map_v01_uncertainty(legacy)
        self.assertEqual([], list(uncertainty_validator().iter_errors(mapped)))
        self.assertEqual(
            mapped["reopening_or_reduction_conditions"],
            ["Same recorded route.", "Same recorded route."],
        )

    def test_all_legacy_status_values_validate_by_identity_without_remapping(self) -> None:
        validator = uncertainty_validator()
        for status in ("open", "partially_resolved", "none_identified"):
            record = {
                "id": f"status-{status.replace('_', '-')}",
                "text": "Could this lifecycle state be preserved verbatim?",
                "why_it_matters": "The migration must not invent a replacement status.",
                "reopening_or_reduction_conditions": ["Preserve the source state."],
                "status": status,
            }
            with self.subTest(status=status):
                self.assertEqual([], list(validator.iter_errors(record)))

        invalid = {
            "id": "status-invented",
            "text": "An invented status should fail.",
            "why_it_matters": "New semantics require separate review.",
            "reopening_or_reduction_conditions": ["Review a new lifecycle policy."],
            "status": "resolved",
        }
        self.assertTrue(list(validator.iter_errors(invalid)))

    def test_superseded_single_string_v02_shape_fails_closed(self) -> None:
        validator = uncertainty_validator()
        old_shape = {
            "id": "old-shape",
            "statement": "The old shape should no longer validate.",
            "why_it_matters": "Two accepted shapes would create ambiguity.",
            "reopening_or_reduction_condition": "Use the canonical plural shape.",
        }
        self.assertTrue(list(validator.iter_errors(old_shape)))

        single_string = {
            "id": "single-string",
            "text": "The plural field must remain an array.",
            "why_it_matters": "Flattening would lose list structure.",
            "reopening_or_reduction_conditions": "One string is not the accepted shape.",
            "status": "open",
        }
        self.assertTrue(list(validator.iter_errors(single_string)))

    def test_fixture_proves_interrogative_text_and_distinct_plural_routes(self) -> None:
        concept = load(FIXTURE_CONCEPT)
        uncertainty = concept["claims"][0]["uncertainties"][0]
        self.assertTrue(uncertainty["text"].endswith("?"))
        self.assertEqual(len(uncertainty["reopening_or_reduction_conditions"]), 2)
        self.assertNotEqual(
            uncertainty["reopening_or_reduction_conditions"][0],
            uncertainty["reopening_or_reduction_conditions"][1],
        )
        self.assertEqual(uncertainty["status"], "open")

    def test_historical_research_and_d15_proof_are_not_rewritten(self) -> None:
        self.assertEqual(git_blob_sha(RESEARCH), "a323947f35524da4dec6f8b7a08ab4105d9cd40f")
        self.assertEqual(git_blob_sha(D15_DOC), "db22aae5a4473810d7a49d19a1be53560bef06e6")
        research = load(RESEARCH)
        self.assertEqual(
            research["schema_anchors"]["v02"]["blob_sha"],
            "2c0fc2344fcafde88340b8a5882e0d171246ea02",
        )

    def test_schema_contract_states_lossless_and_no_automatic_question_promotion(self) -> None:
        contract = CONTRACT.read_text(encoding="utf-8")
        self.assertIn("neutral non-blank `text`", contract)
        self.assertIn("`reopening_or_reduction_conditions`", contract)
        self.assertIn("does not require uniqueness", contract)
        self.assertIn("must not promote them automatically", contract)


if __name__ == "__main__":
    unittest.main()
