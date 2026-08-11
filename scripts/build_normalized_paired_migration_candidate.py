#!/usr/bin/env python3
"""Build the D1-D17-normalized Autism + Neurodiversity migration candidate."""
from __future__ import annotations

import argparse
from pathlib import Path

try:
    from scripts.build_paired_migration_candidate import build_candidate as build_partial_candidate
    from scripts.normalize_paired_migration_candidate import apply_normalization
except ModuleNotFoundError:  # direct execution from scripts/
    from build_paired_migration_candidate import build_candidate as build_partial_candidate
    from normalize_paired_migration_candidate import apply_normalization


def build_candidate(destination: Path) -> Path:
    return apply_normalization(build_partial_candidate(Path(destination)))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("destination", type=Path)
    args = parser.parse_args()
    print(build_candidate(args.destination))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
