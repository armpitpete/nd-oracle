from __future__ import annotations

import copy
import json
from pathlib import Path
import unittest

from scripts import validate as nd_validate


ROOT = Path(__file__).resolve().parents[1]
CANDIDATE_DIR = ROOT / "migration-candidates" / "topic-expansion-batch-a" / "candidates"
AUTHORITATIVE_DIR = ROOT / "objects"
AUTHORITATIVE_CONCEPT_DIR = AUTHORITATIVE_DIR / "concepts"
EXPECTED_IDS = {
    "dyslexia",
    "developmental-coordination-disorder",
    "tourette-syndrome",
    "learning-disability",
    "developmental-language-disorder",
}
ACCEPTED_BLOBS = {
    "dyslexia": "6609a1a100919003b541e22559f51031ca202031",
    "developmental-coordination-disorder": "885dbc3a8293c6fa615d3fcacf80fe8dc23802e1",
    "tourette-syndrome": "f49e8adfe9a2fecc92239c024a4ee17523aa2574",
    "learning-disability": "a06995d02e7acf4022ff31069ea5bc7fc6da68fe",
    "developmental-language-disorder": "fc99e429d6464523b12e5aa8af804fe5523d20a1",
}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def accepted_semantic_projection(obj: dict) -> dict:
    projected = copy.deepcopy(obj)
    projected.pop("status", None)
    projected.pop("provenance", None)
    if projected.get("id") == "dyslexia":
        for relation in projected.get("relations", []):
            if relation.get("target_id") == "developmental-language-disorder":
                relation["note"] = relation["note"].replace(
                    "distinct candidate concepts", "distinct concepts"
                )
    return projected


class BatchACandidateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.candidate_paths = sorted(CANDIDATE_DIR.glob("*.json"))
        cls.candidates = {path: load_json(path) for path in cls.candidate_paths}
        cls.by_id = {obj["id"]: obj for obj in cls.candidates.values()}
        cls.authoritative_objects = [
            load_json(path)
            for path in sorted(AUTHORITATIVE_DIR.rglob("*.json"))
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

    def test_exact_batch_is_present(self) -> None:
        self.assertEqual(set(self.by_id), EXPECTED_IDS)
        self.assertEqual(len(self.candidate_paths), 5)

    def test_candidate_history_is_retained_after_promotion(self) -> None:
        self.assertTrue(EXPECTED_IDS.issubset(self.authoritative_ids))
        for path in self.candidate_paths:
            self.assertTrue(
                path.is_relative_to(CANDIDATE_DIR),
                f"candidate escaped candidate directory: {path}",
            )
        for object_id in EXPECTED_IDS:
            self.assertTrue((AUTHORITATIVE_CONCEPT_DIR / f"{object_id}.json").is_file())

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
                nd_validate.validate_v01_object(path, obj, self.all_ids, ROOT)
            )
        self.assertEqual(errors, [], "\n".join(errors))

    def test_candidates_remain_unreviewed_seeds(self) -> None:
        for path, obj in self.candidates.items():
            self.assertEqual(obj["status"], "seed", path.name)
            self.assertEqual(obj["provenance"]["review_state"], "unreviewed_seed", path.name)
            self.assertIsNone(obj["provenance"]["last_reviewed"], path.name)

    def test_promoted_objects_match_accepted_semantics(self) -> None:
        for object_id in EXPECTED_IDS:
            candidate = accepted_semantic_projection(self.by_id[object_id])
            authoritative = accepted_semantic_projection(self.authoritative_by_id[object_id])
            self.assertEqual(authoritative, candidate, object_id)

    def test_promoted_objects_record_review_and_exact_source_blob(self) -> None:
        for object_id, blob_sha in ACCEPTED_BLOBS.items():
            obj = self.authoritative_by_id[object_id]
            self.assertEqual(obj["status"], "reviewed", object_id)
            self.assertEqual(obj["provenance"]["review_state"], "editor_reviewed", object_id)
            self.assertEqual(obj["provenance"]["last_reviewed"], "2026-08-12", object_id)
            self.assertIn(blob_sha, obj["provenance"]["method"], object_id)

    def test_neurodiversity_is_not_asserted_as_taxonomic_parent(self) -> None:
        for collection in (self.by_id, self.authoritative_by_id):
            for object_id in EXPECTED_IDS:
                obj = collection[object_id]
                forbidden = [
                    relation
                    for relation in obj.get("relations", [])
                    if relation.get("target_id") == "neurodiversity"
                    and relation.get("type") in {"narrower_than", "broader_than"}
                ]
                self.assertEqual(
                    forbidden,
                    [],
                    f"{object_id} reintroduced rejected neurodiversity taxonomy: {forbidden}",
                )

    def test_ambiguous_near_synonyms_are_explained_not_encoded_as_aliases(self) -> None:
        for collection in (self.by_id, self.authoritative_by_id):
            dcd_aliases = {
                item.casefold()
                for item in collection["developmental-coordination-disorder"]["aliases"]
            }
            self.assertNotIn("dyspraxia", dcd_aliases)

            learning_disability_aliases = {
                item.casefold() for item in collection["learning-disability"]["aliases"]
            }
            self.assertNotIn("intellectual disability", learning_disability_aliases)
            self.assertNotIn("disorder of intellectual development", learning_disability_aliases)

            dyslexia_summary = collection["dyslexia"]["summary"].casefold()
            self.assertNotIn("learning disability", dyslexia_summary)


if __name__ == "__main__":
    unittest.main()
