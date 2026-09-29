from __future__ import annotations

import hashlib
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from scripts import resource_visuals

ROOT = Path(__file__).resolve().parents[1]


def load_resources() -> list[dict]:
    return [
        json.loads(path.read_text(encoding="utf-8"))
        for path in sorted((ROOT / "objects" / "resources").glob("*.json"))
    ]


class ResourceVisualFullCorpusTests(unittest.TestCase):
    def test_every_governed_resource_has_an_explicit_visual_state(self) -> None:
        resources = load_resources()
        registry = resource_visuals.load_registry()
        resource_visuals.validate_registry(registry, resources, require_complete=True)
        self.assertEqual({item["id"] for item in resources}, set(registry["entries"]))

    def test_missing_resource_entry_fails_complete_validation(self) -> None:
        resources = load_resources()
        registry = resource_visuals.load_registry()
        broken = json.loads(json.dumps(registry))
        broken["entries"].pop(next(iter(broken["entries"])))
        with self.assertRaisesRegex(ValueError, "registry is incomplete"):
            resource_visuals.validate_registry(broken, resources, require_complete=True)

    def test_rights_queue_and_usefulness_counts_are_frozen(self) -> None:
        registry = resource_visuals.load_registry()
        entries = list(registry["entries"].values())
        self.assertEqual(37, sum(bool(entry["materially_helpful"]) for entry in entries))
        self.assertEqual(131, sum(entry["status"] == "not-useful" for entry in entries))
        self.assertEqual(6, sum(entry["status"] == "cleared" for entry in entries))
        self.assertEqual(25, sum(entry["status"] == "permission-required" for entry in entries))
        self.assertEqual(6, sum(entry["status"] == "rights-unknown" for entry in entries))

    def test_a_kind_of_spark_permission_and_exact_asset_are_frozen(self) -> None:
        registry = resource_visuals.load_registry()
        entry = registry["entries"]["a-kind-of-spark"]
        self.assertEqual("cleared", entry["status"])
        self.assertEqual("cleared-written-permission-exact-attached-cover-unaltered", entry["rights_research_state"])
        self.assertIn("must remain byte-for-byte unaltered", entry["rights_note"])
        self.assertIn("future editorial change", entry["rights_note"])
        asset = ROOT / entry["local_path"]
        raw = asset.read_bytes()
        self.assertEqual(1478012, len(raw))
        self.assertEqual(
            "483dc7fd0daa8bc473b449c298737e943a717a3e544f2bd48650d272f021d7d7",
            hashlib.sha256(raw).hexdigest(),
        )

    def test_different_not_less_permission_and_exact_asset_are_frozen(self) -> None:
        registry = resource_visuals.load_registry()
        entry = registry["entries"]["different-not-less"]
        self.assertEqual("cleared", entry["status"])
        self.assertEqual("cleared-written-permission-exact-attached-cover", entry["rights_research_state"])
        self.assertTrue(entry["attribution_required"])
        self.assertEqual("Different, Not Less by Chloé Hayden, published by Murdoch Books.", entry["attribution"])
        asset = ROOT / entry["local_path"]
        raw = asset.read_bytes()
        self.assertEqual(1423161, len(raw))
        self.assertEqual(
            "42e4d6f1ba06ea92d6043ba4f93cc3f982d3fa3ae6937e285fd956caeb9279fd",
            hashlib.sha256(raw).hexdigest(),
        )

    def test_corrupt_cleared_asset_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            media = root / "site" / "resource-media"
            media.mkdir(parents=True)
            (media / "bad.png").write_bytes(b"not a png")
            resource = {"id": "demo", "category": "book", "name": "Demo"}
            registry = {
                "schema_version": "2",
                "policy": "docs/RESOURCE_VISUAL_ASSET_POLICY_v1.md",
                "entries": {
                    "demo": {
                        "resource_id": "demo", "kind": "book", "status": "cleared",
                        "materially_helpful": True, "helps": ["recognise"],
                        "usefulness_note": "test", "source_url": "https://example.org/demo",
                        "rights_holder": "Fixture", "rights_basis": "Fixture permission",
                        "local_path": "site/resource-media/bad.png", "alt": "Demo",
                        "attribution": None, "attribution_required": False,
                        "checked_on": "2026-09-18", "rights_note": "test",
                    }
                },
            }
            with self.assertRaisesRegex(ValueError, "invalid file signature"):
                resource_visuals.validate_registry(registry, [resource], root=root)

    def test_required_attribution_fails_closed_when_missing(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            media = root / "site" / "resource-media"
            media.mkdir(parents=True)
            shutil.copy2(ROOT / "tests" / "fixtures" / "resource-visual-cleared.svg", media / "demo.svg")
            resource = {"id": "demo", "category": "book", "name": "Demo"}
            registry = {
                "schema_version": "2",
                "policy": "docs/RESOURCE_VISUAL_ASSET_POLICY_v1.md",
                "entries": {
                    "demo": {
                        "resource_id": "demo", "kind": "book", "status": "cleared",
                        "materially_helpful": True, "helps": ["recognise"],
                        "usefulness_note": "test", "source_url": "https://example.org/demo",
                        "rights_holder": "Fixture", "rights_basis": "Fixture permission",
                        "local_path": "site/resource-media/demo.svg", "alt": "Demo",
                        "attribution": None, "attribution_required": True,
                        "checked_on": "2026-09-18", "rights_note": "test",
                    }
                },
            }
            with self.assertRaisesRegex(ValueError, "requires attribution"):
                resource_visuals.validate_registry(registry, [resource], root=root)


    def test_required_attribution_link_fails_closed_when_missing(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            media = root / "site" / "resource-media"
            media.mkdir(parents=True)
            shutil.copy2(ROOT / "tests" / "fixtures" / "resource-visual-cleared.svg", media / "demo.svg")
            resource = {"id": "demo", "category": "app", "name": "Demo"}
            registry = {
                "schema_version": "2",
                "policy": "docs/RESOURCE_VISUAL_ASSET_POLICY_v1.md",
                "entries": {
                    "demo": {
                        "resource_id": "demo", "kind": "app", "status": "cleared",
                        "materially_helpful": True, "helps": ["recognise"],
                        "usefulness_note": "test", "source_url": "https://example.org/demo",
                        "rights_holder": "Fixture", "rights_basis": "Fixture permission",
                        "local_path": "site/resource-media/demo.svg", "alt": "Demo",
                        "attribution": "Fixture", "attribution_required": True,
                        "attribution_url_required": True,
                        "checked_on": "2026-09-19", "rights_note": "test",
                    }
                },
            }
            with self.assertRaisesRegex(ValueError, "requires a linked attribution URL"):
                resource_visuals.validate_registry(registry, [resource], root=root)

    def test_linked_attribution_renders_as_a_safe_link(self) -> None:
        resource = {"id": "demo", "category": "app", "name": "Demo"}
        registry = {
            "entries": {
                "demo": {
                    "resource_id": "demo",
                    "status": "cleared",
                    "materially_helpful": True,
                    "local_path": "site/resource-media/demo.png",
                    "alt": "Demo logo.",
                    "attribution": "Demo",
                    "attribution_url": "https://example.org/",
                }
            }
        }
        rendered = resource_visuals.render_resource_visual(resource, registry=registry)
        self.assertIn('<figcaption><a href="https://example.org/">Demo</a></figcaption>', rendered)


if __name__ == "__main__":
    unittest.main()
