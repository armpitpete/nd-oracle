#!/usr/bin/env python3
"""Historical paired-migration builder bound to immutable source snapshots."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from scripts import _historical_build_paired_migration_candidate as _impl
from scripts.historical_foundation_sources import AUTISM, NEURODIVERSITY, ROOT

_impl.AUTISM_SOURCE = AUTISM
_impl.NEURODIVERSITY_SOURCE = NEURODIVERSITY

for _name in dir(_impl):
    if not _name.startswith("__") and _name not in {"build_candidate", "main"}:
        globals()[_name] = getattr(_impl, _name)


def build_candidate(destination: Path) -> Path:
    _impl.AUTISM_SOURCE = AUTISM
    _impl.NEURODIVERSITY_SOURCE = NEURODIVERSITY
    result = _impl.build_candidate(destination)
    manifest_path = Path(result) / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    snapshot_paths = {
        "autism": AUTISM.relative_to(ROOT).as_posix(),
        "neurodiversity": NEURODIVERSITY.relative_to(ROOT).as_posix(),
    }
    for source in manifest.get("sources", []):
        object_id = source.get("object_id") or source.get("id")
        if object_id in snapshot_paths:
            source["path"] = snapshot_paths[object_id]
        elif str(source.get("path", "")).endswith("autism.json"):
            source["path"] = snapshot_paths["autism"]
        elif str(source.get("path", "")).endswith("neurodiversity.json"):
            source["path"] = snapshot_paths["neurodiversity"]
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("destination", type=Path)
    args = parser.parse_args()
    build_candidate(args.destination)
    print(args.destination)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
