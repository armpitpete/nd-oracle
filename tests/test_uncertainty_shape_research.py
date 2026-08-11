import hashlib
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESEARCH = ROOT / "migration-candidates" / "autism-neurodiversity" / "uncertainty-shape-research.json"
QUESTION_V02 = ROOT / "schema" / "types" / "question-v0.2.json"
V01_SCHEMA = ROOT / "schema" / "object-v0.1.json"
DOC = ROOT / "docs" / "migration-proofs" / "UNCERTAINTY_SHAPE_RESEARCH.md"

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


class UncertaintyShapeResearchTests(unittest.TestCase):
    def test_research_is_non_authoritative_and_anchored_to_d14_main(self) -> None:
        research = load(RESEARCH)
        self.assertEqual(research["research_version"], "1.0")
        self.assertEqual(
            research["prepared_against_main"],
            "a95a7772f6ca69d2c5b58cbcdcc6240110cc9ce8",
        )
        self.assertFalse(research["authoritative"])
        self.assertFalse(research["authoritative_replacement"])

    def test_all_five_authoritative_sources_remain_exact(self) -> None:
        research = load(RESEARCH)
        inventory = {item["object_id"]: item for item in research["authoritative_source_inventory"]}
        self.assertEqual(set(inventory), set(SOURCE_BLOBS))

        for object_id, (path, expected_blob) in SOURCE_BLOBS.items():
            self.assertEqual(git_blob_sha(path), expected_blob)
            self.assertEqual(inventory[object_id]["blob_sha"], expected_blob)

    def test_current_v01_uncertainties_all_have_three_routes_and_status(self) -> None:
        total = 0
        for path, _ in SOURCE_BLOBS.values():
            obj = load(path)
            self.assertEqual(obj["schema_version"], "0.1")
            self.assertEqual(len(obj["uncertainties"]), 2)
            for uncertainty in obj["uncertainties"]:
                total += 1
                self.assertEqual(len(uncertainty["what_would_reduce_it"]), 3)
                self.assertIsInstance(uncertainty["what_would_reduce_it"], list)
                self.assertEqual(uncertainty["status"], "open")
                self.assertTrue(uncertainty["question"].strip())
        self.assertEqual(total, 10)

    def test_schema_mismatch_is_preserved_as_historical_research_evidence(self) -> None:
        v01 = load(V01_SCHEMA)["$defs"]["uncertainty"]
        self.assertEqual(v01["properties"]["what_would_reduce_it"]["type"], "array")
        self.assertIn("status", v01["required"])
        self.assertIn("status", v01["properties"])

        research = load(RESEARCH)
        historical_v02 = research["schema_anchors"]["v02"]
        self.assertEqual(
            historical_v02["blob_sha"],
            "2c0fc2344fcafde88340b8a5882e0d171246ea02",
        )
        self.assertEqual(
            historical_v02["uncertainty_shape"]["required"],
            ["id", "statement", "why_it_matters", "reopening_or_reduction_condition"],
        )
        self.assertEqual(
            historical_v02["uncertainty_shape"]["reopening_or_reduction_condition_type"],
            "string",
        )
        self.assertFalse(historical_v02["uncertainty_shape"]["status_field_present"])

        mismatch = research["observed_mismatch"]
        self.assertEqual(mismatch["authoritative_uncertainty_count"], 10)
        self.assertTrue(mismatch["all_current_uncertainties_use_multiple_reduction_conditions"])
        self.assertTrue(mismatch["all_current_uncertainties_have_explicit_status"])
        self.assertFalse(mismatch["current_v02_embedded_uncertainty_can_preserve_list_structure_directly"])
        self.assertFalse(mismatch["current_v02_embedded_uncertainty_can_preserve_status_directly"])

    def test_question_schema_does_not_justify_automatic_promotion(self) -> None:
        question = load(QUESTION_V02)
        props = question["properties"]
        self.assertEqual(props["evidence_needed"]["type"], "array")
        self.assertEqual(props["reopening_conditions"]["type"], "array")
        self.assertIn("current_understanding", question["required"])

        options = {item["id"]: item for item in load(RESEARCH)["option_assessment"]}
        self.assertEqual(options["u3-promote-to-standalone-question"]["assessment"], "not_a_general_migration_rule")
        self.assertFalse(options["u3-promote-to-standalone-question"]["automatic_promotion_allowed"])
        self.assertTrue(options["u3-promote-to-standalone-question"]["requires_new_current_understanding"])

    def test_research_rejects_silent_lossy_shortcuts(self) -> None:
        research = load(RESEARCH)
        options = {item["id"]: item for item in research["option_assessment"]}
        self.assertEqual(options["u1-flatten-list-into-one-string"]["assessment"], "reject_as_default")
        self.assertEqual(
            options["u2-split-one-legacy-uncertainty-into-many"]["assessment"],
            "reject_without_separate_semantic_change",
        )
        self.assertEqual(options["u4-retain-legacy-unmapped"]["assessment"], "safe_interim_state_only")
        self.assertEqual(options["u5-native-embedded-uncertainty-repair"]["assessment"], "recommended_for_owner_review")

    def test_next_gate_is_historical_policy_gate_and_does_not_rewrite_research(self) -> None:
        research = load(RESEARCH)
        decision = research["decision_candidate"]
        self.assertEqual(decision["id"], "nd-embedded-uncertainty-lossless-representation")
        self.assertEqual(decision["status"], "owner_decision_required")

        boundaries = research["boundaries"]
        for key, value in boundaries.items():
            self.assertFalse(value, key)

        doc = DOC.read_text(encoding="utf-8")
        self.assertIn("nd-embedded-uncertainty-lossless-representation", doc)
        self.assertIn("would **not** authorise", doc)


if __name__ == "__main__":
    unittest.main()
