import json
import unittest
from pathlib import Path

from scripts import build_site


ROOT = Path(__file__).resolve().parents[1]
PUBLIC_STATE = ROOT / "contracts" / "current-public-state.json"
CURRENT_PRODUCTION = ROOT / "contracts" / "current-production.json"
GAP_MAP = ROOT / "docs" / "CONTENT_GAP_MAP_v2.0.md"
FUNCTIONAL_BASELINE = ROOT / "docs" / "ND_UX_V2_4_FUNCTIONAL_BASELINE.md"
DESIGN_SYSTEM = ROOT / "docs" / "ND_UX_V2_5_DESIGN_SYSTEM.md"
USER_TEST = ROOT / "docs" / "ND_UX_V2_USER_TEST_PROTOCOL.md"


class V2PublicBaselineTests(unittest.TestCase):
    def test_public_state_separates_knowledge_presentation_and_live_identity(self):
        public = json.loads(PUBLIC_STATE.read_text(encoding="utf-8"))
        current = json.loads(CURRENT_PRODUCTION.read_text(encoding="utf-8"))

        self.assertEqual(current["source_sha"], public["knowledge_baseline"]["source_sha"])
        self.assertEqual(current["corpus"]["governed_objects"], public["knowledge_baseline"]["governed_objects"])
        self.assertEqual(current["verification"]["canonical_routes_verified"], public["knowledge_baseline"]["canonical_routes"])
        self.assertEqual("0065ab8000bbb0020aa221f084525116f436b373", public["presentation_baseline"]["source_sha"])
        self.assertFalse(public["presentation_baseline"]["content_change"])
        self.assertEqual("not-yet-reconciled", public["live_site"]["deployment_identity_status"])

    def test_gap_map_is_bound_to_current_accepted_corpus(self):
        text = GAP_MAP.read_text(encoding="utf-8")
        for marker in (
            "366 governed objects",
            "450 canonical routes",
            "49/49 governed Claims covered",
            "0 evidence gaps",
            "90 governed scoped discovery routes",
        ):
            self.assertIn(marker, text)

        domains = (
            "Daily living",
            "Sensory needs",
            "Communication",
            "Work",
            "Education & study",
            "Assessment & diagnosis",
            "Relationships & family",
            "Money & administration",
            "Sleep",
            "Food & eating",
            "Healthcare access",
            "Mental wellbeing",
            "Mobility & travel",
            "Technology & accessibility",
            "Games & downtime",
            "Books & media",
            "Organisations & peer community",
        )
        for domain in domains:
            self.assertIn(f"| {domain} |", text)

    def test_v24_and_v25_doctrine_is_frozen_without_card_default(self):
        baseline = FUNCTIONAL_BASELINE.read_text(encoding="utf-8")
        design = DESIGN_SYSTEM.read_text(encoding="utf-8")
        css = (ROOT / "site" / "styles.css").read_text(encoding="utf-8")

        self.assertIn("page headings are directional landmarks, not hero cards", baseline)
        self.assertIn("No hero-and-card default grammar.", design)
        self.assertIn("ND-UX-V2.4: page-first composition", css)
        tail = css[css.index("ND-UX-V2.4: page-first composition"):]
        self.assertIn(".page .page-heading", tail)
        self.assertIn("background: transparent", tail)
        self.assertIn("border-left", tail)
        self.assertIn(".choice-card", tail)

    def test_home_is_short_orientation_surface_not_legacy_catalogue(self):
        concepts = build_site.load_concepts()
        resources = build_site.load_resources()
        questions = build_site.load_questions()
        page = build_site.render_index(concepts, resources, questions)

        self.assertIn("What do you need right now?", page)
        self.assertIn("Or start with an area of life", page)
        self.assertIn("Need another way in?", page)
        self.assertIn("Want the whole catalogue?", page)
        self.assertNotIn("More question shortcuts", page)
        self.assertNotIn('class="home-shortcuts"', page)

        for href in ("/find/", "/questions/", "/resources/", "/understand/", "/a-z/"):
            self.assertIn(f'href="{href}"', page)

    def test_human_task_gate_cannot_be_satisfied_by_automation(self):
        text = USER_TEST.read_text(encoding="utf-8")
        self.assertIn("not a substitute for real neurodivergent task evidence", text)
        self.assertIn("Do not mark this gate PASS", text)
        for task in (
            "I think I might have ADHD. Where do I begin?",
            "Phone calls are difficult.",
            "I need help at work.",
            "My child struggles with eating.",
            "What is monotropism?",
            "I want an autistic peer group.",
            "I don't know the correct word for my problem.",
            "I need help but I don't know which section.",
            "I want to understand the evidence behind this.",
            "I live outside England.",
        ):
            self.assertIn(task, text)


if __name__ == "__main__":
    unittest.main()
