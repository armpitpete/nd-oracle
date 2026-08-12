"""Immutable pre-review source paths for historical migration proofs.

These paths deliberately do not point at the living authoritative corpus.
Historical migration work must remain anchored to the exact source blobs it
originally evaluated even after authoritative objects evolve.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HISTORICAL_FOUNDATION_ROOT = (
    ROOT / "migration-snapshots" / "foundation-seed-2026-08-10" / "objects" / "concepts"
)

AUTISM = HISTORICAL_FOUNDATION_ROOT / "autism.json"
NEURODIVERSITY = HISTORICAL_FOUNDATION_ROOT / "neurodiversity.json"
ADHD = HISTORICAL_FOUNDATION_ROOT / "adhd.json"
EXECUTIVE_FUNCTION = HISTORICAL_FOUNDATION_ROOT / "executive-function.json"
SENSORY_PROCESSING = HISTORICAL_FOUNDATION_ROOT / "sensory-processing.json"

HISTORICAL_FOUNDATION_BLOBS = {
    "autism": "b2d3809ecfcdb1d81c793a2401f0533a4b17ea98",
    "neurodiversity": "5a38bc4250079412dd3f4da1d598dfcab984ca66",
    "adhd": "719f26a9af773cd1bcf670df4d12ed5f6bcf0a23",
    "executive-function": "f67e1a73e89245f9e6c6c2a34d4acc47169b8273",
    "sensory-processing": "7626d61a2844aae88ce6811760dfe97b5baa94bc",
}
