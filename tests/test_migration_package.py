from __future__ import annotations

import copy
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from scripts.validate_migration import git_blob_sha, validate_package

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests" / "fixtures" / "migration" / "autism"
SOURCE = ROOT / "objects" / "concepts" / "autism.json"
AUTISM_V01_BLOB = "b2d3809ecfcdb1d81c793a2401f0533a4b17ea98"


class AutismMigrationPackageTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.package = Path(self.tmp.name) / "autism"
        shutil.copytree(FIXTURE, self.package)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def load(self, name: str) -> dict:
        return json.loads((self.package / name).read_text(encoding="utf-8"))

    def save(self, name: str, value: dict) -> None:
        (self.package / name).write_text(
            json.dumps(value, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )

    def test_fixture_is_valid_but_not_ready(self) -> None:
        before = git_blob_sha(SOURCE)
        self.assertEqual([], validate_package(self.package))
        self.assertEqual(before, git_blob_sha(SOURCE))
        manifest = self.load("manifest.json")
        self.assertEqual("owner_decision_pending", manifest["package_status"])
        self.assertFalse(manifest["authoritative_replacement"])

    def test_enrichment_pass_is_evidence_backed_with_perspective_decisions_pending(self) -> None:
        ledger = self.load("enrichment-ledger.json")
        verified = [item for item in ledger["entries"] if item["review_state"] == "verified"]
        pending = [item for item in ledger["entries"] if item["review_state"] == "pending"]
        self.assertEqual(19, len(verified))
        self.assertEqual(3, len(pending))
        self.assertTrue(all(item["evidence_route"] for item in verified))
        self.assertTrue(all(item["value_origin"] == "owner_decision" for item in pending))

    def test_neurobiology_citation_conflict_is_explicit(self) -> None:
        ledger = self.load("enrichment-ledger.json")
        correction = next(
            item
            for item in ledger["entries"]
            if item["id"] == "enrich-autism-source-neurobiology-citation-correction"
        )
        self.assertEqual("verified", correction["review_state"])
        self.assertIn("Cheung", correction["proposed_value"])
        self.assertIn("Lau", correction["proposed_value"])
        self.assertIn("conflicts", correction["limitations"][0].lower())
        self.assertIn("Kawakami", SOURCE.read_text(encoding="utf-8"))

    def test_d1_accepts_corrected_future_citation_without_mutating_v01(self) -> None:
        decisions = self.load("owner-decisions.json")["decisions"]
        by_id = {item["id"]: item for item in decisions}
        d1 = by_id["d1-neurobiology-citation-correction"]
        self.assertEqual("accepted", d1["status"])
        self.assertIn("Cheung", d1["accepted_value"])
        self.assertIn("Lau", d1["accepted_value"])
        self.assertTrue(d1["preserve_legacy_source_text"])
        self.assertFalse(d1["authoritative_v01_mutation_authorised"])
        self.assertFalse(d1["authoritative_v02_replacement_authorised"])
        self.assertEqual(AUTISM_V01_BLOB, git_blob_sha(SOURCE))
        self.assertIn("Kawakami, S. et al.", SOURCE.read_text(encoding="utf-8"))
        pending = {item["id"] for item in decisions if item["status"] == "pending"}
        self.assertEqual(
            {
                "d3-uncertainty-reduction-shape",
                "d4-ecosystem-entry-points-home",
                "d5-autism-neurodiversity-structural-closure",
            },
            pending,
        )

    def test_d2_defers_related_to_without_mapping_or_inventing_confidence(self) -> None:
        decisions = self.load("owner-decisions.json")["decisions"]
        by_id = {item["id"]: item for item in decisions}
        d2 = by_id["d2-related-to-mapping"]
        self.assertEqual("accepted", d2["status"])
        self.assertEqual("legacy_retained_unmapped", d2["accepted_disposition"])
        self.assertFalse(d2["map_to_associated_with_authorised"])
        self.assertFalse(d2["invent_relation_confidence_authorised"])
        self.assertFalse(d2["authoritative_v01_mutation_authorised"])
        self.assertFalse(d2["authoritative_v02_replacement_authorised"])

        ledger = self.load("preservation-ledger.json")
        related = [
            item
            for item in ledger["entries"]
            if item["unit"].startswith("relation:") and '\"type\":\"related_to\"' in item["unit"]
        ]
        self.assertEqual(2, len(related))
        self.assertTrue(all(item["disposition"] == "legacy_retained_unmapped" for item in related))
        self.assertTrue(all(item["owner_decision_ref"] == "d2-related-to-mapping" for item in related))
        self.assertTrue(all(item["legacy_value"]["type"] == "related_to" for item in related))
        self.assertTrue(all("confidence" not in item["legacy_value"] for item in related))
        self.assertEqual(
            {"sensory-processing", "executive-function"},
            {item["legacy_value"]["target_id"] for item in related},
        )
        self.assertTrue(all("candidate_destination" not in item for item in related))
        self.assertEqual(AUTISM_V01_BLOB, git_blob_sha(SOURCE))

    def test_evidence_roles_remain_bounded(self) -> None:
        ledger = self.load("enrichment-ledger.json")
        roles = {
            item["id"]: item["proposed_value"]
            for item in ledger["entries"]
            if item["target_field"].endswith(".role")
        }
        self.assertEqual("supportive", roles["enrich-autism-source-who-autism-claim-1-role"])
        self.assertEqual("supportive", roles["enrich-autism-source-neurobiology-autism-claim-2-role"])
        self.assertEqual("compatible", roles["enrich-autism-source-who-autism-claim-2-role"])

    def test_structural_dependency_records_existing_legacy_reciprocal(self) -> None:
        ledger = self.load("dependency-ledger.json")
        dependency = ledger["entries"][0]
        self.assertEqual("unresolved", dependency["resolution_status"])
        self.assertTrue(any("broader_than -> autism" in item for item in dependency["resolution_evidence"]))

    def test_source_blob_drift_fails_closed(self) -> None:
        manifest = self.load("manifest.json")
        manifest["sources"][0]["blob_sha"] = "0" * 40
        self.save("manifest.json", manifest)
        self.assertTrue(any("blob drift" in item for item in validate_package(self.package)))

    def test_omitted_preservation_unit_fails_closed(self) -> None:
        ledger = self.load("preservation-ledger.json")
        ledger["entries"].pop()
        self.save("preservation-ledger.json", ledger)
        self.assertTrue(any("omitted preservation units" in item for item in validate_package(self.package)))

    def test_unknown_preservation_unit_fails_closed(self) -> None:
        ledger = self.load("preservation-ledger.json")
        ledger["entries"].append({"unit": "summary:\"invented\"", "disposition": "represented_exactly"})
        self.save("preservation-ledger.json", ledger)
        self.assertTrue(any("unknown preservation units" in item for item in validate_package(self.package)))

    def test_duplicate_preservation_unit_fails_closed(self) -> None:
        ledger = self.load("preservation-ledger.json")
        ledger["entries"].append(copy.deepcopy(ledger["entries"][0]))
        self.save("preservation-ledger.json", ledger)
        self.assertTrue(any("exactly once" in item for item in validate_package(self.package)))

    def test_placeholder_cannot_satisfy_verified_enrichment(self) -> None:
        ledger = self.load("enrichment-ledger.json")
        item = ledger["entries"][0]
        item["review_state"] = "verified"
        item["value_origin"] = "verified_evidence"
        item["evidence_route"] = ["https://example.invalid/evidence"]
        item["proposed_value"] = "TBD"
        self.save("enrichment-ledger.json", ledger)
        self.assertTrue(any("placeholder or missing value" in item for item in validate_package(self.package)))

    def test_verified_enrichment_requires_evidence_route(self) -> None:
        ledger = self.load("enrichment-ledger.json")
        item = ledger["entries"][0]
        item["review_state"] = "verified"
        item["value_origin"] = "verified_evidence"
        item["proposed_value"] = "Verified title"
        item["evidence_route"] = []
        self.save("enrichment-ledger.json", ledger)
        self.assertTrue(any("requires an evidence route" in item for item in validate_package(self.package)))

    def test_deterministic_transform_cannot_manufacture_enrichment_semantics(self) -> None:
        ledger = self.load("enrichment-ledger.json")
        ledger["entries"][0]["value_origin"] = "deterministic_transform"
        self.save("enrichment-ledger.json", ledger)
        errors = validate_package(self.package)
        self.assertTrue(any("deterministic_transform" in item and "not one of" in item for item in errors))

    def test_unresolved_owner_decisions_prevent_ready_state(self) -> None:
        manifest = self.load("manifest.json")
        manifest["package_status"] = "ready_for_authoritative_review"
        self.save("manifest.json", manifest)
        self.assertTrue(any("unresolved preservation dispositions" in item for item in validate_package(self.package)))

    def test_unresolved_structural_dependency_prevents_ready_state(self) -> None:
        manifest = self.load("manifest.json")
        manifest["package_status"] = "ready_for_authoritative_review"
        self.save("manifest.json", manifest)
        self.assertTrue(any("structural dependencies" in item for item in validate_package(self.package)))

    def test_legacy_unmapped_value_must_remain_exact(self) -> None:
        ledger = self.load("preservation-ledger.json")
        item = next(entry for entry in ledger["entries"] if entry["disposition"] == "legacy_retained_unmapped")
        item["legacy_value"]["questions"][0] = "Changed question"
        self.save("preservation-ledger.json", ledger)
        self.assertTrue(any("retained legacy value does not match" in item for item in validate_package(self.package)))

    def test_related_to_is_not_auto_converted(self) -> None:
        ledger = self.load("preservation-ledger.json")
        item = next(
            entry
            for entry in ledger["entries"]
            if entry["unit"].startswith("relation:") and '\"type\":\"related_to\"' in entry["unit"]
        )
        item["candidate_destination"] = "candidate relation associated_with"
        self.save("preservation-ledger.json", ledger)
        self.assertTrue(any("related_to cannot auto-map" in item for item in validate_package(self.package)))

    def test_ecosystem_questions_are_not_auto_promoted(self) -> None:
        candidate = self.package / "candidate"
        candidate.mkdir()
        (candidate / "question.json").write_text(
            json.dumps(
                {
                    "schema_version": "0.2",
                    "id": "auto-promoted-question",
                    "type": "question",
                    "question": "What barrier is being changed?",
                }
            ),
            encoding="utf-8",
        )
        self.assertTrue(any("auto-promotes ecosystem entry text" in item for item in validate_package(self.package)))

    def test_authoritative_replacement_remains_separate(self) -> None:
        manifest = self.load("manifest.json")
        manifest["authoritative_replacement"] = True
        self.save("manifest.json", manifest)
        self.assertTrue(any("False was expected" in item for item in validate_package(self.package)))


if __name__ == "__main__":
    unittest.main()
