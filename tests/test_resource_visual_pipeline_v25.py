from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path

from scripts import resource_visuals

ROOT = Path(__file__).resolve().parents[1]


class ResourceVisualPipelineTests(unittest.TestCase):
    def _fixture_root(self) -> tuple[tempfile.TemporaryDirectory, Path, dict, list[dict]]:
        temp = tempfile.TemporaryDirectory()
        root = Path(temp.name)
        media = root / "site" / "resource-media"
        media.mkdir(parents=True)
        shutil.copy2(ROOT / "tests" / "fixtures" / "resource-visual-cleared.svg", media / "demo.svg")
        resource = {"id": "demo-resource", "category": "book", "name": "Demo Resource"}
        entry = {
            "resource_id": "demo-resource",
            "kind": "book",
            "status": "cleared",
            "materially_helpful": True,
            "helps": ["recognise", "distinguish"],
            "usefulness_note": "The fixture proves the positive publication path.",
            "source_url": "https://example.org/demo-resource",
            "rights_holder": "ND Oracle test fixture",
            "rights_basis": "Fixture created for ND Oracle automated testing; not a public product image.",
            "local_path": "site/resource-media/demo.svg",
            "alt": "Demo Resource test visual",
            "attribution": "ND Oracle test fixture",
            "checked_on": "2026-09-16",
            "rights_note": "Synthetic test fixture only.",
        }
        registry = {
            "schema_version": "2",
            "policy": "docs/RESOURCE_VISUAL_ASSET_POLICY_v1.md",
            "render_rule": "test",
            "entries": {"demo-resource": entry},
        }
        return temp, root, registry, [resource]

    def test_cleared_useful_visual_renders_and_publishes_locally(self) -> None:
        temp, root, registry, resources = self._fixture_root()
        self.addCleanup(temp.cleanup)
        resource_visuals.validate_registry(registry, resources, root=root)
        html = resource_visuals.render_resource_visual(resources[0], registry=registry, root=root)
        self.assertIn('class="resource-visual"', html)
        self.assertIn('src="/resource-media/demo.svg"', html)
        self.assertIn('alt="Demo Resource test visual"', html)
        self.assertIn('ND Oracle test fixture', html)
        with tempfile.TemporaryDirectory() as output:
            copied = resource_visuals.publish_resource_visual_assets(Path(output), resources, registry=registry, root=root)
            self.assertEqual(len(copied), 1)
            self.assertTrue((Path(output) / "resource-media" / "demo.svg").is_file())

    def test_noncleared_and_not_useful_entries_never_render(self) -> None:
        for status, helpful in (("permission-required", True), ("rights-unknown", True), ("not-useful", False)):
            with self.subTest(status=status):
                resource = {"id": "demo-resource", "category": "book", "name": "Demo Resource"}
                entry = {
                    "resource_id": "demo-resource", "kind": "book", "status": status,
                    "materially_helpful": helpful, "helps": ["recognise"] if helpful else [],
                    "usefulness_note": "test", "source_url": "https://example.org/demo" if helpful else None,
                    "rights_holder": None, "rights_basis": None, "local_path": None, "alt": None,
                    "attribution": None, "checked_on": "2026-09-16", "rights_note": "test",
                }
                registry = {"schema_version": "2", "policy": "docs/RESOURCE_VISUAL_ASSET_POLICY_v1.md", "render_rule": "test", "entries": {"demo-resource": entry}}
                resource_visuals.validate_registry(registry, [resource])
                self.assertEqual(resource_visuals.render_resource_visual(resource, registry=registry), "")

    def test_cleared_visual_fails_closed_on_missing_requirements(self) -> None:
        temp, root, registry, resources = self._fixture_root()
        self.addCleanup(temp.cleanup)
        for field in ("alt", "source_url", "rights_basis"):
            with self.subTest(field=field):
                broken = json.loads(json.dumps(registry))
                broken["entries"]["demo-resource"][field] = None
                with self.assertRaises(ValueError):
                    resource_visuals.validate_registry(broken, resources, root=root)
        missing = json.loads(json.dumps(registry))
        missing["entries"]["demo-resource"]["local_path"] = "site/resource-media/missing.svg"
        with self.assertRaises(ValueError):
            resource_visuals.validate_registry(missing, resources, root=root)
        external = json.loads(json.dumps(registry))
        external["entries"]["demo-resource"]["local_path"] = "https://example.org/demo.svg"
        with self.assertRaises(ValueError):
            resource_visuals.validate_registry(external, resources, root=root)

    def test_actual_registry_is_schema_v2_and_p1_only(self) -> None:
        registry = resource_visuals.load_registry()
        resources = []
        for path in sorted((ROOT / "objects" / "resources").glob("*.json")):
            resources.append(json.loads(path.read_text(encoding="utf-8")))
        resource_visuals.validate_registry(registry, resources)
        resource_map = {item["id"]: item for item in resources}
        self.assertTrue(registry["entries"])
        for rid, entry in registry["entries"].items():
            self.assertIn(resource_map[rid]["category"], {"book", "game", "app", "media"})
            self.assertTrue(entry["materially_helpful"])
            self.assertTrue(entry["helps"])

    def test_builder_wires_registry_render_and_asset_publication(self) -> None:
        source = (ROOT / "scripts" / "build_site.py").read_text(encoding="utf-8")
        self.assertIn("_resource_visuals.render_resource_visual(resource)", source)
        self.assertIn("_resource_visuals.publish_resource_visual_assets(destination, resources)", source)
        self.assertIn("from scripts import resource_visuals as _resource_visuals", source)


if __name__ == "__main__":
    unittest.main()
