from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

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

    def test_commercial_source_requires_conflict_record(self) -> None:
        obj = copy.deepcopy(SEED)
        obj["sources"][0]["kind"] = "commercial"
        self.assert_invalid(obj)
        obj["sources"][0]["conflicts_of_interest"] = []
        self.assertEqual([], list(VALIDATOR.iter_errors(obj)))


if __name__ == "__main__":
    unittest.main()
