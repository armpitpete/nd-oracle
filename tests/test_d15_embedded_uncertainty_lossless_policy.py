import hashlib
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAIR = ROOT / "migration-candidates" / "autism-neurodiversity" / "structural-candidate.json"
DECISIONS = ROOT / "migration-candidates" / "autism-neurodiversity" / "owner-decisions.json"
RESEARCH = ROOT / "migration-candidates" / "autism-neurodiversity" / "uncertainty-shape-research.json"
COMMON_V02 = ROOT / "schema" / "common-v0.2.json"
AUTISM = ROOT / "objects" / "concepts" / "autism.json"
NEURODIVERSITY = ROOT / "objects" / "concepts" / "neurodiversity.json"
DOC = ROOT / "docs" / "migration-proofs" / "D15_EMBEDDED_UNCERTAINTY_LOSSLESS_POLICY.md"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def git_blob_sha(path: Path) -> str:
    data = path.read_bytes()
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


class D15EmbeddedUncertaintyLosslessPolicyTests(unittest.TestCase):
    def test_d15_records_exact_policy_acceptance_against_post_pr52_main(self) -> None:
        decisions = {item["id"]: item for item in load(DECISIONS)["decisions"]}
        d15 = decisions["d15-embedded-uncertainty-lossless-representation"]

        self.assertEqual(d15["status"], "accepted")
        self.assertEqual(d15["accepted_on"], "2026-08-11")
        self.assertEqual(
            d15["accepted_against_main"],
            "a9bed79b827f6308cbaa8f2a11edda1b9c5d3da8",
        )
        self.assertEqual(
            d15["supersedes_research_decision_candidate"],
            {
                "path": "migration-candidates/autism-neurodiversity/uncertainty-shape-research.json",
                "id": "nd-embedded-uncertainty-lossless-representation",
            },
        )

        policy = d15["accepted_policy"]
        self.assertTrue(policy["preserve_one_legacy_uncertainty_as_one_embedded_uncertainty_by_default"])
        self.assertTrue(policy["preserve_multiple_reduction_or_reopening_routes_as_distinct_items"])
        self.assertTrue(policy["preserve_lifecycle_state_explicitly"])
        self.assertTrue(policy["preserve_legacy_interrogative_wording_without_forced_declarative_conversion"])
        self.assertTrue(policy["question_promotion_requires_separate_explicit_justification"])

    def test_d15_does_not_authorise_implementation_or_semantic_shortcuts(self) -> None:
        decisions = {item["id"]: item for item in load(DECISIONS)["decisions"]}
        d15 = decisions["d15-embedded-uncertainty-lossless-representation"]

        for field in (
            "schema_change_authorised",
            "validator_change_authorised",
            "authoritative_v01_mutation_authorised",
            "authoritative_v02_replacement_authorised",
            "automatic_question_promotion_authorised",
            "uncertainty_split_authorised",
            "list_flattening_authorised",
            "status_remapping_authorised",
            "publication_or_deployment_authorised",
        ):
            self.assertFalse(d15[field], field)

    def test_research_remains_historical_pre_d15_snapshot(self) -> None:
        research = load(RESEARCH)
        self.assertEqual(
            research["prepared_against_main"],
            "a95a7772f6ca69d2c5b58cbcdcc6240110cc9ce8",
        )
        self.assertEqual(
            research["decision_candidate"]["id"],
            "nd-embedded-uncertainty-lossless-representation",
        )
        self.assertEqual(research["decision_candidate"]["status"], "owner_decision_required")
        self.assertFalse(research["boundaries"]["schema_change_authorised"])
        self.assertFalse(research["boundaries"]["validator_change_authorised"])

    def test_current_pair_records_policy_accepted_but_implementation_pending(self) -> None:
        pair = load(PAIR)
        self.assertIn(
            "d15-embedded-uncertainty-lossless-representation",
            pair["accepted_owner_decisions"],
        )
        self.assertIn(
            "migration-candidates/autism-neurodiversity/uncertainty-shape-research.json",
            pair["research_refs"],
        )

        blockers = {item["id"]: item for item in pair["blockers"]}
        for blocker_id in ("autism-uncertainty-shape", "neurodiversity-uncertainty-shape"):
            blocker = blockers[blocker_id]
            self.assertEqual(blocker["kind"], "accepted_policy_schema_implementation_pending")
            self.assertEqual(
                blocker["decision_ref"],
                "d15-embedded-uncertainty-lossless-representation",
            )

        auth = pair["authorisations"]
        self.assertTrue(auth["embedded_uncertainty_lossless_policy_accepted"])
        self.assertFalse(auth["embedded_uncertainty_schema_change_authorised"])
        self.assertFalse(auth["embedded_uncertainty_validator_change_authorised"])
        self.assertFalse(auth["automatic_question_promotion_authorised"])
        self.assertFalse(auth["uncertainty_split_authorised"])
        self.assertFalse(auth["uncertainty_list_flattening_authorised"])
        self.assertFalse(auth["uncertainty_status_remapping_authorised"])

    def test_schema_remains_pre_d15_implementation_shape(self) -> None:
        common = load(COMMON_V02)["$defs"]["uncertainty"]
        self.assertEqual(
            common["required"],
            ["id", "statement", "why_it_matters", "reopening_or_reduction_condition"],
        )
        self.assertNotIn("status", common["properties"])
        self.assertEqual(
            common["properties"]["reopening_or_reduction_condition"]["$ref"],
            "#/$defs/nonBlankString",
        )
        self.assertEqual(git_blob_sha(COMMON_V02), "2c0fc2344fcafde88340b8a5882e0d171246ea02")

    def test_authoritative_pair_sources_remain_unchanged(self) -> None:
        self.assertEqual(git_blob_sha(AUTISM), "b2d3809ecfcdb1d81c793a2401f0533a4b17ea98")
        self.assertEqual(git_blob_sha(NEURODIVERSITY), "5a38bc4250079412dd3f4da1d598dfcab984ca66")

        doc = DOC.read_text(encoding="utf-8")
        self.assertIn("policy direction accepted", doc)
        self.assertIn("implementation not authorised", doc)
        self.assertIn("accepted_policy_schema_implementation_pending", doc)


if __name__ == "__main__":
    unittest.main()
