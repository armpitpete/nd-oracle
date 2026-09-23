import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_JSON = ROOT / "contracts" / "navigation-v1.json"
CONTRACT_MD = ROOT / "docs" / "ND_UX_V2_NAVIGATION_CONTRACT_v1.md"
DESIGN = ROOT / "docs" / "ND_UX_V2_5_DESIGN_SYSTEM.md"
USER_TEST = ROOT / "docs" / "ND_UX_V2_USER_TEST_PROTOCOL.md"
EVIDENCE_WORKFLOW = ROOT / ".github" / "workflows" / "ux-visual-evidence.yml"

EXPECTED_PRIMARY = [
    "Conditions",
    "Books",
    "Games",
    "Apps & tools",
    "Organisations & peer groups",
    "Work & education",
    "Health & diagnosis",
    "Daily living",
    "Evidence & research",
]
EXPECTED_SECONDARY = ["Search", "A–Z", "Browse everything", "Not sure where to start?"]
ABSTRACT = {"Resources", "Topics", "Needs", "Questions"}


class NavigationContractV1Tests(unittest.TestCase):
    def setUp(self):
        self.contract = json.loads(CONTRACT_JSON.read_text(encoding="utf-8"))

    def test_release_blocking_rule_is_exact_and_mobile_scoped(self):
        self.assertEqual(
            "A new visitor can tell that ND Oracle contains things such as conditions, books, games and apps, and can reach them without first learning what “Resources”, “Topics”, “Needs” or similar internal categories mean.",
            self.contract["acceptance_rule"],
        )
        self.assertEqual(["desktop", "narrow/mobile"], self.contract["applies_to"])
        self.assertEqual(168, self.contract["release_blocking_for_pr"])

    def test_primary_categories_are_concrete_frozen_and_bounded(self):
        labels = [item["label"] for item in self.contract["primary_categories"]]
        self.assertEqual(EXPECTED_PRIMARY, labels)
        self.assertEqual(9, self.contract["first_decision_area"]["max_prominent_choices"])
        self.assertTrue(ABSTRACT.isdisjoint(labels))
        for item in self.contract["primary_categories"]:
            self.assertTrue(item["purpose"])
            self.assertTrue(item["includes"])
            self.assertTrue(item["excludes"])
            self.assertTrue(item["target_route"].startswith("/"))

    def test_secondary_utilities_and_uncertainty_escape_are_bounded(self):
        self.assertEqual(EXPECTED_SECONDARY, [item["label"] for item in self.contract["secondary_utilities"]])
        self.assertEqual(4, self.contract["uncertainty_route"]["max_choices"])
        self.assertEqual(4, len(self.contract["uncertainty_route"]["choices"]))
        self.assertEqual("Not sure where to start?", self.contract["secondary_utilities"][-1]["label"])

    def test_internal_taxonomy_is_not_primary_vocabulary(self):
        self.assertEqual(["Resources", "Topics", "Needs", "Questions"], self.contract["internal_terms"])
        self.assertIn("must not need to understand", self.contract["terminology_rule"])
        self.assertEqual(
            "Primary content categories → secondary utilities → deeper/internal browsing tools.",
            self.contract["hierarchy_rule"],
        )

    def test_direct_reachability_and_no_duplicate_authority(self):
        direct = self.contract["direct_reachability"]
        self.assertEqual("Home → category → item", direct["target_pattern"])
        self.assertIn("Resources", direct["avoidable_failure_pattern"])
        overlap = "\n".join(self.contract["overlap_rules"])
        self.assertIn("one governed object", overlap)
        self.assertIn("without cloning", overlap)

    def test_protected_boundaries_are_explicit(self):
        protected = self.contract["protected_boundaries"]
        for marker in (
            "objects/",
            "schema/",
            "discovery/",
            "contracts/current-production.json",
            ".github/workflows/deploy-cloudflare-pages.yml",
        ):
            self.assertIn(marker, protected)
        self.assertIn("presentation/navigation authority only", self.contract["implementation_boundary"])

    def test_existing_visual_evidence_already_covers_home_desktop_and_narrow(self):
        workflow = EVIDENCE_WORKFLOW.read_text(encoding="utf-8")
        self.assertIn('"home|/"', workflow)
        self.assertIn("capture baseline 8765 1440,1100 desktop", workflow)
        self.assertIn("capture baseline 8765 390,844 narrow", workflow)
        self.assertIn("capture candidate 8766 1440,1100 desktop", workflow)
        self.assertIn("capture candidate 8766 390,844 narrow", workflow)

    def test_design_authority_points_to_navigation_contract(self):
        design = DESIGN.read_text(encoding="utf-8")
        self.assertIn("ND_UX_V2_NAVIGATION_CONTRACT_v1.md", design)
        self.assertIn("concrete visitor-recognisable categories", design)

    def test_human_protocol_binds_first_impression_and_simple_outcomes(self):
        text = USER_TEST.read_text(encoding="utf-8")
        self.assertIn("Without clicking anything, what kinds of things do you think you can find on this website?", text)
        for label in ("Found it", "Confusing", "Couldn't find it"):
            self.assertIn(label, text)
        for task in (
            "one condition",
            "one book",
            "one game",
            "one app/tool",
            "one organisation/peer group",
            "one practical-help route",
        ):
            self.assertIn(task, text)

    def test_markdown_and_machine_contract_share_authority(self):
        md = CONTRACT_MD.read_text(encoding="utf-8")
        self.assertIn(self.contract["acceptance_rule"], md)
        self.assertIn("Phase 1 is complete", md)
        self.assertIn("Actual Home/category implementation is Phase 2", md)


if __name__ == "__main__":
    unittest.main()
