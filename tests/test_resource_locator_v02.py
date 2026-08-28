from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.validate import load_schema_validators

ROOT = Path(__file__).resolve().parents[1]
RESOURCE_FIXTURE = ROOT / "tests" / "fixtures" / "v0.2" / "resources" / "fixture-resource.json"


class ResourceLocatorV02Tests(unittest.TestCase):
    def setUp(self) -> None:
        validators, errors = load_schema_validators(ROOT)
        self.assertEqual([], errors)
        self.validator = validators["0.2"]
        self.resource = json.loads(RESOURCE_FIXTURE.read_text(encoding="utf-8"))

    def test_resource_requires_at_least_one_access_locator(self) -> None:
        self.resource.pop("locators")
        self.assertTrue(list(self.validator.iter_errors(self.resource)))

    def test_resource_url_locator_must_be_https(self) -> None:
        self.resource["locators"] = [{"type": "url", "value": "http://example.org/resource"}]
        self.assertTrue(list(self.validator.iter_errors(self.resource)))

    def test_resource_accepts_https_access_locator(self) -> None:
        self.assertEqual([], list(self.validator.iter_errors(self.resource)))


if __name__ == "__main__":
    unittest.main()
