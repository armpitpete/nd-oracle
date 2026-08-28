from __future__ import annotations

import copy
import json
from pathlib import Path
import unittest

from scripts import validate as nd_validate


ROOT = Path(__file__).resolve().parents[1]
CANDIDATE_DIR = ROOT / "migration-candidates" / "foundation-review-batch-b" / "candidates"
AUTHORITATIVE_DIR = ROOT / "objects"
CONCEPT_DIR = AUTHORITATIVE_DIR / "concepts"
EXPECTED_IDS = {
    "neurodiversity",
    "autism",
    "adhd",
    "executive-function",
    "sensory-processing",
}
CANDIDATE_BLOBS = {
    "neurodiversity": "68a97d9f1c21c5e4e4d0c0b92eee9447a88668ad",
    "autism": "d3b58ae49a44dfb47d37622cdc3ca3fbe87a0923",
    "adhd": "c55adf286bb91341866c9a95857637065fc469a9",
    "executive-function": "f4a4e41e100303e40270fcb60e9ed7502e486920",
    "sensory-processing": "4483a4fd2f84446f11b5ac104975ad506ef93e56",
}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def semantic_projection(obj: dict) -> dict:
    projected = copy.deepcopy(obj)
    projected.pop("status", None)
    projected.pop("provenance", None)
    return projected


class BatchBFoundationReviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.candidate_paths = sorted(CANDIDATE_DIR.glob("*.json"))
        cls.candidates = {path: load_json(path) for path in cls.candidate_paths}
        cls.by_id = {obj["id"]: obj for obj in cls.candidates.values()}
        cls.authoritative_objects = [
            load_json(path) for path in sorted(AUTHORITATIVE_DIR.rglob("*.json"))
        ]
        cls.authoritative_by_id = {
            obj["id"]: obj for obj in cls.authoritative_objects if obj.get("id")
        }
        cls.authoritative_ids = set(cls.authoritative_by_id)
        cls.all_ids = cls.authoritative_ids | set(cls.by_id)
        validators, errors = nd_validate.load_schema_validators(ROOT)
        if errors:
            raise AssertionError("schema validator setup failed: " + "; ".join(errors))
        cls.v01_schema_validator = validators["0.1"]

    def test_exact_original_five_batch_is_present(self) -> None:
        self.assertEqual(set(self.by_id), EXPECTED_IDS)
        self.assertEqual(len(self.candidate_paths), 5)

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
            errors.extend(nd_validate.validate_v01_object(path, obj, self.all_ids, ROOT))
        self.assertEqual(errors, [], "\n".join(errors))

    def test_candidates_remain_preserved_unreviewed_seeds(self) -> None:
        for path, obj in self.candidates.items():
            self.assertEqual(obj["status"], "seed", path.name)
            self.assertEqual(obj["provenance"]["review_state"], "unreviewed_seed", path.name)
            self.assertIsNone(obj["provenance"]["last_reviewed"], path.name)

    def test_authoritative_objects_match_candidate_semantics_exactly(self) -> None:
        for object_id in EXPECTED_IDS:
            self.assertEqual(
                semantic_projection(self.authoritative_by_id[object_id]),
                semantic_projection(self.by_id[object_id]),
                object_id,
            )

    def test_authoritative_objects_record_review_and_exact_candidate_blob(self) -> None:
        for object_id, blob_sha in CANDIDATE_BLOBS.items():
            obj = self.authoritative_by_id[object_id]
            self.assertEqual(obj["status"], "reviewed", object_id)
            self.assertEqual(obj["provenance"]["review_state"], "editor_reviewed", object_id)
            self.assertEqual(obj["provenance"]["last_reviewed"], "2026-08-12", object_id)
            self.assertIn(blob_sha, obj["provenance"]["method"], object_id)

    def test_foundation_review_remains_valid_as_concept_corpus_grows(self) -> None:
        concept_paths = sorted(CONCEPT_DIR.glob("*.json"))
        self.assertGreaterEqual(len(concept_paths), 10)
        for path in concept_paths:
            obj = load_json(path)
            self.assertEqual(obj["status"], "reviewed", path.name)
            self.assertEqual(obj["provenance"]["review_state"], "editor_reviewed", path.name)
            self.assertIsNotNone(obj["provenance"]["last_reviewed"], path.name)

    def test_neurodiversity_taxonomy_is_absent(self) -> None:
        for collection in (self.by_id, self.authoritative_by_id):
            for object_id in EXPECTED_IDS:
                obj = collection[object_id]
                forbidden = [
                    relation
                    for relation in obj.get("relations", [])
                    if relation.get("type") in {"narrower_than", "broader_than"}
                    and (
                        object_id == "neurodiversity"
                        or relation.get("target_id") == "neurodiversity"
                    )
                ]
                self.assertEqual(forbidden, [], f"{object_id}: {forbidden}")

    def test_sensory_near_synonyms_are_not_exact_aliases(self) -> None:
        for collection in (self.by_id, self.authoritative_by_id):
            aliases = {item.casefold() for item in collection["sensory-processing"]["aliases"]}
            self.assertNotIn("sensory integration", aliases)
            self.assertNotIn("sensory modulation", aliases)

    def test_review_depth_is_not_seed_thinness(self) -> None:
        for object_id in EXPECTED_IDS:
            obj = self.authoritative_by_id[object_id]
            self.assertGreaterEqual(len(obj["claims"]), 3, object_id)
            self.assertGreaterEqual(len(obj["sources"]), 4, object_id)
            self.assertGreaterEqual(len(obj["uncertainties"]), 3, object_id)
            self.assertGreaterEqual(len(obj["perspectives"]), 2, object_id)


if __name__ == "__main__":
    unittest.main()
