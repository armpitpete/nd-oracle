from __future__ import annotations

import copy
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker
from scripts.validate import validate_repository

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((ROOT / "schema" / "object-v0.1.json").read_text(encoding="utf-8"))
VALIDATOR = Draft202012Validator(SCHEMA, format_checker=FormatChecker())
SEED = json.loads((ROOT / "objects" / "concepts" / "autism.json").read_text(encoding="utf-8"))


class SchemaValidationTests(unittest.TestCase):
    def assert_invalid(self, obj: object) -> None:
        self.assertTrue(list(VALIDATOR.iter_errors(obj)))

    def test_all_seed_objects_match_schema(self) -> None:
        for path in (ROOT / "objects").rglob("*.json"):
            with self.subTest(path=path.name):
                obj = json.loads(path.read_text(encoding="utf-8"))
                self.assertEqual([], list(VALIDATOR.iter_errors(obj)))

    def test_rejects_extra_property(self) -> None:
        obj = copy.deepcopy(SEED)
        obj["untracked_claim"] = "must not pass silently"
        self.assert_invalid(obj)

    def test_rejects_unimplemented_object_type(self) -> None:
        obj = copy.deepcopy(SEED)
        obj["type"] = "resource"
        self.assert_invalid(obj)

    def test_rejects_invalid_date(self) -> None:
        obj = copy.deepcopy(SEED)
        obj["provenance"]["created"] = "not-a-date"
        self.assert_invalid(obj)

    def test_rejects_empty_internal_identifier(self) -> None:
        obj = copy.deepcopy(SEED)
        obj["sources"][0]["id"] = ""
        self.assert_invalid(obj)

    def test_rejects_whitespace_only_description(self) -> None:
        obj = copy.deepcopy(SEED)
        obj["uncertainties"][0]["why_it_matters"] = "   "
        self.assert_invalid(obj)

    def test_commercial_source_requires_conflict_record(self) -> None:
        obj = copy.deepcopy(SEED)
        obj["sources"][0]["kind"] = "commercial"
        self.assert_invalid(obj)
        obj["sources"][0]["conflicts_of_interest"] = []
        self.assertEqual([], list(VALIDATOR.iter_errors(obj)))


class RepositoryValidationTests(unittest.TestCase):
    def validate_mutation(self, filename: str, mutate) -> list[str]:
        with tempfile.TemporaryDirectory() as directory:
            test_root = Path(directory)
            shutil.copytree(ROOT / "schema", test_root / "schema")
            shutil.copytree(ROOT / "objects", test_root / "objects")
            path = test_root / "objects" / "concepts" / filename
            obj = json.loads(path.read_text(encoding="utf-8"))
            mutate(obj)
            path.write_text(json.dumps(obj), encoding="utf-8")
            _, errors = validate_repository(test_root)
            return errors

    def test_complete_repository_passes(self) -> None:
        count, errors = validate_repository(ROOT)
        self.assertEqual(5, count)
        self.assertEqual([], errors)

    def test_rejects_nonreciprocal_claim_source_mapping(self) -> None:
        def mutate(obj: dict) -> None:
            obj["sources"][1]["supports"] = ["autism-claim-1"]

        errors = self.validate_mutation("autism.json", mutate)
        self.assertTrue(any("does not list claim autism-claim-2" in error for error in errors), errors)
        self.assertTrue(any("claim autism-claim-1 does not reference" in error for error in errors), errors)

    def test_rejects_nonreciprocal_perspective_source_mapping(self) -> None:
        def mutate(obj: dict) -> None:
            obj["sources"][0]["supports"].remove("autism-perspective-clinical")
            obj["sources"][1]["supports"].append("autism-perspective-clinical")

        errors = self.validate_mutation("autism.json", mutate)
        self.assertTrue(any("does not list perspective autism-perspective-clinical" in error for error in errors), errors)
        self.assertTrue(any("perspective autism-perspective-clinical does not reference" in error for error in errors), errors)

    def test_rejects_cross_category_internal_id_collision(self) -> None:
        def mutate(obj: dict) -> None:
            obj["perspectives"][0]["id"] = obj["claims"][0]["id"]
            obj["sources"][0]["supports"].remove("autism-perspective-clinical")

        errors = self.validate_mutation("autism.json", mutate)
        self.assertTrue(any("internal ids must be unique" in error for error in errors), errors)

    def test_rejects_dangling_relation(self) -> None:
        def mutate(obj: dict) -> None:
            obj["relations"][0]["target_id"] = "missing-concept"

        errors = self.validate_mutation("autism.json", mutate)
        self.assertTrue(any("relation references missing object missing-concept" in error for error in errors), errors)

    def test_rejects_filename_object_id_mismatch(self) -> None:
        def mutate(obj: dict) -> None:
            obj["id"] = "renamed-autism"

        errors = self.validate_mutation("autism.json", mutate)
        self.assertTrue(any("filename must match object id" in error for error in errors), errors)

    def test_rejects_duplicate_object_id(self) -> None:
        def mutate(obj: dict) -> None:
            obj["id"] = "autism"

        errors = self.validate_mutation("adhd.json", mutate)
        self.assertIn("duplicate object id across repository", errors)


if __name__ == "__main__":
    unittest.main()
