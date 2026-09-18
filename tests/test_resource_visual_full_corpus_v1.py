from __future__ import annotations

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
        self.assertEqual(1, sum(entry["status"] == "cleared" for entry in entries))
        self.assertEqual(28, sum(entry["status"] == "permission-required" for entry in entries))
        self.assertEqual(8, sum(entry["status"] == "rights-unknown" for entry in entries))

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


if __name__ == "__main__":
    unittest.main()
