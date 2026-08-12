"""Load immutable historical tests against immutable foundation-source snapshots."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import sys
import types
import unittest

from scripts.historical_foundation_sources import (
    ADHD,
    AUTISM,
    EXECUTIVE_FUNCTION,
    NEURODIVERSITY,
    SENSORY_PROCESSING,
)

_LIVE_TO_HISTORICAL = {
    str(Path(__file__).resolve().parents[1] / "objects" / "concepts" / "autism.json"): AUTISM,
    str(Path(__file__).resolve().parents[1] / "objects" / "concepts" / "neurodiversity.json"): NEURODIVERSITY,
    str(Path(__file__).resolve().parents[1] / "objects" / "concepts" / "adhd.json"): ADHD,
    str(Path(__file__).resolve().parents[1] / "objects" / "concepts" / "executive-function.json"): EXECUTIVE_FUNCTION,
    str(Path(__file__).resolve().parents[1] / "objects" / "concepts" / "sensory-processing.json"): SENSORY_PROCESSING,
}


def _replace_paths(value):
    if isinstance(value, Path):
        return _LIVE_TO_HISTORICAL.get(str(value), value)
    if isinstance(value, list):
        return [_replace_paths(item) for item in value]
    if isinstance(value, tuple):
        return tuple(_replace_paths(item) for item in value)
    if isinstance(value, set):
        return {_replace_paths(item) for item in value}
    if isinstance(value, dict):
        return {_replace_paths(key): _replace_paths(item) for key, item in value.items()}
    return value


def bind_historical_foundation_paths(module: types.ModuleType) -> None:
    """Replace module-level live foundation paths with immutable snapshots."""
    for name, value in list(vars(module).items()):
        if name.startswith("__"):
            continue
        replaced = _replace_paths(value)
        if replaced is not value:
            setattr(module, name, replaced)


def export_historical_tests(target_globals: dict, wrapper_file: str, implementation_name: str) -> None:
    """Load a preserved test implementation and export its TestCase classes."""
    implementation = Path(wrapper_file).with_name(implementation_name)
    module_name = f"_nd_oracle_historical_{implementation.stem}_{abs(hash(str(implementation)))}"
    spec = importlib.util.spec_from_file_location(module_name, implementation)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load historical test implementation: {implementation}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    bind_historical_foundation_paths(module)
    for name, value in vars(module).items():
        if isinstance(value, type) and issubclass(value, unittest.TestCase):
            target_globals[name] = value
