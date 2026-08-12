import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from scripts.build_paired_migration_candidate import build_candidate
from scripts.validate_migration import validate_package


ROOT = Path(__file__).resolve().parents[1]
PAIR = ROOT / "migration-candidates" / "autism-neurodiversity" / "structural-candidate.json"
DECISIONS = ROOT / "migration-candidates" / "autism-neurodiversity" / "owner-decisions.json"
COMMON = ROOT / "schema" / "common-v0.2.json"
AUTISM = ROOT / "objects" / "concepts" / "autism.json"
NEURODIVERSITY = ROOT / "objects" / "concepts" / "neurodiversity.json"
ADHD = ROOT / "objects" / "concepts" / "adhd.json"
PROOF = ROOT / "docs" / "migration-proofs" / "D17_PAIRED_CANDIDATE_IMPLEMENTATION.md"
D17 = "d17-neurodiversity-legacy-structural-disposition"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def git_blob_sha(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


class D17PairedCandidateImplementationTests(unittest.TestCase):
    def test_implementation_authority_is_post_decision_and_non_authoritative(self) -> None:
        pair = load(PAIR)
        authority = pair["implementation_authority"]
        self.assertEqual("owner_directed_non_authoritative_candidate_implementation", authority["kind"])
        self.assertEqual("266362fe083fb278fc1dcc8f0a90619906194f07", authority["authorised_against_main"])
        self.assertEqual(D17, authority["governing_decision"])
        self.assertIn("legacy_retained_unmapped", authority["scope"])
        self.assertFalse(pair["authoritative"])
        self.assertFalse(pair["authorisations"]["authoritative_v02_replacement"])
        self.assertFalse(pair["authorisations"]["new_semantic_graph_relation_authorised"])
        self.assertFalse(pair["authorisations"]["expand_pair_to_adhd"])

    def test_pair_emits_no_v02_taxonomy_edge_and_preserves_exact_legacy_records(self) -> None:
        pair = load(PAIR)
        objects = {item["id"]: item["structural_relation"] for item in pair["objects"]}
        expected = {
            "autism": {
                "type": "narrower_than",
                "target_id": "neurodiversity",
                "note": "Autism is commonly situated within neurodiversity discourse.",
            },
            "neurodiversity": {
                "type": "broader_than",
                "target_id": "autism",
                "note": "Autism is commonly discussed within the neurodiversity ecosystem.",
            },
        }
        for object_id, relation in objects.items():
            self.assertEqual("legacy_retained_unmapped", relation["disposition"])
            self.assertFalse(relation["emit_v02_semantic_edge"])
            self.assertEqual(D17, relation["decision_ref"])
            self.assertNotIn("type", relation)
            self.assertNotIn("target", relation)
            self.assertNotIn("confidence", relation)
            self.assertEqual("not_required_without_v02_edge", relation["confidence_status"])
            self.assertEqual(expected[object_id], relation["legacy_relation"])

    def test_historical_confidence_blocker_is_retained_as_resolved_trace(self) -> None:
        pair = load(PAIR)
        blockers = {item["id"]: item for item in pair["blockers"]}
        historical = blockers["paired-structural-relation-confidence"]
        self.assertEqual("resolved_by_d17_no_v02_edge", historical["kind"])
        self.assertEqual(D17, historical["decision_ref"])
        self.assertEqual("d6-structural-relation-confidence", historical["policy_ref"])
        self.assertFalse(pair["authorisations"]["paired_structural_confidence_required_for_legacy_pair"])
        self.assertFalse(pair["authorisations"]["infer_or_default_structural_confidence"])
        self.assertFalse(pair["authorisations"]["use_not_applicable_as_confidence_shortcut"])

    def test_d17_decision_record_is_preserved_and_not_rewritten(self) -> None:
        decisions = {item["id"]: item for item in load(DECISIONS)["decisions"]}
        d17 = decisions[D17]
        self.assertEqual("accepted", d17["status"])
        self.assertEqual("586f9589c4c14a0bcb7a84bc0c579bfef94f6d7c", d17["accepted_against_main"])
        self.assertFalse(d17["paired_candidate_mutation_authorised"])
        self.assertFalse(d17["schema_change_authorised"])
        self.assertFalse(d17["validator_change_authorised"])
        self.assertFalse(d17["adhd_scope_expansion_authorised"])

    def test_generated_package_preserves_d6_and_d17_and_does_not_regenerate_confidence(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            package = Path(tmp) / "pair"
            build_candidate(package)
            self.assertEqual([], validate_package(package))
            decisions = {item["id"]: item for item in load(package / "owner-decisions.json")["decisions"]}
            self.assertIn("d6-structural-relation-confidence", decisions)
            self.assertIn(D17, decisions)
            enrichment_ids = {item["id"] for item in load(package / "enrichment-ledger.json")["entries"]}
            self.assertNotIn("resolve-autism-neurodiversity-structural-confidence", enrichment_ids)
            dependencies = {item["id"]: item for item in load(package / "dependency-ledger.json")["entries"]}
            self.assertEqual("resolved", dependencies["dependency-autism-neurodiversity"]["resolution_status"])
            self.assertEqual("unresolved", dependencies["dependency-neurodiversity-adhd"]["resolution_status"])

    def test_schema_and_authoritative_objects_are_unchanged(self) -> None:
        self.assertEqual("ce0141ee7031f21fa2bd72b2faa3371aed3e622b", git_blob_sha(COMMON))
        self.assertEqual("b2d3809ecfcdb1d81c793a2401f0533a4b17ea98", git_blob_sha(AUTISM))
        self.assertEqual("5a38bc4250079412dd3f4da1d598dfcab984ca66", git_blob_sha(NEURODIVERSITY))
        self.assertEqual("719f26a9af773cd1bcf670df4d12ed5f6bcf0a23", git_blob_sha(ADHD))

    def test_proof_records_no_replacement_relation_or_adhd_expansion(self) -> None:
        proof = PROOF.read_text(encoding="utf-8")
        self.assertIn("no current v0.2 `type` field", proof)
        self.assertIn("no current v0.2 `target` field", proof)
        self.assertIn("no `confidence` value", proof)
        self.assertIn("ADHD migration scope expansion", proof)
        self.assertIn("D17 is not rewritten", proof)


if __name__ == "__main__":
    unittest.main()
