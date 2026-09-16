from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TODAY = "2026-09-16"


def replace_once(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    if old not in text:
        raise SystemExit(f"marker not found in {path}: {old[:100]!r}")
    if text.count(old) != 1:
        raise SystemExit(f"marker not unique in {path}: {text.count(old)} occurrences")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


def write_resource_visuals_module() -> None:
    content = r'''from __future__ import annotations

import html
import json
import shutil
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "site" / "resource-visuals.json"
MEDIA_DIR = ROOT / "site" / "resource-media"
ALLOWED_STATUSES = {"cleared", "permission-required", "rights-unknown", "not-useful"}
USEFUL_REASONS = {"recognise", "distinguish", "understand"}
ALLOWED_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp", ".svg"}
MAX_ASSET_BYTES = 1_500_000


def load_registry(path: Path = REGISTRY_PATH) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _safe_source_url(value: object) -> bool:
    if not isinstance(value, str):
        return False
    parsed = urlsplit(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def should_render(entry: dict) -> bool:
    return bool(entry.get("materially_helpful")) and entry.get("status") == "cleared"


def _asset_path(entry: dict, *, root: Path) -> Path:
    raw = entry.get("local_path")
    if not isinstance(raw, str) or not raw.startswith("site/resource-media/"):
        raise ValueError("cleared visual local_path must be under site/resource-media/")
    candidate = (root / raw).resolve()
    media_root = (root / "site" / "resource-media").resolve()
    try:
        candidate.relative_to(media_root)
    except ValueError as exc:
        raise ValueError("resource visual local_path escapes site/resource-media") from exc
    return candidate


def validate_registry(registry: dict, resources: list[dict], *, root: Path = ROOT) -> dict:
    if registry.get("schema_version") != "2":
        raise ValueError("resource visual registry must use schema_version 2")
    if registry.get("policy") != "docs/RESOURCE_VISUAL_ASSET_POLICY_v1.md":
        raise ValueError("resource visual registry policy pointer is invalid")
    entries = registry.get("entries")
    if not isinstance(entries, dict):
        raise ValueError("resource visual registry entries must be an object")

    resource_map = {item["id"]: item for item in resources}
    for resource_id, entry in entries.items():
        if resource_id not in resource_map:
            raise ValueError(f"resource visual registry contains orphan Resource ID: {resource_id}")
        if entry.get("resource_id") != resource_id:
            raise ValueError(f"{resource_id}: resource_id field must match registry key")
        if entry.get("kind") != resource_map[resource_id].get("category"):
            raise ValueError(f"{resource_id}: visual kind must match governed Resource category")

        status = entry.get("status")
        if status not in ALLOWED_STATUSES:
            raise ValueError(f"{resource_id}: invalid visual status {status!r}")
        materially_helpful = entry.get("materially_helpful")
        if not isinstance(materially_helpful, bool):
            raise ValueError(f"{resource_id}: materially_helpful must be boolean")
        reasons = entry.get("helps")
        if not isinstance(reasons, list) or any(reason not in USEFUL_REASONS for reason in reasons):
            raise ValueError(f"{resource_id}: helps must contain only recognise/distinguish/understand")
        if materially_helpful and not reasons:
            raise ValueError(f"{resource_id}: a useful visual needs at least one usefulness reason")
        if not materially_helpful and reasons:
            raise ValueError(f"{resource_id}: non-useful visual cannot carry usefulness reasons")
        if status == "not-useful" and materially_helpful:
            raise ValueError(f"{resource_id}: not-useful cannot be materially helpful")
        if status != "not-useful" and not materially_helpful:
            raise ValueError(f"{resource_id}: useful visual candidates must be materially helpful or use not-useful")

        if should_render(entry):
            for field in ("alt", "source_url", "rights_basis", "checked_on"):
                if not entry.get(field):
                    raise ValueError(f"{resource_id}: cleared visual missing {field}")
            if not _safe_source_url(entry.get("source_url")):
                raise ValueError(f"{resource_id}: cleared visual source_url must be safe http(s)")
            asset = _asset_path(entry, root=root)
            if not asset.is_file():
                raise ValueError(f"{resource_id}: cleared visual local file does not exist: {asset}")
            if asset.suffix.casefold() not in ALLOWED_SUFFIXES:
                raise ValueError(f"{resource_id}: unsupported visual format {asset.suffix}")
            if asset.stat().st_size > MAX_ASSET_BYTES:
                raise ValueError(f"{resource_id}: visual exceeds {MAX_ASSET_BYTES} bytes")
        else:
            if entry.get("local_path") is not None:
                raise ValueError(f"{resource_id}: uncleared/non-useful visual must not store a publishable local_path")
            if entry.get("alt") is not None:
                raise ValueError(f"{resource_id}: uncleared/non-useful visual must not publish alt text")
            if entry.get("rights_basis") is not None:
                raise ValueError(f"{resource_id}: uncleared/non-useful visual must not claim a rights basis")
    return registry


def render_resource_visual(resource: dict, *, registry: dict | None = None, root: Path = ROOT) -> str:
    if registry is None:
        registry = load_registry()
    entry = registry.get("entries", {}).get(resource["id"])
    if not entry or not should_render(entry):
        return ""
    validate_registry(registry, [resource], root=root)
    local_path = entry["local_path"]
    public_path = "/" + local_path.removeprefix("site/")
    attribution = entry.get("attribution")
    caption = f"<figcaption>{html.escape(str(attribution))}</figcaption>" if attribution else ""
    return (
        '<figure class="resource-visual" aria-label="Resource recognition visual">'
        f'<img src="{html.escape(public_path, quote=True)}" alt="{html.escape(entry["alt"], quote=True)}" decoding="async">'
        f"{caption}</figure>"
    )


def publish_resource_visual_assets(destination: Path, resources: list[dict], *, registry: dict | None = None, root: Path = ROOT) -> list[Path]:
    if registry is None:
        registry = load_registry()
    validate_registry(registry, resources, root=root)
    copied: list[Path] = []
    for entry in registry["entries"].values():
        if not should_render(entry):
            continue
        source = _asset_path(entry, root=root)
        target_dir = destination / "resource-media"
        target_dir.mkdir(parents=True, exist_ok=True)
        target = target_dir / source.name
        shutil.copy2(source, target)
        copied.append(target)
    return copied
'''
    (ROOT / "scripts" / "resource_visuals.py").write_text(content, encoding="utf-8")


def patch_builder() -> None:
    path = ROOT / "scripts" / "build_site.py"
    text = path.read_text(encoding="utf-8")
    import_old = "from scripts import discovery\n"
    import_new = "from scripts import discovery\nfrom scripts import resource_visuals as _resource_visuals\n"
    if import_new not in text:
        if text.count(import_old) != 1:
            raise SystemExit("build_site discovery import marker missing/non-unique")
        text = text.replace(import_old, import_new, 1)

    old = '''def render_resource(resource: dict, concept_map: dict[str, dict], questions: list[dict], evidence_map: dict[str, dict] | None=None) -> str:\n    page = _compat09__render_resource(resource, concept_map, questions)\n    if evidence_map is None:\n        evidence_map = {item['id']: item for item in load_evidence()}\n    claims = render_governed_resource_claims(resource, evidence_map)\n    if claims:\n        marker = '<section aria-labelledby="limits-heading">'\n        if marker not in page:\n            raise ValueError(f"{resource['id']}: cannot locate limits section for governed claims")\n        page = page.replace(marker, claims + marker, 1)\n    return page\n'''
    new = '''def render_resource(resource: dict, concept_map: dict[str, dict], questions: list[dict], evidence_map: dict[str, dict] | None=None) -> str:\n    page = _compat09__render_resource(resource, concept_map, questions)\n    visual = _resource_visuals.render_resource_visual(resource)\n    if visual:\n        marker = '<section class="notice"><strong>Listed, not endorsed.</strong>'\n        if marker not in page:\n            raise ValueError(f"{resource['id']}: cannot locate resource boundary for recognition visual")\n        page = page.replace(marker, visual + marker, 1)\n    if evidence_map is None:\n        evidence_map = {item['id']: item for item in load_evidence()}\n    claims = render_governed_resource_claims(resource, evidence_map)\n    if claims:\n        marker = '<section aria-labelledby="limits-heading">'\n        if marker not in page:\n            raise ValueError(f"{resource['id']}: cannot locate limits section for governed claims")\n        page = page.replace(marker, claims + marker, 1)\n    return page\n'''
    if new not in text:
        if text.count(old) != 1:
            raise SystemExit("render_resource marker missing/non-unique")
        text = text.replace(old, new, 1)

    old_build = '''    resources = _compat06__load_resources()\n    evidence = load_evidence()\n    concept_map = {item['id']: item for item in concepts}\n'''
    new_build = '''    resources = _compat06__load_resources()\n    evidence = load_evidence()\n    _resource_visuals.publish_resource_visual_assets(destination, resources)\n    concept_map = {item['id']: item for item in concepts}\n'''
    if new_build not in text:
        if text.count(old_build) != 1:
            raise SystemExit("final build resource marker missing/non-unique")
        text = text.replace(old_build, new_build, 1)
    path.write_text(text, encoding="utf-8")


def update_policy() -> None:
    path = ROOT / "docs" / "RESOURCE_VISUAL_ASSET_POLICY_v1.md"
    text = path.read_text(encoding="utf-8")
    old = "ND Oracle therefore treats product imagery as an accessibility/navigation aid when it can lawfully publish the asset.\n\nThe image is **recognition material, not evidence**. It must never imply endorsement, efficacy, safety, suitability or a stronger evidence status."
    new = "ND Oracle therefore treats product imagery as an accessibility/navigation aid when it can lawfully publish the asset.\n\n**Canonical usefulness rule:** **Render a cleared visual when it materially helps the user recognise, distinguish or understand the resource.**\n\nUsefulness is the first gate. Finding an image, owning a local copy or having permission does not by itself justify displaying it. A visual that does not materially help is recorded as `not-useful` and stays absent.\n\nThe image is **recognition material, not evidence**. It must never imply endorsement, efficacy, safety, suitability or a stronger evidence status."
    if old not in text:
        raise SystemExit("policy purpose marker missing")
    text = text.replace(old, new, 1)
    old2 = "Only `cleared` may render."
    new2 = "Only `cleared` may render, and only when `materially_helpful` is true with one or more recorded usefulness reasons: `recognise`, `distinguish`, or `understand`. Rendering is derived from those fields; the registry does not contain an independent `render` switch."
    if old2 not in text:
        raise SystemExit("policy status marker missing")
    text = text.replace(old2, new2, 1)
    insertion = """
## Asset format and size boundary

Publishable local assets are limited to PNG, JPEG, WebP and SVG. A single source asset must be no larger than 1.5 MB. Presentation CSS preserves the useful source aspect ratio rather than forcing every resource into a square thumbnail. Cropping must not remove identifying information such as a book title, game identity or app mark.

The source file remains local under `site/resource-media/`; the generated public path is `/resource-media/<filename>`. Remote image URLs are provenance only and are never used as the rendered image source.
"""
    marker = "## Prohibited shortcuts\n"
    if insertion.strip() not in text:
        if marker not in text:
            raise SystemExit("policy prohibited marker missing")
        text = text.replace(marker, insertion + "\n" + marker, 1)
    path.write_text(text, encoding="utf-8")


def update_design_system() -> None:
    path = ROOT / "docs" / "ND_UX_V2_5_DESIGN_SYSTEM.md"
    text = path.read_text(encoding="utf-8")
    old = "For recognisable resources such as books, games, apps, films, physical products and other media, a useful product visual should normally be shown when ND Oracle has a lawful asset to publish."
    new = "**Render a cleared visual when it materially helps the user recognise, distinguish or understand the resource.** This usefulness gate comes before publication: a lawful asset is not displayed merely because it exists."
    if old not in text:
        raise SystemExit("design-system visual marker missing")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


def first_resource_url(resource: dict) -> str | None:
    for locator in resource.get("locators", []):
        if locator.get("type") == "url" and isinstance(locator.get("value"), str):
            return locator["value"]
    return None


def build_registry_and_inventory() -> None:
    resources = []
    for path in sorted((ROOT / "objects" / "resources").glob("*.json")):
        resources.append(json.loads(path.read_text(encoding="utf-8")))
    old = json.loads((ROOT / "site" / "resource-visuals.json").read_text(encoding="utf-8"))
    old_entries = old.get("entries", {})
    p1 = {"book", "game", "app", "media"}
    notes = {
        "book": "A cover normally helps a reader recognise and distinguish the exact book.",
        "game": "Box/key art normally helps a reader recognise and distinguish the exact game.",
        "app": "An official app/product visual normally helps a reader recognise the exact software.",
        "media": "A poster, programme, podcast or other official media visual normally helps recognition.",
    }
    entries = {}
    for resource in resources:
        if resource.get("category") not in p1:
            continue
        rid = resource["id"]
        prior = old_entries.get(rid, {})
        entry = {
            "resource_id": rid,
            "kind": resource["category"],
            "status": prior.get("status", "rights-unknown"),
            "materially_helpful": True,
            "helps": ["recognise", "distinguish"],
            "usefulness_note": notes[resource["category"]],
            "source_url": prior.get("source_url") or first_resource_url(resource),
            "rights_holder": prior.get("rights_holder"),
            "rights_basis": prior.get("rights_basis"),
            "local_path": prior.get("local_path"),
            "alt": prior.get("alt"),
            "attribution": prior.get("attribution"),
            "checked_on": prior.get("checked_on") or TODAY,
            "rights_note": prior.get("note") or prior.get("rights_note") or "No explicit republication licence or permission has yet been recorded in ND Oracle; fail closed until one is reviewed.",
        }
        if entry["status"] != "cleared":
            entry["rights_basis"] = None
            entry["local_path"] = None
            entry["alt"] = None
            entry["attribution"] = None
        entries[rid] = entry
    registry = {
        "schema_version": "2",
        "policy": "docs/RESOURCE_VISUAL_ASSET_POLICY_v1.md",
        "render_rule": "Render a cleared visual when it materially helps the user recognise, distinguish or understand the resource; rendering is derived from usefulness + cleared status + valid local rights/provenance metadata.",
        "entries": entries,
    }
    (ROOT / "site" / "resource-visuals.json").write_text(json.dumps(registry, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    grouped = {key: [] for key in ("book", "game", "app", "media")}
    for resource in resources:
        if resource.get("category") in grouped:
            grouped[resource["category"]].append(resource)
    lines = [
        "# Resource visual inventory v1",
        "",
        f"Date: {TODAY}",
        "Status: bounded P1 usefulness and rights triage",
        "",
        "## Rule",
        "",
        "**Render a cleared visual when it materially helps the user recognise, distinguish or understand the resource.**",
        "",
        "This inventory applies the usefulness gate to the highest-value recognition classes first. It does not treat an image as evidence or infer publication rights from availability on the web.",
        "",
        "## Priority-1 scope",
        "",
        f"- Books: {len(grouped['book'])}",
        f"- Games: {len(grouped['game'])}",
        f"- Apps: {len(grouped['app'])}",
        f"- Media: {len(grouped['media'])}",
        f"- Total P1 visual candidates: {sum(len(v) for v in grouped.values())}",
        "",
        "All P1 items pass the usefulness gate because their cover/icon/key-art/poster identity normally helps recognition or distinction. Publication remains fail-closed until an explicit rights basis is recorded.",
        "",
    ]
    for category, title in (("book", "Books"), ("game", "Games"), ("app", "Apps"), ("media", "Media")):
        lines += [f"## {title}", "", "| Resource | ID | Rights state | Provenance starting point |", "| --- | --- | --- | --- |"]
        for item in sorted(grouped[category], key=lambda r: r["name"].casefold()):
            entry = entries[item["id"]]
            url = entry.get("source_url") or "not recorded"
            lines.append(f"| {item['name'].replace('|', '/')} | `{item['id']}` | `{entry['status']}` | {url} |")
        lines.append("")
    lines += [
        "## Non-P1 default",
        "",
        "Organisations, ordinary services, Questions, Concepts and Evidence records do not receive visuals by default. Tools, physical products, podcasts and distinctive reports can be promoted into a later tranche only when the same usefulness test is satisfied.",
        "",
        "## Rights boundary",
        "",
        "`rights-unknown` and `permission-required` are completed triage outcomes, not permission to copy or hotlink. A later rights review may move an entry to `cleared`; otherwise the text Resource remains complete without imagery.",
    ]
    (ROOT / "docs" / "RESOURCE_VISUAL_INVENTORY_v1.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_tests() -> None:
    fixture_dir = ROOT / "tests" / "fixtures"
    fixture_dir.mkdir(parents=True, exist_ok=True)
    (fixture_dir / "resource-visual-cleared.svg").write_text('''<svg xmlns="http://www.w3.org/2000/svg" width="240" height="160" viewBox="0 0 240 160" role="img" aria-labelledby="t"><title id="t">ND Oracle resource visual test fixture</title><rect width="240" height="160" fill="#eeeeee"/><text x="24" y="84" font-family="sans-serif" font-size="18">Test fixture</text></svg>\n''', encoding="utf-8")
    content = r'''from __future__ import annotations

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
'''
    (ROOT / "tests" / "test_resource_visual_pipeline_v25.py").write_text(content, encoding="utf-8")

    existing = ROOT / "tests" / "test_resource_visual_hierarchy_v25.py"
    text = existing.read_text(encoding="utf-8")
    start = text.index("def test_resource_visual_registry_fails_closed_by_policy()")
    replacement = '''def test_resource_visual_registry_fails_closed_by_policy() -> None:\n    registry = json.loads(VISUALS.read_text(encoding="utf-8"))\n    assert registry["schema_version"] == "2"\n    assert registry["policy"] == "docs/RESOURCE_VISUAL_ASSET_POLICY_v1.md"\n    assert "materially helps the user recognise, distinguish or understand" in registry["render_rule"]\n    for resource_id, entry in registry["entries"].items():\n        assert entry["resource_id"] == resource_id\n        assert "render" not in entry\n        assert isinstance(entry["materially_helpful"], bool)\n        assert set(entry["helps"]) <= {"recognise", "distinguish", "understand"}\n        if entry["status"] == "cleared":\n            assert entry["materially_helpful"]\n            assert entry["local_path"].startswith("site/resource-media/")\n            assert entry["alt"]\n            assert entry["source_url"]\n            assert entry["rights_basis"]\n            assert (ROOT / entry["local_path"]).is_file()\n        else:\n            assert entry["local_path"] is None\n            assert entry["rights_basis"] is None\n\n\ndef test_stardew_visual_is_not_fabricated_or_hotlinked_without_rights() -> None:\n    registry = json.loads(VISUALS.read_text(encoding="utf-8"))\n    stardew = registry["entries"]["stardew-valley"]\n    assert stardew["status"] == "permission-required"\n    assert stardew["materially_helpful"] is True\n    assert stardew["local_path"] is None\n    assert "stardewvalley.net/terms" in stardew["source_url"]\n\n    policy = POLICY.read_text(encoding="utf-8")\n    assert "hotlink third-party covers" in policy\n    assert "create a lookalike image and present it as the product" in policy\n    assert "recognition material, not evidence" in policy\n    assert "Render a cleared visual when it materially helps the user recognise, distinguish or understand the resource." in policy\n'''
    # replace from first registry test through EOF (these are the final two tests in the file)
    existing.write_text(text[:start] + replacement, encoding="utf-8")


def update_completion_register() -> None:
    path = ROOT / "docs" / "V2_PUBLIC_BASELINE_COMPLETION.md"
    text = path.read_text(encoding="utf-8")
    marker = "- [x] add regression coverage for resource hierarchy/grouping and visual-rights fail-closed behaviour."
    addition = marker + "\n- [x] freeze the canonical visual usefulness rule: render only when a cleared visual materially helps recognition, distinction or understanding;\n- [x] derive rendering from usefulness + cleared rights state rather than an independent render switch;\n- [x] wire the resource visual registry into the public builder and local generated asset publication path;\n- [x] add positive-path cleared-fixture proof plus fail-closed negative tests;\n- [x] inventory every P1 book/game/app/media Resource and record an explicit rights state without fabricating permission;\n- [x] define media-format, local-path and 1.5 MB source-asset boundaries."
    if addition not in text:
        if marker not in text:
            raise SystemExit("completion marker missing")
        text = text.replace(marker, addition, 1)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    write_resource_visuals_module()
    patch_builder()
    update_policy()
    update_design_system()
    build_registry_and_inventory()
    write_tests()
    update_completion_register()


if __name__ == "__main__":
    main()
