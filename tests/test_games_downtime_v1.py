from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts import build_site, discovery

ROOT = Path(__file__).resolve().parents[1]
BENCHMARK = ROOT / "benchmarks" / "games-downtime-v1.json"
DOC = ROOT / "docs" / "GAMES_DOWNTIME_FACETS_v1.md"
NEW_GAME_IDS = {
    "tiny-glade", "townscaper", "summerhouse-game", "gourdlets",
    "the-shape-of-things", "cats-organized-neatly", "garden-galaxy", "dorfromantik",
    "minami-lane", "cloud-gardens",
}
NEW_QUESTION_IDS = {
    "low-reaction-demand-games", "easy-to-interrupt-games",
    "configurable-game-pressure", "simple-control-games",
    "low-consequence-games", "solo-low-social-pressure-games",
    "building-sorting-collecting-games", "gaming-community-social-load",
    "low-sensory-demand-games",
}


class GamesDowntimeV1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.resources = {item["id"]: item for item in build_site.load_resources()}
        cls.questions = {item["id"]: item for item in build_site.load_questions()}
        cls.index = discovery.build_index()
        cls.benchmark = json.loads(BENCHMARK.read_text(encoding="utf-8"))["cases"]

    def test_expanded_game_catalogue_is_non_claim_bearing_and_reachable(self) -> None:
        self.assertTrue(NEW_GAME_IDS <= self.resources.keys())
        for game_id in NEW_GAME_IDS:
            item = self.resources[game_id]
            self.assertEqual("game", item["category"])
            self.assertEqual([], item["claims"])
            self.assertTrue(item["limitations"])
            self.assertTrue(item["locators"])
            self.assertTrue(all(locator["type"] != "url" or locator["value"].startswith("https://") for locator in item["locators"]))

    def test_games_group_contains_every_new_need_route_once(self) -> None:
        games_ids = None
        for group, ids in build_site.QUESTION_GROUPS:
            if group == "Games & downtime":
                games_ids = ids
                break
        self.assertIsNotNone(games_ids)
        self.assertTrue(NEW_QUESTION_IDS <= set(games_ids))
        self.assertEqual(len(games_ids), len(set(games_ids)))

    def test_facets_document_keeps_diagnosis_and_cozy_boundaries_explicit(self) -> None:
        text = DOC.read_text(encoding="utf-8").casefold()
        for phrase in ("user tags", "not endorsement", "diagnostic evidence", "cozy", "sensory demand", "social demand"):
            self.assertIn(phrase, text)

    def test_bounded_discovery_cases_route_to_expected_question(self) -> None:
        failures = []
        for case in self.benchmark:
            _trace, results = discovery.evaluate(case["query"], limit=5, index=self.index)
            actual = results[0].route if results else None
            if actual != case["expected_top"]:
                failures.append((case["query"], actual, case["expected_top"]))
        self.assertEqual([], failures)

    def test_diagnosis_wording_does_not_become_a_game_prescription(self) -> None:
        for query in ("best game for autism", "game for my adhd", "which calming game should an autistic person play"):
            _trace, results = discovery.evaluate(query, limit=5, index=self.index)
            if results:
                self.assertFalse(results[0].route.startswith("/questions/low-time-pressure-games/"), query)
                self.assertFalse(results[0].route.startswith("/questions/low-consequence-games/"), query)


if __name__ == "__main__":
    unittest.main()
