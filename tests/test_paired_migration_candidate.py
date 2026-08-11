from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.build_paired_migration_candidate import (
    AUTISM_SOURCE,
    BASE_COMMIT,
    NEURODIVERSITY_SOURCE,
    build_candidate,
)
from scripts.validate_migration import git_blob_sha, validate_package

ROOT = Path(__file__).resolve().parents[1]
AUTISM_BLOB = "b2d3809ecfcdb1d81c793a2401f0533a4b17ea98"
NEURODIVERSITY_BLOB = "5a38bc4250079412dd3f4da1d598dfcab984ca66"


class PairedMigrationCandidateTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.package = Path(self.tmp.name) / "autism-neurodiversity"
        build_candidate(self.package)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def load(self, relative: str) -> dict:
        return json.loads((self.package / relative).read_text(encoding="utf-8"))

    def save(self, relative: str, value: dict) -> None:
        (self.package / relative).write_text(
            json.dumps(value, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )

    def test_generated_pair_package_is_contract_valid_but_not_ready(self) -> None:
        self.assertEqual([], validate_package(self.package))
        manifest = self.load("manifest.json")
        self.assertEqual(BASE_COMMIT, manifest["source_repository_commit"])
        self.assertEqual("owner_decision_pending", manifest["package_status"])
        self.assertFalse(manifest["authoritative_replacement"])
        self.assertEqual(["autism", "neurodiversity"], manifest["candidate_object_ids"])
        self.assertEqual(
            {"autism", "neurodiversity"},
            {item["object_id"] for item in manifest["sources"]},
        )
        self.assertEqual(AUTISM_BLOB, git_blob_sha(AUTISM_SOURCE))
        self.assertEqual(NEURODIVERSITY_BLOB, git_blob_sha(NEURODIVERSITY_SOURCE))

    def test_structural_pair_preserves_reciprocity_without_inventing_confidence(self) -> None:
        candidate = self.load("candidate/structural-pair.json")
        self.assertEqual("partial_structural_pair", candidate["candidate_kind"])
        self.assertFalse(candidate["authoritative"])
        self.assertEqual(BASE_COMMIT, candidate["source_repository_commit"])
        self.assertEqual("d5-autism-neurodiversity-structural-closure", candidate["decision_ref"])
        self.assertEqual("d6-structural-relation-confidence", candidate["confidence_policy_ref"])

        objects = {item["id"]: item for item in candidate["objects"]}
        autism = objects["autism"]["structural_relation"]
        neurodiversity = objects["neurodiversity"]["structural_relation"]

        self.assertEqual("narrower_than", autism["type"])
        self.assertEqual({"type": "concept", "id": "neurodiversity"}, autism["target"])
        self.assertEqual("broader_than", neurodiversity["type"])
        self.assertEqual({"type": "concept", "id": "autism"}, neurodiversity["target"])
        self.assertEqual("explicit_enrichment_or_schema_policy_required", autism["confidence_status"])
        self.assertEqual("explicit_enrichment_or_schema_policy_required", neurodiversity["confidence_status"])
        self.assertEqual("d6-structural-relation-confidence", autism["confidence_policy_ref"])
        self.assertEqual("d6-structural-relation-confidence", neurodiversity["confidence_policy_ref"])
        self.assertNotIn("confidence", autism)
        self.assertNotIn("confidence", neurodiversity)
        self.assertEqual(
            "Autism is commonly situated within neurodiversity discourse.",
            autism["legacy_relation"]["note"],
        )
        self.assertEqual(
            "Autism is commonly discussed within the neurodiversity ecosystem.",
            neurodiversity["legacy_relation"]["note"],
        )
        self.assertFalse(candidate["authorisations"]["weaken_reciprocity_validator"])
        self.assertFalse(candidate["authorisations"]["authoritative_v02_replacement"])
        self.assertFalse(candidate["authorisations"]["infer_or_default_structural_confidence"])
        self.assertFalse(candidate["authorisations"]["use_not_applicable_as_confidence_shortcut"])

    def test_d6_is_accepted_but_confidence_value_remains_pending(self) -> None:
        decisions = self.load("owner-decisions.json")["decisions"]
        by_id = {item["id"]: item for item in decisions}
        d6 = by_id["d6-structural-relation-confidence"]
        self.assertEqual("accepted", d6["status"])
        self.assertFalse(d6["infer_or_default_confidence_authorised"])
        self.assertFalse(d6["use_not_applicable_as_validation_shortcut_authorised"])
        self.assertTrue(d6["evidence_backed_confidence_enrichment_allowed"])
        self.assertTrue(d6["separate_structural_confidence_schema_policy_allowed"])
        self.assertTrue(d6["current_candidate_confidence_must_remain_absent"])
        self.assertFalse(d6["schema_change_authorised"])
        self.assertFalse(d6["authoritative_v02_replacement_authorised"])

        enrichment = self.load("enrichment-ledger.json")["entries"]
        confidence = next(
            item for item in enrichment
            if item["id"] == "resolve-autism-neurodiversity-structural-confidence"
        )
        self.assertEqual("pending", confidence["review_state"])
        self.assertEqual("pending", confidence["value_origin"])
        self.assertIsNone(confidence["proposed_value"])
        self.assertEqual([], confidence["evidence_route"])
        self.assertTrue(any("not_applicable" in item for item in confidence["limitations"]))

    def test_pair_dependency_remains_open_and_adhd_edge_is_not_silently_dropped(self) -> None:
        dependencies = self.load("dependency-ledger.json")["entries"]
        by_id = {item["id"]: item for item in dependencies}
        self.assertEqual("unresolved", by_id["dependency-autism-neurodiversity"]["resolution_status"])
        self.assertEqual("unresolved", by_id["dependency-neurodiversity-adhd"]["resolution_status"])
        self.assertEqual("adhd", by_id["dependency-neurodiversity-adhd"]["dependent_object"])
        self.assertTrue(
            any("D6 forbids" in item for item in by_id["dependency-autism-neurodiversity"]["resolution_evidence"])
        )

        preservation = self.load("preservation-ledger.json")["entries"]
        nd_relations = [
            item
            for item in preservation
            if item["source_object_id"] == "neurodiversity" and item["unit"].startswith("relation:")
        ]
        self.assertEqual(2, len(nd_relations))
        refs = {item["dependency_ref"] for item in nd_relations}
        self.assertEqual(
            {"dependency-autism-neurodiversity", "dependency-neurodiversity-adhd"},
            refs,
        )

    def test_multi_source_preservation_units_are_source_scoped(self) -> None:
        ledger = self.load("preservation-ledger.json")
        self.assertTrue(ledger["entries"])
        self.assertTrue(all(item.get("source_object_id") in {"autism", "neurodiversity"} for item in ledger["entries"]))
        scoped = [(item["source_object_id"], item["unit"]) for item in ledger["entries"]]
        self.assertEqual(len(scoped), len(set(scoped)))

        ledger["entries"][0].pop("source_object_id")
        self.save("preservation-ledger.json", ledger)
        errors = validate_package(self.package)
        self.assertTrue(any("multi-source package requires source_object_id" in item for item in errors))

    def test_ready_state_is_blocked_by_unresolved_candidate_semantics(self) -> None:
        manifest = self.load("manifest.json")
        manifest["package_status"] = "ready_for_authoritative_review"
        self.save("manifest.json", manifest)
        errors = validate_package(self.package)
        self.assertTrue(any("pending enrichment" in item for item in errors))
        self.assertTrue(any("structural dependencies" in item for item in errors))
        self.assertTrue(any("unresolved preservation dispositions" in item for item in errors))


if __name__ == "__main__":
    unittest.main()
