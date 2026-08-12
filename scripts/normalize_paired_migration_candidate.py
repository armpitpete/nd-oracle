#!/usr/bin/env python3
"""Historical normalization bound to immutable foundation-source snapshots."""
from __future__ import annotations

from scripts import _historical_normalize_paired_migration_candidate as _impl
from scripts.historical_foundation_sources import AUTISM, NEURODIVERSITY

_impl.AUT = AUTISM
_impl.ND = NEURODIVERSITY

for _name in dir(_impl):
    if not _name.startswith("__") and _name != "apply_normalization":
        globals()[_name] = getattr(_impl, _name)


def apply_normalization(destination):
    _impl.AUT = AUTISM
    _impl.ND = NEURODIVERSITY
    return _impl.apply_normalization(destination)
