from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path

from scripts.validate import missing_v01_preservation_units, v01_preservation_inventory

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "objects" / "concepts" / "autism.json"
MANIFEST = ROOT / "docs" / "migration-proofs" / "autism-v0.1-to-v0.2.json"


def git_blob_sha(path: Path) -> str:
    data = path.read_bytes()
    prefix = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(prefix + data).hexdigest()


class AutismMigrationProofTests(unittest.TestCase):
    def setUp(self) -> None:
        self.source = json.loads(SOURCE.read_text(encoding="utf-8"))
        self.manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

    def test_proof_is_anchored_to_exact_authoritative_blob(self) -> None:
        self.assertEqual("b2d3809ecfcdb1d81c793a2401f0533a4b17ea98", git_blob_sha(SOURCE))
        self.assertEqual(git_blob_sha(SOURCE), self.manifest["source"]["git_blob_sha"])
        self.assertFalse(self.manifest["authoritative_mutation"])

    def test_all_v01_preservation_units_are_accounted_for(self) -> None:
        classified = {item["unit"] for item in self.manifest["classifications"]}
        inventory = v01_preservation_inventory(self.source)
        self.assertEqual(34, len(inventory))
        self.assertEqual(inventory, classified)
        self.assertEqual([], missing_v01_preservation_units(self.source, classified))

    def test_classifications_use_governed_vocabulary(self) -> None:
        allowed = set(self.manifest["classification_vocabulary"])
        used = {item["classification"] for item in self.manifest["classifications"]}
        self.assertTrue(used <= allowed)
        self.assertNotIn("loss", used)

    def test_name_and_status_are_explicitly_preserved(self) -> None:
        supplemental = self.manifest["supplemental_preservation"]
        self.assertEqual(self.source["name"], supplemental["name"])
        self.assertEqual(self.source["status"], supplemental["status"])

    def test_proof_stops_on_real_blockers(self) -> None:
        blocking = {
            item["id"]
            for item in self.manifest["blockers"]
            if item["severity"] == "blocking"
        }
        self.assertEqual(
            {
                "evidence-contribution-semantics",
                "evidence-required-metadata",
                "perspective-required-fields",
                "cross-version-structural-reciprocity",
                "ecosystem-entry-successor",
            },
            blocking,
        )
        self.assertEqual(
            "not_migratable_losslessly_under_current_contract",
            self.manifest["conclusion"]["result"],
        )


if __name__ == "__main__":
    unittest.main()
