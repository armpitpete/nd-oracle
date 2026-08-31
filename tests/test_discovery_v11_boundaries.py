from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "discovery" / "routing-policy-v1.1.json"
BROWSER = ROOT / "scripts" / "discovery_browser.js"


def reject_duplicate_pairs(pairs):
    output = {}
    for key, value in pairs:
        if key in output:
            raise ValueError(f"duplicate JSON key: {key}")
        output[key] = value
    return output


class DiscoveryV11BoundaryTests(unittest.TestCase):
    def test_policy_json_contains_no_duplicate_keys(self) -> None:
        parsed = json.loads(POLICY.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicate_pairs)
        self.assertEqual("1.1", parsed["version"])
        self.assertFalse(parsed["orientation"]["enabled"])
        self.assertEqual(29, len(parsed["scope_provenance"]["routes"]))

    def test_browser_discovery_has_no_network_or_query_storage_authority(self) -> None:
        source = BROWSER.read_text(encoding="utf-8")
        forbidden = (
            "fetch(",
            "XMLHttpRequest",
            "sendBeacon",
            "localStorage",
            "sessionStorage",
            "indexedDB",
            "WebSocket",
        )
        hits = [token for token in forbidden if token in source]
        self.assertEqual([], hits)


if __name__ == "__main__":
    unittest.main()
