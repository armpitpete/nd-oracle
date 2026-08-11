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
D17 = "d17-neurodiversity-legacy-structural-disposition"


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

    def test_structural_pair_preserves_legacy_reciprocity_without_emitting_v02_edge(self) -> None:
        candidate = self.load("candidate/structural-pair.json")
        self.assertEqual("partial_structural_pair", candidate["candidate_kind"])
        self.assertFalse(candidate["authoritative"])
        self.assertEqual(BASE_COMMIT, candidate["source_repository_commit"])
        self.assertEqual("d5-autism-neurodiversity-structural-closure", candidate["decision_ref"])
        self.assertEqual("d6-structural-relation-confidence", candidate["confidence_policy_ref"])
        self.assertEqual(D17, candidate["structural_disposition_decision_ref"])
        self.assertIn(D17, candidate["accepted_owner_decisions"])

        objects = {item["id"]: item for item in candidate["objects"]}
        autism = objects["autism"]["structural_relation"]
        neurodiversity = objects["neurodiversity"]["structural_relation"]

        for relation in (autism, neurodiversity):
            self.assertEqual("legacy_retained_unmapped", relation["disposition"])
            self.assertFalse(relation["emit_v02_semantic_edge"])
            self.assertEqual(D17, relation["decision_ref"])
            self.assertNotIn("type", relation)
            self.assertNotIn("target", relation)
            self.assertNotIn("confidence", relation)
            self.assertEqual("not_required_without_v02_edge", relation["confidence_status"])

        self.assertEqual(
            {
                "type": "narrower_than",
                "target_id": "neurodiversity",
                "note": "Autism is commonly situated within neurodiversity discourse.",
            },
            autism["legacy_relation"],
        )
        self.assertEqual(
            {
                "type": "broader_than",
                "target_id": "autism",
                "note": "Autism is commonly discussed within the neurodiversity ecosystem.",
            },
            neurodiversity["legacy_relation"],
        )
        self.assertFalse(candidate["authorisations"]["emit_v02_taxonomy_edge_from_legacy_pair"])
        self.assertFalse(candidate["authorisations"]["authoritative_v02_replacement"])
        self.assertFalse(candidate["authorisations"]["infer_or_default_structural_confidence"])
        self.assertFalse(candidate["authorisations"]["use_not_applicable_as_confidence_shortcut"])
        self.assertFalse(candidate["authorisations"]["new_semantic_graph_relation_authorised"])

    def test_d6_remains_historical_but_structural_confidence_enrichment_is_no_longer_generated(self) -> None:
        candidate = self.load("candidate/structural-pair.json")
        self.assertEqual("d6-structural-relation-confidence", candidate["confidence_policy_ref"])
        self.assertFalse(candidate["authorisations"]["paired_structural_confidence_required_for_legacy_pair"])

        enrichment = self.load("enrichment-ledger.json")["entries"]
        ids = {item["id"] for item in enrichment}
        self.assertNotIn("resolve-autism-neurodiversity-structural-confidence", ids)

        log = (self.package / "decision-log.md").read_text(encoding="utf-8")
        self.assertIn("D6 remains preserved historically", log)
        self.assertIn("no migrated edge exists to score", log)

    def test_d17_resolves_pair_dependency_but_adhd_dependency_remains_open(self) -> None:
        dependencies = self.load("dependency-ledger.json")["entries"]
        by_id = {item["id"]: item for item in dependencies}
        self.assertEqual("resolved", by_id["dependency-autism-neurodiversity"]["resolution_status"])
        self.assertTrue(
            any("D17 accepts" in item for item in by_id["dependency-autism-neurodiversity"]["resolution_evidence"])
        )
        self.assertEqual("unresolved", by_id["dependency-neurodiversity-adhd"]["resolution_status"])
        self.assertEqual("adhd", by_id["dependency-neurodiversity-adhd"]["dependent_object"])

        preservation = self.load("preservation-ledger.json")["entries"]
        autism_relation = next(
            item for item in preservation
            if item["source_object_id"] == "autism" and item["unit"].startswith("relation:")
        )
        self.assertEqual("legacy_retained_unmapped", autism_relation["disposition"])
        self.assertEqual(D17, autism_relation["owner_decision_ref"])

        nd_relations = [
            item
            for item in preservation
            if item["source_object_id"] == "neurodiversity" and item["unit"].startswith("relation:")
        ]
        self.assertEqual(2, len(nd_relations))
        nd_to_autism = next(item for item in nd_relations if item.get("legacy_value", {}).get("target_id") == "autism")
        self.assertEqual("legacy_retained_unmapped", nd_to_autism["disposition"])
        self.assertEqual(D17, nd_to_autism["owner_decision_ref"])
        nd_to_adhd = next(item for item in nd_relations if "adhd" in item["unit"])
        self.assertEqual("structural_dependency", nd_to_adhd["disposition"])
        self.assertEqual("dependency-neurodiversity-adhd", nd_to_adhd["dependency_ref"])

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

    def test_ready_state_remains_blocked_by_other_unresolved_migration_work(self) -> None:
        manifest = self.load("manifest.json")
        manifest["package_status"] = "ready_for_authoritative_review"
        self.save("manifest.json", manifest)
        errors = validate_package(self.package)
        self.assertTrue(any("pending enrichment" in item for item in errors))
        self.assertTrue(any("structural dependencies" in item for item in errors))
        self.assertTrue(any("unresolved preservation dispositions" in item for item in errors))


if __name__ == "__main__":
    unittest.main()
