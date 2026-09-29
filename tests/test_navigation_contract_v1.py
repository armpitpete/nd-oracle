import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_JSON = ROOT / "contracts" / "navigation-v1.json"
CONTRACT_MD = ROOT / "docs" / "ND_UX_V2_NAVIGATION_CONTRACT_v1.md"
DESIGN = ROOT / "docs" / "ND_UX_V2_5_DESIGN_SYSTEM.md"
USER_TEST = ROOT / "docs" / "ND_UX_V2_USER_TEST_PROTOCOL.md"
EVIDENCE_WORKFLOW = ROOT / ".github" / "workflows" / "ux-visual-evidence.yml"
EVIDENCE_RUNNER = ROOT / "scripts" / "run_ux_visual_evidence.sh"

EXPECTED_PRIMARY = [
    "ADHD, autism & other neurodivergence",
    "Help with everyday life",
    "Books, films & media",
    "Games & apps",
    "Find support",
    "Ask a question",
]
EXPECTED_SECONDARY = [
    "Areas of life",
    "Browse A–Z",
    "Browse by place",
    "Questions",
    "Topics",
    "All resources",
]
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

    def test_primary_categories_are_concrete_and_bounded_to_six(self):
        labels = [item["label"] for item in self.contract["primary_categories"]]
        self.assertEqual(EXPECTED_PRIMARY, labels)
        self.assertEqual(6, self.contract["first_decision_area"]["max_prominent_choices"])
        self.assertTrue(ABSTRACT.isdisjoint(labels))
        self.assertEqual(["What are you looking for?"], [g["label"] for g in self.contract["first_decision_area"]["groups"]])
        for item in self.contract["primary_categories"]:
            self.assertTrue(item["purpose"])
            self.assertTrue(item["includes"])
            self.assertTrue(item["excludes"])
            self.assertTrue(item["target_route"].startswith("/"))

    def test_search_is_separate_and_secondary_exploration_is_bounded(self):
        self.assertEqual(["Search ND Oracle"], [item["label"] for item in self.contract["secondary_utilities"]])
        self.assertEqual(EXPECTED_SECONDARY, [item["label"] for item in self.contract["secondary_exploration"]])
        self.assertIn("Search is a separate escape route", self.contract["first_decision_area"]["rule"])

    def test_internal_taxonomy_is_not_primary_vocabulary(self):
        self.assertEqual(["Resources", "Topics", "Needs", "Questions"], self.contract["internal_terms"])
        self.assertIn("must not need to understand", self.contract["terminology_rule"])
        self.assertEqual(
            "Six primary Home routes → separate Search → collapsed secondary exploration → deeper/internal browsing tools.",
            self.contract["hierarchy_rule"],
        )

    def test_direct_reachability_recovery_and_no_duplicate_authority(self):
        direct = self.contract["direct_reachability"]
        self.assertEqual("Home → clear first-hop route → item or next concrete choice", direct["target_pattern"])
        self.assertIn("internal taxonomy term", direct["avoidable_failure_pattern"])
        overlap = "\n".join(self.contract["overlap_rules"])
        self.assertIn("governed object", overlap.lower())
        self.assertIn("presentation layer", overlap)
        self.assertIn("No first choice becomes a dead end", self.contract["recovery_rule"])

    def test_scope_is_bounded_to_home_and_first_hop(self):
        scope = "\n".join(self.contract["scope_guard"])
        self.assertIn("Home", scope)
        self.assertIn("first-hop", scope)
        self.assertIn("Do not restructure the wider ND Oracle taxonomy", scope)
        self.assertIn("Governed knowledge and production authority stay protected", self.contract["implementation_boundary"])

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

    def test_existing_visual_evidence_already_covers_home_desktop_and_narrow(self):
        workflow = EVIDENCE_WORKFLOW.read_text(encoding="utf-8")
        runner = EVIDENCE_RUNNER.read_text(encoding="utf-8")
        self.assertIn("bash candidate/scripts/run_ux_visual_evidence.sh", workflow)
        self.assertIn('"home|/"', runner)
        self.assertIn("capture baseline 8765 1440,1100 desktop", runner)
        self.assertIn("capture baseline 8765 390,844 narrow", runner)
        self.assertIn("capture candidate 8766 1440,1100 desktop", runner)
        self.assertIn("capture candidate 8766 390,844 narrow", runner)

    def test_design_authority_points_to_navigation_contract(self):
        design = DESIGN.read_text(encoding="utf-8")
        self.assertIn("ND_UX_V2_NAVIGATION_CONTRACT_v1.md", design)
        self.assertIn("concrete visitor-recognisable categories", design)

    def test_human_protocol_binds_comprehension_recovery_and_simple_outcomes(self):
        text = USER_TEST.read_text(encoding="utf-8")
        self.assertIn("Without clicking anything, what kinds of things do you think you can find on this website?", text)
        self.assertIn("What would you expect to find here?", text)
        self.assertIn("wrong first route", text)
        for label in ("Found it", "Confusing", "Couldn't find it"):
            self.assertIn(label, text)
        for task in (
            "Find information about ADHD",
            "Find a book about an autistic young person",
            "Find an app",
            "Find help with sensory overload",
            "Find a local neurodivergent peer group",
        ):
            self.assertIn(task, text)

    def test_markdown_and_machine_contract_share_authority(self):
        md = CONTRACT_MD.read_text(encoding="utf-8")
        self.assertIn(self.contract["acceptance_rule"], md)
        self.assertIn("six primary Home routes", md)
        self.assertIn("wrong-choice recovery", md)


if __name__ == "__main__":
    unittest.main()
