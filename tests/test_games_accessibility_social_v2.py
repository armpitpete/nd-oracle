from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts import discovery

ROOT = Path(__file__).resolve().parents[1]
OBJECTS = ROOT / "objects"


class GamesAccessibilitySocialV2Tests(unittest.TestCase):
    def load_resource(self, object_id: str) -> dict:
        return json.loads((OBJECTS / "resources" / f"{object_id}.json").read_text(encoding="utf-8"))

    def load_question(self, object_id: str) -> dict:
        return json.loads((OBJECTS / "questions" / f"{object_id}.json").read_text(encoding="utf-8"))

    def test_steam_accessibility_route_is_declaration_not_certification(self) -> None:
        item = self.load_resource("steam-accessibility-features")
        self.assertEqual("reviewed", item["status"])
        self.assertEqual([], item["claims"])
        text = " ".join([item["audience_or_context"], *item["limitations"], *item["conflicts_of_interest"]]).casefold()
        self.assertIn("developer", text)
        self.assertIn("independently audited", text)
        self.assertIn("independent accessibility certification", text)
        self.assertNotIn("certified accessible", text)

    def test_adult_gaming_group_keeps_age_and_geography_limits(self) -> None:
        item = self.load_resource("incompatible-cartridges-gamers-group")
        self.assertEqual([], item["claims"])
        text = " ".join([item["audience_or_context"], *item["limitations"]]).casefold()
        self.assertIn("18+", text)
        self.assertIn("harrow", text)
        self.assertIn("hillingdon", text)
        self.assertIn("not a general uk", item["audience_or_context"].casefold())

    def test_low_sensory_route_remains_not_currently_answerable(self) -> None:
        item = self.load_question("low-sensory-demand-games")
        self.assertEqual("not_currently_answerable", item["status"])
        refs = {(ref["type"], ref["id"]) for ref in item["related_objects"]}
        self.assertIn(("resource", "steam-accessibility-features"), refs)
        self.assertIn("not strong enough to rank", item["current_understanding"].casefold())

    def test_social_load_route_adds_adult_option_without_hiding_scope(self) -> None:
        item = self.load_question("gaming-community-social-load")
        refs = {(ref["type"], ref["id"]) for ref in item["related_objects"]}
        self.assertIn(("resource", "incompatible-cartridges-gamers-group"), refs)
        self.assertIn("harrow or hillingdon", item["current_understanding"].casefold())
        self.assertIn("still lacks uk-wide", item["current_understanding"].casefold())

    def test_accessibility_inspection_query_routes_to_new_question(self) -> None:
        _trace, results = discovery.evaluate("check game accessibility before buying", limit=5)
        self.assertTrue(results)
        self.assertEqual("/questions/checking-game-accessibility-before-buying/", results[0].route)

    def test_adult_group_query_routes_to_scoped_information_not_recommendation(self) -> None:
        _trace, results = discovery.evaluate("adult autistic gaming group", limit=5)
        self.assertTrue(results)
        self.assertEqual("/questions/adult-autistic-gaming-communities/", results[0].route)
        item = self.load_question("adult-autistic-gaming-communities")
        self.assertIn("does not yet provide a uk-wide", item["current_understanding"].casefold())


if __name__ == "__main__":
    unittest.main()
