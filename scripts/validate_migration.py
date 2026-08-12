#!/usr/bin/env python3
"""Validate migration packages against the immutable source state they record."""
from __future__ import annotations

import json
import shutil
import sys
import tempfile
from pathlib import Path

from scripts import _historical_validate_migration as _impl
from scripts.historical_foundation_sources import (
    ADHD,
    AUTISM,
    EXECUTIVE_FUNCTION,
    NEURODIVERSITY,
    ROOT,
    SENSORY_PROCESSING,
)

_SNAPSHOTS = {
    "autism": AUTISM,
    "neurodiversity": NEURODIVERSITY,
    "adhd": ADHD,
    "executive-function": EXECUTIVE_FUNCTION,
    "sensory-processing": SENSORY_PROCESSING,
}

for _name in dir(_impl):
    if not _name.startswith("__") and _name not in {"validate_package", "main"}:
        globals()[_name] = getattr(_impl, _name)


def validate_package(package_dir: Path, root: Path = ROOT) -> list[str]:
    package_dir = Path(package_dir)
    root = Path(root)
    if root.resolve() != ROOT.resolve():
        return _impl.validate_package(package_dir, root)

    manifest_path = package_dir / "manifest.json"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return _impl.validate_package(package_dir, root)

    sources = manifest.get("sources")
    if not isinstance(sources, list):
        return _impl.validate_package(package_dir, root)

    with tempfile.TemporaryDirectory(prefix="nd-oracle-historical-sources-") as directory:
        mirror = Path(directory)
        for source in sources:
            if not isinstance(source, dict) or not isinstance(source.get("path"), str):
                continue
            destination = mirror / source["path"]
            destination.parent.mkdir(parents=True, exist_ok=True)
            object_id = source.get("object_id")
            snapshot = _SNAPSHOTS.get(object_id)
            source_path = snapshot if snapshot is not None else root / source["path"]
            if source_path.exists():
                shutil.copyfile(source_path, destination)
        return _impl.validate_package(package_dir, mirror)


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if len(args) != 1:
        print("usage: python scripts/validate_migration.py <migration-package-directory>", file=sys.stderr)
        return 2
    errors = validate_package(Path(args[0]))
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print(f"Migration package valid: {args[0]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
