from __future__ import annotations

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


def validate_registry(registry: dict, resources: list[dict], *, root: Path = ROOT, require_complete: bool = False) -> dict:
    if registry.get("schema_version") != "2":
        raise ValueError("resource visual registry must use schema_version 2")
    if registry.get("policy") != "docs/RESOURCE_VISUAL_ASSET_POLICY_v1.md":
        raise ValueError("resource visual registry policy pointer is invalid")
    entries = registry.get("entries")
    if not isinstance(entries, dict):
        raise ValueError("resource visual registry entries must be an object")

    resource_map = {item["id"]: item for item in resources}
    if require_complete:
        missing = sorted(set(resource_map) - set(entries))
        if missing:
            raise ValueError(f"resource visual registry is incomplete; missing Resource IDs: {', '.join(missing)}")

    rendered_assets: set[str] = set()
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
            _validate_asset_bytes(asset, resource_id=resource_id)
            if entry.get("attribution_required") and not entry.get("attribution"):
                raise ValueError(f"{resource_id}: cleared visual requires attribution text")
            asset_key = str(asset.resolve()).casefold()
            if asset_key in rendered_assets:
                raise ValueError(f"{resource_id}: cleared visual reuses a local asset already mapped to another Resource")
            rendered_assets.add(asset_key)
        else:
            if entry.get("local_path") is not None:
                raise ValueError(f"{resource_id}: uncleared/non-useful visual must not store a publishable local_path")
            if entry.get("alt") is not None:
                raise ValueError(f"{resource_id}: uncleared/non-useful visual must not publish alt text")
            if entry.get("rights_basis") is not None:
                raise ValueError(f"{resource_id}: uncleared/non-useful visual must not claim a rights basis")
    return registry


def _validate_asset_bytes(asset: Path, *, resource_id: str) -> None:
    raw = asset.read_bytes()
    suffix = asset.suffix.casefold()
    if suffix == ".png" and not raw.startswith(b"\x89PNG\r\n\x1a\n"):
        raise ValueError(f"{resource_id}: PNG asset has an invalid file signature")
    if suffix in {".jpg", ".jpeg"} and not raw.startswith(b"\xff\xd8\xff"):
        raise ValueError(f"{resource_id}: JPEG asset has an invalid file signature")
    if suffix == ".webp" and (len(raw) < 12 or raw[:4] != b"RIFF" or raw[8:12] != b"WEBP"):
        raise ValueError(f"{resource_id}: WebP asset has an invalid file signature")
    if suffix == ".svg" and b"<svg" not in raw[:2048].lower():
        raise ValueError(f"{resource_id}: SVG asset does not contain an SVG root element")


def render_resource_visual(resource: dict, *, registry: dict | None = None, root: Path = ROOT) -> str:
    if registry is None:
        registry = load_registry()
    entry = registry.get("entries", {}).get(resource["id"])
    if not entry or not should_render(entry):
        return ""
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
    validate_registry(registry, resources, root=root, require_complete=True)
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
