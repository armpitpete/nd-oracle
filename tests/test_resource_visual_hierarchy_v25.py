from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CSS = ROOT / "site" / "styles.css"
VISUALS = ROOT / "site" / "resource-visuals.json"
POLICY = ROOT / "docs" / "RESOURCE_VISUAL_ASSET_POLICY_v1.md"


def test_resource_detail_keeps_readable_base_size_and_adds_weight_hierarchy() -> None:
    css = CSS.read_text(encoding="utf-8")
    marker = "ND-UX-V2.5: YP/ND resource hierarchy"
    assert marker in css
    tail = css[css.index(marker):]
    assert "font-size" not in tail.split("/* V2.5 resource imagery", 1)[0]
    assert ".page--resource .notice strong" in tail
    assert "font-weight: 850" in tail
    assert "section[aria-labelledby=\"limits-heading\"]" in tail


def test_resource_detail_uses_bounded_colour_sections_and_compact_proximity() -> None:
    css = CSS.read_text(encoding="utf-8")
    tail = css[css.index("ND-UX-V2.5: YP/ND resource hierarchy"):]
    for token in (
        "var(--wayfind-green-soft)",
        "var(--wayfind-cyan-soft)",
        "var(--wayfind-violet-soft)",
        "var(--wayfind-rose-soft)",
        "var(--wayfind-amber-soft)",
        "var(--wayfind-slate-soft)",
    ):
        assert token in tail
    assert "margin: 0.7rem 0" in tail
    assert "margin-top: 0" in tail
    assert "border-left" in tail


def test_resource_visual_registry_fails_closed_by_policy() -> None:
    registry = json.loads(VISUALS.read_text(encoding="utf-8"))
    assert registry["policy"] == "docs/RESOURCE_VISUAL_ASSET_POLICY_v1.md"
    for resource_id, entry in registry["entries"].items():
        assert entry["resource_id"] == resource_id
        if entry["render"]:
            assert entry["status"] == "cleared"
            assert entry["local_path"].startswith("site/resource-media/")
            assert entry["alt"]
            assert entry["source_url"]
            assert entry["rights_basis"]
            assert (ROOT / entry["local_path"]).is_file()
        else:
            assert entry["status"] != "cleared" or entry["local_path"] is None


def test_stardew_visual_is_not_fabricated_or_hotlinked_without_rights() -> None:
    registry = json.loads(VISUALS.read_text(encoding="utf-8"))
    stardew = registry["entries"]["stardew-valley"]
    assert stardew["status"] == "permission-required"
    assert stardew["render"] is False
    assert stardew["local_path"] is None
    assert "stardewvalley.net/terms" in stardew["source_url"]

    policy = POLICY.read_text(encoding="utf-8")
    assert "hotlink third-party covers" in policy
    assert "create a lookalike image and present it as the product" in policy
    assert "recognition material, not evidence" in policy
