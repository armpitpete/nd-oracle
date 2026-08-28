from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path

from scripts.validate import (
    load_schema_validators,
    missing_v01_preservation_units,
    validate_repository,
    v01_preservation_inventory,
)

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures" / "v0.2"


class V02ValidationTests(unittest.TestCase):
    def _load_fixture(self, relative: str) -> dict:
        return json.loads((FIXTURES / relative).read_text(encoding="utf-8"))

    def _validate_mutation(self, relative: str, mutate) -> list[str]:
        with tempfile.TemporaryDirectory() as directory:
            test_root = Path(directory)
            shutil.copytree(ROOT / "schema", test_root / "schema")
            shutil.copytree(ROOT / "objects", test_root / "objects")
            fixture_root = test_root / "tests" / "fixtures" / "v0.2"
            shutil.copytree(FIXTURES, fixture_root)
            path = fixture_root / relative
            obj = json.loads(path.read_text(encoding="utf-8"))
            mutate(obj)
            path.write_text(json.dumps(obj), encoding="utf-8")
            _, errors = validate_repository(test_root, fixture_root)
            return errors

    def test_fixture_graph_passes_without_changing_authoritative_count(self) -> None:
        count, errors = validate_repository(ROOT, FIXTURES)
        self.assertEqual(25, count)
        self.assertEqual([], errors)

    def test_dispatcher_accepts_all_six_v02_types(self) -> None:
        validators, errors = load_schema_validators(ROOT)
        self.assertEqual([], errors)
        validator = validators["0.2"]
        seen = set()
        for path in FIXTURES.rglob("*.json"):
            obj = json.loads(path.read_text(encoding="utf-8"))
            seen.add(obj["type"])
            with self.subTest(path=path.name):
                self.assertEqual([], list(validator.iter_errors(obj)))
        self.assertEqual(
            {"concept", "evidence", "question", "resource", "perspective", "experience"},
            seen,
        )

    def test_fixture_exercises_required_semantic_distinctions(self) -> None:
        evidence = self._load_fixture("evidence/fixture-evidence.json")
        concept = self._load_fixture("concepts/fixture-concept.json")
        question = self._load_fixture("questions/fixture-question.json")
        resource = self._load_fixture("resources/fixture-resource.json")
        roles = {item["role"] for item in evidence["contributions"]}
        self.assertIn("supportive", roles)
        self.assertIn("inconclusive", roles)
        self.assertEqual("doi", evidence["locator"]["type"])
        claim = next(item for item in concept["claims"] if item["id"] == "fixture-claim-two")
        self.assertEqual([], claim["question_ids"])
        self.assertEqual("fixture-no-question", claim["uncertainties"][0]["id"])
        self.assertGreaterEqual(len(question["related_objects"]), 2)
        self.assertEqual(2, len(resource["experience_ids"]))
        self.assertEqual("url", resource["locators"][0]["type"])

    def test_rejects_unknown_schema_version(self) -> None:
        errors = self._validate_mutation(
            "resources/fixture-resource.json",
            lambda obj: obj.__setitem__("schema_version", "9.9"),
        )
        self.assertTrue(any("unsupported schema_version" in error for error in errors), errors)

    def test_rejects_unknown_object_type(self) -> None:
        errors = self._validate_mutation(
            "resources/fixture-resource.json",
            lambda obj: obj.__setitem__("type", "mystery"),
        )
        self.assertTrue(errors)

    def test_rejects_duplicate_global_object_id(self) -> None:
        errors = self._validate_mutation(
            "resources/fixture-resource.json",
            lambda obj: obj.__setitem__("id", "fixture-concept"),
        )
        self.assertTrue(any("duplicate object id" in error for error in errors), errors)

    def test_rejects_filename_object_id_mismatch(self) -> None:
        errors = self._validate_mutation(
            "resources/fixture-resource.json",
            lambda obj: obj.__setitem__("id", "renamed-fixture-resource"),
        )
        self.assertTrue(any("filename must match object id" in error for error in errors), errors)

    def test_rejects_wrong_type_directory(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            test_root = Path(directory)
            shutil.copytree(ROOT / "schema", test_root / "schema")
            shutil.copytree(ROOT / "objects", test_root / "objects")
            fixture_root = test_root / "tests" / "fixtures" / "v0.2"
            shutil.copytree(FIXTURES, fixture_root)
            source = fixture_root / "perspectives" / "fixture-perspective.json"
            source.replace(fixture_root / "resources" / source.name)
            _, errors = validate_repository(test_root, fixture_root)
            self.assertTrue(any("must be stored under perspectives/" in error for error in errors), errors)

    def test_rejects_claims_on_non_claim_owner(self) -> None:
        errors = self._validate_mutation(
            "perspectives/fixture-perspective.json",
            lambda obj: obj.__setitem__("claims", []),
        )
        self.assertTrue(errors)

    def test_rejects_duplicate_local_claim_id(self) -> None:
        def mutate(obj: dict) -> None:
            obj["claims"][1]["id"] = obj["claims"][0]["id"]

        errors = self._validate_mutation("concepts/fixture-concept.json", mutate)
        self.assertTrue(any("duplicate local id" in error for error in errors), errors)

    def test_rejects_malformed_claim_reference(self) -> None:
        def mutate(obj: dict) -> None:
            obj["contributions"][0]["claim_ref"] = "not a claim ref"

        self.assertTrue(self._validate_mutation("evidence/fixture-evidence.json", mutate))

    def test_rejects_missing_claim_owner(self) -> None:
        def mutate(obj: dict) -> None:
            obj["contributions"][0]["claim_ref"] = "missing-owner#fixture-claim-one"

        errors = self._validate_mutation("evidence/fixture-evidence.json", mutate)
        self.assertTrue(any("missing claim owner" in error for error in errors), errors)

    def test_rejects_missing_claim(self) -> None:
        def mutate(obj: dict) -> None:
            obj["contributions"][0]["claim_ref"] = "fixture-concept#missing-claim"

        errors = self._validate_mutation("evidence/fixture-evidence.json", mutate)
        self.assertTrue(any("references missing claim" in error for error in errors), errors)

    def test_rejects_claim_reference_to_non_claim_owner(self) -> None:
        def mutate(obj: dict) -> None:
            obj["contributions"][0]["claim_ref"] = "fixture-question#pretend-claim"

        errors = self._validate_mutation("evidence/fixture-evidence.json", mutate)
        self.assertTrue(any("not a v0.2 claim owner" in error for error in errors), errors)

    def test_rejects_missing_evidence_referenced_by_claim(self) -> None:
        def mutate(obj: dict) -> None:
            obj["claims"][0]["evidence_ids"] = ["missing-evidence"]

        errors = self._validate_mutation("concepts/fixture-concept.json", mutate)
        self.assertTrue(any("missing evidence" in error for error in errors), errors)

    def test_rejects_invalid_evidence_role_and_blank_contribution_fields(self) -> None:
        for field, value in (
            ("role", "proves"),
            ("finding", "   "),
            ("population_or_context", " "),
            ("methodology", ""),
        ):
            def mutate(obj: dict, field=field, value=value) -> None:
                obj["contributions"][0][field] = value
            with self.subTest(field=field):
                self.assertTrue(self._validate_mutation("evidence/fixture-evidence.json", mutate))

    def test_rejects_missing_question_reference(self) -> None:
        def mutate(obj: dict) -> None:
            obj["claims"][0]["question_ids"] = ["missing-question"]

        errors = self._validate_mutation("concepts/fixture-concept.json", mutate)
        self.assertTrue(any("missing question" in error for error in errors), errors)

    def test_rejects_question_shape_coerced_into_local_uncertainty(self) -> None:
        def mutate(obj: dict) -> None:
            obj["claims"][0]["uncertainties"][0] = {
                "id": "coerced-question",
                "question": "This should not validate as a local uncertainty.",
                "why_it_matters": "The categories must remain distinct.",
                "evidence_needed": ["More synthetic evidence."],
            }

        self.assertTrue(self._validate_mutation("concepts/fixture-concept.json", mutate))

    def test_rejects_typed_reference_to_wrong_target_type(self) -> None:
        def mutate(obj: dict) -> None:
            obj["related_objects"][0]["type"] = "evidence"

        errors = self._validate_mutation("resources/fixture-resource.json", mutate)
        self.assertTrue(any("expects evidence fixture-concept but found concept" in error for error in errors), errors)

    def test_rejects_nonreciprocal_structural_relation(self) -> None:
        errors = self._validate_mutation(
            "concepts/fixture-broader-concept.json",
            lambda obj: obj.__setitem__("relations", []),
        )
        self.assertTrue(any("requires reciprocal broader_than" in error for error in errors), errors)

    def test_rejects_dangling_relation_target(self) -> None:
        def mutate(obj: dict) -> None:
            obj["relations"][0]["target"]["id"] = "missing-concept"

        errors = self._validate_mutation("concepts/fixture-concept.json", mutate)
        self.assertTrue(any("references missing object missing-concept" in error for error in errors), errors)

    def test_rejects_invalid_date_locator_and_commercial_conflict_state(self) -> None:
        mutations = [
            lambda obj: obj.__setitem__("date", "not-a-date"),
            lambda obj: obj.__setitem__("locator", {"type": "url", "value": "http://example.invalid"}),
            lambda obj: (obj.__setitem__("source_kind", "commercial"), obj.pop("conflicts_of_interest", None)),
        ]
        for mutate in mutations:
            with self.subTest(mutate=mutate):
                self.assertTrue(self._validate_mutation("evidence/fixture-evidence.json", mutate))

    def test_migration_loss_inventory_detects_unaccounted_v01_semantics(self) -> None:
        source = json.loads(
            (ROOT / "objects" / "concepts" / "autism.json").read_text(encoding="utf-8")
        )
        preserved = v01_preservation_inventory(source)
        removed = {
            next(unit for unit in preserved if unit.startswith("claim:")),
            next(unit for unit in preserved if unit.startswith("claim-source-route:")),
            next(unit for unit in preserved if unit.startswith("claim-uncertainty-route:")),
            next(unit for unit in preserved if unit.startswith("perspective:")),
            next(unit for unit in preserved if unit.startswith("scope-excludes:")),
            next(unit for unit in preserved if unit.startswith("provenance:")),
        }
        missing = missing_v01_preservation_units(source, preserved - removed)
        self.assertEqual(removed, set(missing))


if __name__ == "__main__":
    unittest.main()
