from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.build_normalized_paired_migration_candidate import build_candidate
from scripts.validate import load_schema_validators, validate_v02_object
from scripts.validate_migration import git_blob_sha, validate_package

ROOT = Path(__file__).resolve().parents[1]
AUTISM = ROOT / "objects" / "concepts" / "autism.json"
NEURODIVERSITY = ROOT / "objects" / "concepts" / "neurodiversity.json"
AUTISM_BLOB = "b2d3809ecfcdb1d81c793a2401f0533a4b17ea98"
NEURODIVERSITY_BLOB = "5a38bc4250079412dd3f4da1d598dfcab984ca66"
S16 = "neurodiversity-source-singer-2016-kindle"
S17 = "neurodiversity-source-singer-2017-revised-print"


class D1D17StateNormalizationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.package = Path(self.tmp.name) / "autism-neurodiversity"
        build_candidate(self.package)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def load(self, relative: str):
        return json.loads((self.package / relative).read_text(encoding="utf-8"))

    def candidate_objects(self):
        paths = sorted((self.package / "candidate").rglob("*.json"))
        return paths, [json.loads(path.read_text(encoding="utf-8")) for path in paths]

    def test_normalized_package_is_contract_valid_and_has_only_two_open_blockers(self) -> None:
        self.assertEqual([], validate_package(self.package))
        manifest = self.load("manifest.json")
        self.assertEqual("enrichment_pending", manifest["package_status"])
        self.assertFalse(manifest["authoritative_replacement"])

        state = self.load("migration-state.json")
        self.assertEqual("paired_migration_candidate", state["candidate_kind"])
        self.assertEqual(
            {"singer-2016-full-date", "dependency-neurodiversity-adhd"},
            {item["id"] for item in state["open_blockers"]},
        )

        pending = {
            item["id"]
            for item in self.load("enrichment-ledger.json")["entries"]
            if item["review_state"] == "pending"
        }
        self.assertEqual({"enrich-neurodiversity-source-singer-2016-kindle-date"}, pending)

        unresolved_dependencies = {
            item["id"]
            for item in self.load("dependency-ledger.json")["entries"]
            if item["resolution_status"] != "resolved"
        }
        self.assertEqual({"dependency-neurodiversity-adhd"}, unresolved_dependencies)

    def test_normalization_removes_stale_owner_decision_required_dispositions(self) -> None:
        entries = self.load("preservation-ledger.json")["entries"]
        self.assertFalse(any(item["disposition"] == "owner_decision_required" for item in entries))

        adhd = next(
            item for item in entries
            if item["source_object_id"] == "neurodiversity"
            and item["unit"].startswith("relation:")
            and '"target_id":"adhd"' in item["unit"]
        )
        self.assertEqual("structural_dependency", adhd["disposition"])
        self.assertEqual("dependency-neurodiversity-adhd", adhd["dependency_ref"])

    def test_d16_uncertainty_shape_is_applied_losslessly(self) -> None:
        legacy = json.loads(AUTISM.read_text(encoding="utf-8"))
        candidate = self.load("candidate/concepts/autism.json")
        by_id = {
            item["id"]: item
            for claim in candidate["claims"]
            for item in claim["uncertainties"]
        }
        for old in legacy["uncertainties"]:
            new = by_id[old["id"]]
            self.assertEqual(old["question"], new["text"])
            self.assertEqual(old["why_it_matters"], new["why_it_matters"])
            self.assertEqual(old["what_would_reduce_it"], new["reopening_or_reduction_conditions"])
            self.assertEqual(old["status"], new["status"])

    def test_d17_emits_no_autism_neurodiversity_taxonomy_edge(self) -> None:
        autism = self.load("candidate/concepts/autism.json")
        neurodiversity = self.load("candidate/concepts/neurodiversity.json")
        self.assertEqual([], autism["relations"])
        self.assertEqual([], neurodiversity["relations"])

        entries = self.load("preservation-ledger.json")["entries"]
        pair = [
            item for item in entries
            if item["unit"].startswith("relation:")
            and (
                (item["source_object_id"] == "autism" and '"target_id":"neurodiversity"' in item["unit"])
                or (item["source_object_id"] == "neurodiversity" and '"target_id":"autism"' in item["unit"])
            )
        ]
        self.assertEqual(2, len(pair))
        self.assertTrue(all(item["disposition"] == "legacy_retained_unmapped" for item in pair))
        self.assertTrue(all(item["owner_decision_ref"] == "d17-neurodiversity-legacy-structural-disposition" for item in pair))

    def test_materialized_candidate_graph_is_v02_schema_and_semantic_valid(self) -> None:
        paths, objects = self.candidate_objects()
        self.assertEqual(9, len(objects))
        by_id = {obj["id"]: obj for obj in objects}
        self.assertEqual(len(objects), len(by_id))

        validators, schema_load_errors = load_schema_validators()
        self.assertEqual([], schema_load_errors)
        schema_validator = validators["0.2"]
        for path, obj in zip(paths, objects):
            schema_errors = list(schema_validator.iter_errors(obj))
            self.assertEqual([], schema_errors, f"{path}: {[error.message for error in schema_errors]}")
            semantic_errors = validate_v02_object(
                path,
                obj,
                by_id,
                ROOT,
                fixture_root=self.package / "candidate",
            )
            self.assertEqual([], semantic_errors, f"{path}: {semantic_errors}")

    def test_singer_2016_identity_is_preserved_but_not_materialized_without_date(self) -> None:
        pending = self.load("pending-evidence-identities.json")["entries"]
        self.assertEqual(1, len(pending))
        self.assertEqual(S16, pending[0]["id"])
        self.assertEqual("date", pending[0]["blocking_field"])
        bindings = pending[0]["accepted_identity"]["accepted_contribution_bindings"]
        self.assertEqual(2, len(bindings))
        self.assertEqual(
            {"d13-singer-edition-specific-contribution-bindings", "d14-singer-2016-claim2-binding-followup"},
            {item["decision_ref"] for item in bindings},
        )
        self.assertFalse((self.package / "candidate" / "evidence" / f"{S16}.json").exists())
        self.assertTrue((self.package / "candidate" / "evidence" / f"{S17}.json").exists())

    def test_authoritative_source_blobs_are_unchanged(self) -> None:
        self.assertEqual(AUTISM_BLOB, git_blob_sha(AUTISM))
        self.assertEqual(NEURODIVERSITY_BLOB, git_blob_sha(NEURODIVERSITY))


if __name__ == "__main__":
    unittest.main()
