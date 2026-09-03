from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts import build_site


ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
CURRENT_POINTER = ROOT / "contracts" / "current-production.json"
V12_PRODUCTION = ROOT / "docs" / "PRODUCTION_STATE_v1.2.md"
V11_PRODUCTION = ROOT / "docs" / "PRODUCTION_STATE_v1.1.md"
V10_PRODUCTION = ROOT / "docs" / "PRODUCTION_STATE_v1.0.md"

CURRENT_RELEASE_SHA = "20926066e76e06beeef7d9ba87f24b88bada8658"
CURRENT_TREE_SHA = "e19ef7a180a1ad5b31849763aa00b516f384d53e"
CURRENT_ARTIFACT_SHA256 = "166bab6dc89dd02d119dbba23035f948666a5b3e3ee39cd179f71a45d3289c71"
CURRENT_DEPLOYMENT_RUN = 33784220017
CURRENT_VERIFICATION_RUN = 33785057163
CURRENT_VERIFICATION_JOB = 100747694338
HISTORICAL_V12_RELEASE_SHA = "fad8e560979ba67bf94104d02f3b5100db8572cf"
HISTORICAL_V12_ARTIFACT_SHA256 = "b88c462115434d3ce9929f1e62ec29d0fb0095c13c05ec17c87b813afea426a1"
V11_RELEASE_SHA = "3032305dd81d48b2c6cc777b72f038267f995819"
V10_RELEASE_SHA = "a0081e7d879e23568792ad5a468250eeb21dd20b"


def load_current() -> dict:
    return json.loads(CURRENT_POINTER.read_text(encoding="utf-8"))


class ReleaseStateIntegrityTests(unittest.TestCase):
    def test_current_pointer_names_exact_accepted_production(self) -> None:
        current = load_current()
        self.assertEqual("1", current["schema_version"])
        self.assertEqual("accepted", current["status"])
        self.assertEqual("2026-09-03", current["as_of"])
        self.assertEqual("https://ndoracle.org", current["canonical_site"])
        self.assertEqual("v1.2", current["builder_release"])
        self.assertEqual("docs/PRODUCTION_STATE_2026-09-03.md", current["production_state_document"])
        self.assertEqual(CURRENT_RELEASE_SHA, current["source_sha"])
        self.assertEqual(CURRENT_TREE_SHA, current["source_tree_sha"])

        deployment = current["deployment"]
        self.assertEqual(CURRENT_DEPLOYMENT_RUN, deployment["workflow_run_id"])
        self.assertEqual(19, deployment["workflow_run_number"])
        self.assertEqual(100744979763, deployment["guard_job_id"])
        self.assertEqual(100745012361, deployment["upload_job_id"])
        self.assertEqual(CURRENT_ARTIFACT_SHA256, deployment["artifact_sha256"])
        self.assertEqual("https://4651e0b6.nd-oracle.pages.dev", deployment["cloudflare_deployment"])
        self.assertEqual("nd-oracle", deployment["cloudflare_project"])
        self.assertEqual("main", deployment["production_branch"])

        verification = current["verification"]
        self.assertEqual(CURRENT_VERIFICATION_RUN, verification["workflow_run_id"])
        self.assertEqual(316, verification["workflow_run_number"])
        self.assertEqual(CURRENT_VERIFICATION_JOB, verification["job_id"])
        self.assertEqual(135, verification["temporary_pr"])
        self.assertEqual(274, verification["canonical_routes_verified"])
        self.assertEqual(380, verification["regression_tests_passed"])

        corpus = current["corpus"]
        self.assertEqual(190, corpus["governed_objects"])
        self.assertEqual(20, corpus["concepts"])
        self.assertEqual(91, corpus["resources"])
        self.assertEqual(76, corpus["questions"])
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
        self.assertIn("Current production is the accepted 2026-09-03 deployment", text)
        self.assertNotIn("Production is the accepted v1.2 release", text)

    def test_current_production_record_matches_pointer(self) -> None:
        current = load_current()
        production_path = ROOT / current["production_state_document"]
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
        self.assertIn("190 governed objects", text)
        self.assertIn("380-test permanent regression suite", text)
        self.assertIn("274 canonical", text)
        self.assertIn("49/49 Claims covered", text)
        self.assertIn("60 governed source records", text)
        self.assertIn("60 checked, 0 overdue", text)
        self.assertIn("190 checked, 0 overdue", text)

    def test_accepted_production_remains_a_floor_while_repository_head_may_advance(self) -> None:
        current = load_current()
        corpus = current["corpus"]
        self.assertEqual(
            corpus["concepts"] + corpus["resources"] + corpus["questions"] + corpus["evidence_objects"],
            corpus["governed_objects"],
        )
        self.assertEqual(190, corpus["governed_objects"])
        self.assertEqual(274, current["verification"]["canonical_routes_verified"])
        self.assertGreaterEqual(len(build_site.load_concepts()), corpus["concepts"])
        self.assertGreaterEqual(len(build_site.load_resources()), corpus["resources"])
        self.assertGreaterEqual(len(build_site.load_questions()), corpus["questions"])
        self.assertGreaterEqual(len(build_site.load_evidence()), corpus["evidence_objects"])
        self.assertGreaterEqual(build_site.V10_ROUTE_COUNT, current["verification"]["canonical_routes_verified"])

    def test_current_discovery_counts_are_explicit_and_additive(self) -> None:
        discovery = load_current()["discovery"]
        self.assertEqual(41, discovery["frozen_base_scoped_routes"])
        self.assertEqual(29, discovery["assessment_extension_scoped_routes"])
        self.assertEqual(70, discovery["total_scoped_routes"])
        self.assertEqual(
            discovery["frozen_base_scoped_routes"] + discovery["assessment_extension_scoped_routes"],
            discovery["total_scoped_routes"],
        )

    def test_historical_v12_production_evidence_remains_frozen(self) -> None:
        current = load_current()
        self.assertNotEqual("docs/PRODUCTION_STATE_v1.2.md", current["production_state_document"])
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
