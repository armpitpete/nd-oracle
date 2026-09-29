from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "site" / "terminology.json"
REQUIRED_FIELDS = {
    "id", "term", "kind", "aliases", "parts", "meaning",
    "related_routes", "reviewed_on", "provenance",
}
VALID_KINDS = {"word", "phrase", "acronym"}


def load_registry(path: Path = REGISTRY_PATH) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_registry(registry: dict, *, expected_count: int = 52) -> None:
    if registry.get("schema_version") != "1":
        raise ValueError("Terminology registry schema_version must be 1")
    entries = registry.get("entries")
    if not isinstance(entries, list) or len(entries) != expected_count:
        raise ValueError(
            f"Terminology registry must contain exactly {expected_count} audited entries"
        )

    ids: list[str] = []
    canonical: list[str] = []
    aliases: dict[str, set[str]] = {}
    for item in entries:
        missing = REQUIRED_FIELDS - set(item)
        if missing:
            raise ValueError(
                f"{item.get('id', '<unknown>')}: missing fields {sorted(missing)}"
            )
        if item["kind"] not in VALID_KINDS:
            raise ValueError(f"{item['id']}: invalid kind {item['kind']}")
        if not item["id"] or not item["term"] or not item["meaning"]:
            raise ValueError(f"{item['id']}: id, term and meaning are required")
        if not item["parts"] or any(
            not part.get("label") or not part.get("meaning")
            for part in item["parts"]
        ):
            raise ValueError(
                f"{item['id']}: every entry needs at least one explained part"
            )
        if not item["related_routes"] or any(
            not route.startswith("/") for route in item["related_routes"]
        ):
            raise ValueError(
                f"{item['id']}: related_routes must contain site-relative routes"
            )
        ids.append(item["id"])
        canonical.append(item["term"].casefold())
        for alias in item["aliases"]:
            aliases.setdefault(alias.casefold(), set()).add(item["id"])

    if len(ids) != len(set(ids)):
        raise ValueError("Terminology registry contains duplicate IDs")
    if len(canonical) != len(set(canonical)):
        raise ValueError("Terminology registry contains duplicate canonical terms")
    ambiguous = {
        alias: sorted(targets)
        for alias, targets in aliases.items()
        if len(targets) > 1
    }
    if ambiguous:
        raise ValueError(
            "Terminology aliases must resolve to one canonical entry: "
            f"{ambiguous}"
        )


def entries_by_id(registry: dict) -> dict[str, dict]:
    validate_registry(registry)
    return {item["id"]: item for item in registry["entries"]}
