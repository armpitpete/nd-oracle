from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts import build_site


ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
CURRENT_POINTER = ROOT / "contracts" / "current-production.json"
CURRENT_PRODUCTION = ROOT / "docs" / "PRODUCTION_STATE_2026-09-04_IRELAND_ASSESSMENT_DIAGNOSIS_v1.md"
UK_BASELINE = ROOT / "docs" / "UK_REFERENCE_BASELINE_v1.md"
PREVIOUS_UK_BASELINE_PRODUCTION = ROOT / "docs" / "PRODUCTION_STATE_2026-09-04_UK_REFERENCE_BASELINE_v1.md"
PREVIOUS_PRODUCTION = ROOT / "docs" / "PRODUCTION_STATE_2026-09-03_RELATIONSHIPS_FAMILY.md"
PREVIOUS_20260903_PRODUCTION = ROOT / "docs" / "PRODUCTION_STATE_2026-09-03.md"
V12_PRODUCTION = ROOT / "docs" / "PRODUCTION_STATE_v1.2.md"
V11_PRODUCTION = ROOT / "docs" / "PRODUCTION_STATE_v1.1.md"
V10_PRODUCTION = ROOT / "docs" / "PRODUCTION_STATE_v1.0.md"

CURRENT_RELEASE_SHA = "10fe0a0bc1f1a075e420dd0bc432d0a69cc15197"
CURRENT_TREE_SHA = "bce34c6908a409daefce1ba24ce06349fa24cac2"
CURRENT_ARTIFACT_SHA256 = "4967f8a711aefeb8bf878de7dba5a18063cd57d0b1ca54e53d6022d9cfe5f033"
CURRENT_DEPLOYMENT_RUN = 33896144673
CURRENT_VERIFICATION_RUN = 33896431576
CURRENT_VERIFICATION_JOB = 101100054619

PREVIOUS_UK_BASELINE_RELEASE_SHA = "579c012cc9b31707409579da05b52a4d07efe61c"
PREVIOUS_UK_BASELINE_ARTIFACT_SHA256 = "5357cc31658b37dc6c7d9f0ff4f0330894df8877a7869024ad6feefce8d4e0f4"

PREVIOUS_RELEASE_SHA = "5c05d775a5d548c0f4ad92f78e25008febe40d69"
PREVIOUS_ARTIFACT_SHA256 = "4864e9a9aa56a3278ad46d4a32695354f25018b9ce9d2ccb46cf8fa68ba4ba2a"
PREVIOUS_20260903_RELEASE_SHA = "20926066e76e06beeef7d9ba87f24b88bada8658"
PREVIOUS_20260903_ARTIFACT_SHA256 = "166bab6dc89dd02d119dbba23035f948666a5b3e3ee39cd179f71a45d3289c71"
HISTORICAL_V12_RELEASE_SHA = "fad8e560979ba67bf94104d02f3b5100db8572cf"
HISTORICAL_V12_ARTIFACT_SHA256 = "b88c462115434d3ce9929f1e62ec29d0fb0095c13c05ec17c87b813afea426a1"
V11_RELEASE_SHA = "3032305dd81d48b2c6cc777b72f038267f995819"
V10_RELEASE_SHA = "a0081e7d879e23568792ad5a468250eeb21dd20b"

BASELINE_CONTENT_SHA = "802e69b4437a276c234a036d9cd8f3f58f582b71"
BASELINE_CONTENT_TREE = "8cf57114836ba4e5443d5bae3943531aa2f42722"


def load_current() -> dict:
    return json.loads(CURRENT_POINTER.read_text(encoding="utf-8"))


class ReleaseStateIntegrityTests(unittest.TestCase):
    def test_current_pointer_names_exact_accepted_production(self) -> None:
        current = load_current()
        self.assertEqual("1", current["schema_version"])
        self.assertEqual("accepted", current["status"])
        self.assertEqual("2026-09-04", current["as_of"])
        self.assertEqual("https://ndoracle.org", current["canonical_site"])
        self.assertEqual("v1.2", current["builder_release"])
        self.assertEqual(
            "docs/PRODUCTION_STATE_2026-09-04_IRELAND_ASSESSMENT_DIAGNOSIS_v1.md",
            current["production_state_document"],
        )
        self.assertEqual(CURRENT_RELEASE_SHA, current["source_sha"])
        self.assertEqual(CURRENT_TREE_SHA, current["source_tree_sha"])

        deployment = current["deployment"]
        self.assertEqual(CURRENT_DEPLOYMENT_RUN, deployment["workflow_run_id"])
        self.assertEqual(24, deployment["workflow_run_number"])
        self.assertEqual(101099134040, deployment["guard_job_id"])
        self.assertEqual(101099176328, deployment["upload_job_id"])
        self.assertEqual(CURRENT_ARTIFACT_SHA256, deployment["artifact_sha256"])
        self.assertEqual("https://325a78a3.nd-oracle.pages.dev", deployment["cloudflare_deployment"])
        self.assertEqual("nd-oracle", deployment["cloudflare_project"])
        self.assertEqual("main", deployment["production_branch"])
        self.assertEqual(33896104483, deployment["dispatch_helper_run_id"])
        self.assertEqual(101099001632, deployment["dispatch_helper_job_id"])
        self.assertEqual("ec4e3bca4357b615d72f59f8616e32307bcf1214", deployment["dispatch_helper_commit"])
        self.assertEqual("release/temp-dispatch-ireland-v1-production", deployment["dispatch_helper_branch"])

        verification = current["verification"]
        self.assertEqual(CURRENT_VERIFICATION_RUN, verification["workflow_run_id"])
        self.assertEqual(18, verification["workflow_run_number"])
        self.assertEqual(CURRENT_VERIFICATION_JOB, verification["job_id"])
        self.assertEqual(33896422762, verification["dispatch_helper_run_id"])
        self.assertEqual(101100013185, verification["dispatch_helper_job_id"])
        self.assertEqual("7a9e8ae9927a738008f346347b37b52353fbdd61", verification["dispatch_helper_commit"])
        self.assertEqual("release/temp-dispatch-ireland-v1-live-verify", verification["dispatch_helper_branch"])
        self.assertEqual(403, verification["canonical_routes_verified"])
        self.assertEqual(439, verification["regression_tests_passed"])

        corpus = current["corpus"]
        self.assertEqual(319, corpus["governed_objects"])
        self.assertEqual(20, corpus["concepts"])
        self.assertEqual(144, corpus["resources"])
        self.assertEqual(152, corpus["questions"])
        self.assertEqual(3, corpus["evidence_objects"])
        self.assertEqual(60, corpus["governed_source_records"])
        self.assertEqual(49, corpus["governed_claims"])
        self.assertEqual(49, corpus["covered_claims"])
        self.assertEqual(0, corpus["evidence_gaps"])
        self.assertEqual(0, corpus["overdue_source_records"])
        self.assertEqual(0, corpus["overdue_governed_objects"])

    def test_readme_current_production_matches_pointer(self) -> None:
        current = load_current()
        text = README.read_text(encoding="utf-8")
        for value in (
            current["source_sha"],
            current["source_tree_sha"],
            current["deployment"]["artifact_sha256"],
            str(current["deployment"]["workflow_run_id"]),
            str(current["verification"]["workflow_run_id"]),
            str(current["verification"]["job_id"]),
            current["production_state_document"],
            "contracts/current-production.json",
        ):
            self.assertIn(value, text)
        self.assertIn("Current production is the accepted **UK Reference Baseline v1 + Republic of Ireland Assessment & diagnosis v1** deployment", text)
        self.assertIn("319 governed objects", text)
        self.assertIn("403 canonical routes", text)

    def test_current_production_record_matches_pointer(self) -> None:
        current = load_current()
        production_path = ROOT / current["production_state_document"]
        self.assertEqual(CURRENT_PRODUCTION, production_path)
        self.assertTrue(production_path.is_file())
        text = production_path.read_text(encoding="utf-8")
        for value in (
            current["source_sha"],
            current["source_tree_sha"],
            current["deployment"]["artifact_sha256"],
            str(current["deployment"]["workflow_run_id"]),
            str(current["deployment"]["guard_job_id"]),
            str(current["deployment"]["upload_job_id"]),
            str(current["verification"]["workflow_run_id"]),
            str(current["verification"]["job_id"]),
            current["deployment"]["cloudflare_deployment"],
        ):
            self.assertIn(value, text)
        self.assertIn("319 governed objects", text)
        self.assertIn("439-test regression suite", text)
        self.assertIn("403 canonical", text)
        self.assertIn("All 49 Claims remain evidence-covered", text)
        self.assertIn("60 governed source records", text)
        self.assertIn("60 governed Evidence source records checked; 0 overdue", text)
        self.assertIn("319 governed objects checked; 0 overdue", text)

    def test_accepted_production_remains_a_floor_while_repository_head_may_advance(self) -> None:
        current = load_current()
        corpus = current["corpus"]
        self.assertEqual(
            corpus["concepts"] + corpus["resources"] + corpus["questions"] + corpus["evidence_objects"],
            corpus["governed_objects"],
        )
        self.assertEqual(319, corpus["governed_objects"])
        self.assertEqual(403, current["verification"]["canonical_routes_verified"])
        self.assertGreaterEqual(len(build_site.load_concepts()), corpus["concepts"])
        self.assertGreaterEqual(len(build_site.load_resources()), corpus["resources"])
        self.assertGreaterEqual(len(build_site.load_questions()), corpus["questions"])
        self.assertGreaterEqual(len(build_site.load_evidence()), corpus["evidence_objects"])
        self.assertGreaterEqual(build_site.V10_ROUTE_COUNT, current["verification"]["canonical_routes_verified"])

    def test_current_discovery_counts_are_explicit_and_additive(self) -> None:
        discovery = load_current()["discovery"]
        self.assertEqual(41, discovery["frozen_base_scoped_routes"])
        self.assertEqual(29, discovery["assessment_extension_scoped_routes"])
        self.assertEqual(12, discovery["ireland_assessment_extension_scoped_routes"])
        self.assertEqual(82, discovery["total_scoped_routes"])
        self.assertEqual(
            discovery["frozen_base_scoped_routes"]
            + discovery["assessment_extension_scoped_routes"]
            + discovery["ireland_assessment_extension_scoped_routes"],
            discovery["total_scoped_routes"],
        )

    def test_uk_reference_baseline_content_snapshot_remains_frozen(self) -> None:
        text = UK_BASELINE.read_text(encoding="utf-8")
        self.assertIn(BASELINE_CONTENT_SHA, text)
        self.assertIn(BASELINE_CONTENT_TREE, text)
        self.assertIn("**307 governed objects**", text)
        self.assertIn("**391 canonical public routes**", text)
        self.assertIn("FROZEN CONTENT BASELINE", text)
        self.assertNotIn(CURRENT_ARTIFACT_SHA256, text)

    def test_previous_uk_baseline_production_evidence_remains_frozen(self) -> None:
        current = load_current()
        self.assertNotEqual(
            "docs/PRODUCTION_STATE_2026-09-04_UK_REFERENCE_BASELINE_v1.md",
            current["production_state_document"],
        )
        text = PREVIOUS_UK_BASELINE_PRODUCTION.read_text(encoding="utf-8")
        self.assertIn(PREVIOUS_UK_BASELINE_RELEASE_SHA, text)
        self.assertIn(PREVIOUS_UK_BASELINE_ARTIFACT_SHA256, text)
        self.assertIn("307 governed objects", text)
        self.assertIn("416-test regression suite", text)
        self.assertIn("391 canonical", text)
        self.assertNotIn(CURRENT_RELEASE_SHA, text)
        self.assertNotIn(CURRENT_ARTIFACT_SHA256, text)

    def test_previous_relationships_production_evidence_remains_frozen(self) -> None:
        current = load_current()
        self.assertNotEqual(
            "docs/PRODUCTION_STATE_2026-09-03_RELATIONSHIPS_FAMILY.md",
            current["production_state_document"],
        )
        text = PREVIOUS_PRODUCTION.read_text(encoding="utf-8")
        self.assertIn(PREVIOUS_RELEASE_SHA, text)
        self.assertIn(PREVIOUS_ARTIFACT_SHA256, text)
        self.assertIn("208 governed objects", text)
        self.assertIn("392-test regression suite", text)
        self.assertIn("292 canonical", text)
        self.assertNotIn(CURRENT_RELEASE_SHA, text)
        self.assertNotIn(CURRENT_ARTIFACT_SHA256, text)

    def test_previous_20260903_production_evidence_remains_frozen(self) -> None:
        text = PREVIOUS_20260903_PRODUCTION.read_text(encoding="utf-8")
        self.assertIn(PREVIOUS_20260903_RELEASE_SHA, text)
        self.assertIn(PREVIOUS_20260903_ARTIFACT_SHA256, text)
        self.assertIn("190 governed objects", text)
        self.assertIn("380-test permanent regression suite", text)
        self.assertIn("274 canonical", text)
        self.assertNotIn(CURRENT_RELEASE_SHA, text)
        self.assertNotIn(CURRENT_ARTIFACT_SHA256, text)

    def test_historical_v12_production_evidence_remains_frozen(self) -> None:
        text = V12_PRODUCTION.read_text(encoding="utf-8")
        self.assertIn("# ND Oracle production state v1.2", text)
        self.assertIn(HISTORICAL_V12_RELEASE_SHA, text)
        self.assertIn(HISTORICAL_V12_ARTIFACT_SHA256, text)
        self.assertIn("335-test permanent regression suite", text)
        self.assertIn("148 canonical", text)
        self.assertIn("125 authoritative objects", text)
        self.assertIn("600ea685.nd-oracle.pages.dev", text)
        self.assertNotIn(CURRENT_RELEASE_SHA, text)

    def test_v11_production_evidence_remains_frozen(self) -> None:
        text = V11_PRODUCTION.read_text(encoding="utf-8")
        self.assertIn("# ND Oracle production state v1.1", text)
        self.assertIn(V11_RELEASE_SHA, text)
        self.assertIn("84f6ac3e76d07d26367794b87cf6f85736aa4d8e976865d2d79a806bd429dfb7", text)

    def test_v10_production_evidence_remains_frozen(self) -> None:
        text = V10_PRODUCTION.read_text(encoding="utf-8")
        self.assertIn("# ND Oracle production state v1.0", text)
        self.assertIn(V10_RELEASE_SHA, text)


if __name__ == "__main__":
    unittest.main()
