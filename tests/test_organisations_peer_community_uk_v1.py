from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts import build_site, discovery

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "contracts" / "organisations-peer-community-uk-v1.json"
BENCHMARK = ROOT / "benchmarks" / "organisations-peer-community-uk-v1.json"

NEW_RESOURCE_IDS = (
    "amase-autistic-mutual-aid-society-edinburgh",
    "argh-scotland",
    "people-first-self-advocacy",
    "disability-wales-full-member-dpos",
    "bda-dyslexia-charity-network",
    "bda-local-dyslexia-hubs",
    "tourettes-action-support-groups",
    "dyspraxia-foundation-local-groups",
    "dyspraxic-adults-forum",
    "autism-ni-autistic-adult-peer-networks",
    "neurodiversity-uk-events-directory",
)

NEW_QUESTION_IDS = (
    "find-neurodivergent-led-organisation",
    "how-peer-led-is-an-organisation",
    "no-local-peer-group-rural-or-travel-barriers",
    "peer-support-online-vs-in-person",
    "check-peer-group-accessibility-before-joining",
    "check-community-moderation-before-joining",
    "check-community-privacy-before-joining",
    "cross-neurodivergent-support-not-diagnosis-specific",
    "peer-support-while-awaiting-assessment",
    "leave-change-peer-group-poor-fit",
    "peer-group-no-published-rules",
    "peer-support-outside-england",
    "tourette-peer-support-online-or-local",
)

EXPECTED_GROUP = (
    "find-local-neurodivergent-peer-group",
    "online-peer-community-safety-fit",
    "parent-carer-peer-support-uk",
    *NEW_QUESTION_IDS,
)


def load_resource(object_id: str) -> dict:
    return json.loads((ROOT / "objects" / "resources" / f"{object_id}.json").read_text(encoding="utf-8"))


def load_question(object_id: str) -> dict:
    return json.loads((ROOT / "objects" / "questions" / f"{object_id}.json").read_text(encoding="utf-8"))


class OrganisationsPeerCommunityUKV1Tests(unittest.TestCase):
    def test_exact_candidate_counts_and_routes(self) -> None:
        concepts = build_site.load_concepts()
        resources = build_site.load_resources()
        questions = build_site.load_questions()
        evidence = build_site.load_evidence()
        self.assertGreaterEqual(len(concepts), 20)
        self.assertGreaterEqual(len(resources), 136)
        self.assertGreaterEqual(len(questions), 148)
        self.assertEqual(3, len(evidence))
        self.assertGreaterEqual(len(concepts) + len(resources) + len(questions) + len(evidence), 307)
        self.assertGreaterEqual(build_site.V10_ROUTE_COUNT, 391)
        self.assertEqual(build_site.V10_ROUTE_COUNT, len(build_site.sitemap_paths(concepts, resources, questions)))

    def test_new_resources_are_reviewed_reachable_and_claimless(self) -> None:
        self.assertEqual(11, len(NEW_RESOURCE_IDS))
        for object_id in NEW_RESOURCE_IDS:
            item = load_resource(object_id)
            self.assertEqual(object_id, item["id"])
            self.assertEqual("reviewed", item["status"])
            self.assertEqual("editor_reviewed", item["provenance"]["review_state"])
            self.assertEqual("2026-09-04", item["provenance"]["last_reviewed"])
            self.assertEqual([], item["claims"])
            self.assertTrue(item["limitations"])
            self.assertTrue(item["locators"])
            self.assertTrue(all(x["type"] == "url" and x["value"].startswith("https://") for x in item["locators"]))

    def test_new_questions_are_governed_and_public(self) -> None:
        self.assertEqual(13, len(NEW_QUESTION_IDS))
        paths = set(build_site.sitemap_paths(build_site.load_concepts(), build_site.load_resources(), build_site.load_questions()))
        for object_id in NEW_QUESTION_IDS:
            item = load_question(object_id)
            self.assertEqual("partially_resolved", item["status"])
            self.assertEqual("editor_reviewed", item["provenance"]["review_state"])
            self.assertTrue(item["evidence_needed"])
            self.assertTrue(item["reopening_conditions"])
            self.assertIn(f"/questions/{object_id}/", paths)
        for object_id in NEW_RESOURCE_IDS:
            self.assertIn(f"/resources/{object_id}/", paths)

    def test_question_group_is_complete_once(self) -> None:
        groups = [ids for group, ids in build_site.QUESTION_GROUPS if group == "Organisations & peer community"]
        self.assertEqual(1, len(groups))
        self.assertEqual(list(EXPECTED_GROUP), groups[0])
        self.assertEqual(len(groups[0]), len(set(groups[0])))

    def test_metadata_contract_has_all_section_resources_and_uncertainty_semantics(self) -> None:
        contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
        expected = {
            "nas-autism-services-directory",
            "adhd-uk-support-groups",
            "nas-online-community",
            *NEW_RESOURCE_IDS,
        }
        self.assertEqual(expected, set(contract["resources"]))
        self.assertTrue(contract["no_quality_or_safety_score"])
        valid_access = set(contract["accessibility_states"])
        valid_moderation = set(contract["moderation_states"])
        valid_privacy = set(contract["privacy_states"])
        for object_id, row in contract["resources"].items():
            self.assertIn(row["access"]["state"], valid_access, object_id)
            self.assertIn(row["moderation"]["state"], valid_moderation, object_id)
            self.assertIn(row["privacy"]["state"], valid_privacy, object_id)
            self.assertTrue(row["geography"]["nations"], object_id)
            self.assertTrue(row["leadership"]["note"], object_id)

    def test_peer_controlled_labels_are_evidenced_not_inferred(self) -> None:
        contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
        peer_controlled = {
            object_id
            for object_id, row in contract["resources"].items()
            if row["leadership"]["type"] == "peer_controlled"
        }
        self.assertEqual({"amase-autistic-mutual-aid-society-edinburgh", "argh-scotland"}, peer_controlled)
        self.assertEqual("user_led", contract["resources"]["people-first-self-advocacy"]["leadership"]["type"])
        self.assertEqual("dpo_membership_governed", contract["resources"]["disability-wales-full-member-dpos"]["leadership"]["type"])
        self.assertEqual("organisation_led", contract["resources"]["bda-local-dyslexia-hubs"]["leadership"]["type"])
        self.assertEqual("unclear", contract["resources"]["dyspraxic-adults-forum"]["leadership"]["type"])

    def test_four_nations_and_rural_proofs_are_explicit(self) -> None:
        contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
        proofs = contract["geographic_proofs"]
        self.assertEqual({"England", "Scotland", "Wales", "Northern Ireland"}, {x["nation"] for x in proofs})
        labels = {x["probe"] for x in proofs}
        for expected in ("York / Yorkshire", "Cumbria", "Highland", "Powys", "Fermanagh"):
            self.assertIn(expected, labels)

    def test_cross_nd_directory_conflict_and_completeness_limits_are_permanent(self) -> None:
        item = load_resource("neurodiversity-uk-events-directory")
        text = " ".join(item["limitations"] + item["conflicts_of_interest"]).lower()
        self.assertIn("self-described", text)
        self.assertIn("commercial", text)
        self.assertIn("sells", text)
        q = load_question("cross-neurodivergent-support-not-diagnosis-specific")
        self.assertIn("does not pretend", q["current_understanding"].lower())

    def test_metadata_never_turns_unknown_into_absent_or_score(self) -> None:
        contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
        self.assertIn("uncertainty", contract["state_semantics"]["not_found"].lower())
        self.assertFalse(any(
            "safe_score" in json.dumps(row).lower() or "quality_score" in json.dumps(row).lower()
            for row in contract["resources"].values()
        ))

    def test_research_evidence_is_contextual_not_universal_claim(self) -> None:
        contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
        evidence = contract["research_evidence"]
        self.assertEqual(1, len(evidence))
        self.assertEqual("contextual_not_claim_bearing", evidence[0]["status"])
        self.assertEqual("10.3389/fpsyg.2022.831628", evidence[0]["doi"])
        self.assertIn("cannot establish universal efficacy", evidence[0]["limits"])

    def test_peer_support_never_replaces_crisis_or_professional_authority(self) -> None:
        leave_text = load_question("leave-change-peer-group-poor-fit")["current_understanding"].lower()
        wait_text = load_question("peer-support-while-awaiting-assessment")["current_understanding"].lower()
        moderation_text = load_question("check-community-moderation-before-joining")["current_understanding"].lower()
        self.assertIn("emergency", leave_text)
        self.assertIn("clinical", wait_text)
        self.assertIn("not proof", moderation_text)

    def test_18_case_discovery_and_hostile_benchmark(self) -> None:
        benchmark = json.loads(BENCHMARK.read_text(encoding="utf-8"))
        self.assertEqual(18, len(benchmark["cases"]))
        for case in benchmark["cases"]:
            with self.subTest(query=case["query"]):
                trace, results = discovery.evaluate(case["query"], limit=5)
                if case["mode"] == "boundary":
                    self.assertEqual(case["expected_final_reason"], trace["final_reason"])
                    self.assertEqual([], results)
                    continue
                self.assertEqual("results", trace["final_reason"])
                routes = [result.route for result in results]
                rank = min(
                    (routes.index(route) + 1 for route in case["acceptable_routes"] if route in routes),
                    default=None,
                )
                self.assertIsNotNone(rank, f"{case['query']!r}: {routes}")
                self.assertLessEqual(rank, case["max_rank"], f"{case['query']!r}: {routes}")

    def test_current_production_pointer_preserves_verified_uk_baseline(self) -> None:
        current = json.loads((ROOT / "contracts" / "current-production.json").read_text(encoding="utf-8"))
        self.assertEqual("94d1ab0d8df5699b1316e64d70c28fe11b25b7cf", current["source_sha"])
        self.assertEqual(325, current["corpus"]["governed_objects"])
        self.assertEqual(409, current["verification"]["canonical_routes_verified"])
        self.assertEqual(
            "docs/PRODUCTION_STATE_2026-09-04_NHS_BULLETIN_PROMOTION_v1.md",
            current["production_state_document"],
        )


if __name__ == "__main__":
    unittest.main()
