from __future__ import annotations

import json
from pathlib import Path
import unittest

from scripts import validate as nd_validate


ROOT = Path(__file__).resolve().parents[1]
CANDIDATE_DIR = ROOT / "migration-candidates" / "topic-expansion-batch-a" / "candidates"
AUTHORITATIVE_DIR = ROOT / "objects"
EXPECTED_IDS = {
    "dyslexia",
    "developmental-coordination-disorder",
    "tourette-syndrome",
    "learning-disability",
    "developmental-language-disorder",
}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


class BatchACandidateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.candidate_paths = sorted(CANDIDATE_DIR.glob("*.json"))
        cls.candidates = {path: load_json(path) for path in cls.candidate_paths}
        cls.authoritative_objects = [
            load_json(path)
            for path in sorted(AUTHORITATIVE_DIR.rglob("*.json"))
        ]
        cls.authoritative_ids = {
            obj["id"] for obj in cls.authoritative_objects if obj.get("id")
        }
        cls.all_ids = cls.authoritative_ids | {
            obj["id"] for obj in cls.candidates.values()
        }

        validators, errors = nd_validate.load_schema_validators(ROOT)
        if errors:
            raise AssertionError("schema validator setup failed: " + "; ".join(errors))
        cls.v01_schema_validator = validators["0.1"]

    def test_exact_batch_is_present(self) -> None:
        self.assertEqual(
            {obj["id"] for obj in self.candidates.values()},
            EXPECTED_IDS,
        )
        self.assertEqual(len(self.candidate_paths), 5)

    def test_candidates_are_not_authoritative(self) -> None:
        self.assertTrue(EXPECTED_IDS.isdisjoint(self.authoritative_ids))
        for path in self.candidate_paths:
            self.assertTrue(
                path.is_relative_to(CANDIDATE_DIR),
                f"candidate escaped candidate directory: {path}",
            )

    def test_candidates_conform_to_v01_schema_and_semantics(self) -> None:
        errors: list[str] = []
        for path, obj in self.candidates.items():
            schema_errors = sorted(
                self.v01_schema_validator.iter_errors(obj),
                key=lambda error: list(error.absolute_path),
            )
            for error in schema_errors:
                location = ".".join(str(item) for item in error.absolute_path) or "<root>"
                errors.append(f"{path.name}:{location}: {error.message}")
            errors.extend(
                nd_validate.validate_v01_object(
                    path,
                    obj,
                    self.all_ids,
                    ROOT,
                )
            )
        self.assertEqual(errors, [], "\n".join(errors))

    def test_candidates_remain_unreviewed_seeds(self) -> None:
        for path, obj in self.candidates.items():
            self.assertEqual(obj["status"], "seed", path.name)
            self.assertEqual(obj["provenance"]["review_state"], "unreviewed_seed", path.name)
            self.assertIsNone(obj["provenance"]["last_reviewed"], path.name)

    def test_neurodiversity_is_not_asserted_as_taxonomic_parent(self) -> None:
        for path, obj in self.candidates.items():
            forbidden = [
                relation
                for relation in obj.get("relations", [])
                if relation.get("target_id") == "neurodiversity"
                and relation.get("type") in {"narrower_than", "broader_than"}
            ]
            self.assertEqual(
                forbidden,
                [],
                f"{path.name} reintroduced rejected neurodiversity taxonomy: {forbidden}",
            )


if __name__ == "__main__":
    unittest.main()
