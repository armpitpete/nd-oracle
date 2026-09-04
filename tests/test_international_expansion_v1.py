from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "contracts" / "international-expansion-v1.json"
DOC = ROOT / "docs" / "INTERNATIONAL_EXPANSION_ARCHITECTURE_v1.md"


class InternationalExpansionV1Tests(unittest.TestCase):
    def load_contract(self) -> dict:
        return json.loads(CONTRACT.read_text(encoding="utf-8"))

    def test_package_model_rejects_mass_empty_country_expansion(self) -> None:
        contract = self.load_contract()
        model = contract["package_model"]
        sequencing = contract["sequencing"]

        self.assertEqual("jurisdiction_package", model["name"])
        self.assertTrue(model["no_empty_country_shells"])
        self.assertTrue(model["no_silent_scope_inheritance"])
        self.assertFalse(sequencing["parallel_mass_country_expansion"])
        self.assertEqual(
            "single_country_source_readiness_probe",
            sequencing["next_action_after_acceptance"],
        )

    def test_core_schema_is_deferred_until_real_implementations_prove_need(self) -> None:
        model = self.load_contract()["package_model"]
        self.assertFalse(model["core_schema_change_now"])
        self.assertEqual(3, model["schema_reconsideration_after_real_country_packages"])

    def test_discovery_and_translation_boundaries_are_explicit(self) -> None:
        contract = self.load_contract()
        discovery = contract["discovery_rules"]
        translation = contract["translation_rules"]

        self.assertTrue(discovery["additive_only"])
        self.assertTrue(discovery["must_not_replace_frozen_uk_bindings"])
        self.assertTrue(discovery["exact_scope_binding_required"])
        self.assertTrue(discovery["cross_jurisdiction_hostile_cases_required"])
        self.assertTrue(discovery["no_global_uk_fallback"])

        self.assertTrue(translation["record_source_language"])
        self.assertTrue(translation["prefer_first_party_local_language"])
        self.assertTrue(translation["machine_translation_is_not_authoritative_provenance"])
        self.assertTrue(translation["published_translation_preserves_original_source"])
        self.assertTrue(translation["material_translation_uncertainty_must_be_visible"])

    def test_acceptance_and_production_remain_separate(self) -> None:
        contract = self.load_contract()
        acceptance = set(contract["acceptance_gates"])
        production = set(contract["production_gates"])

        self.assertIn("protected_exact_head_merge_authority", acceptance)
        self.assertIn("full_regression_pass", acceptance)
        self.assertIn("hostile_diff_review_pass", acceptance)

        self.assertIn("exact_main_deployment", production)
        self.assertIn("artifact_identity_recorded", production)
        self.assertIn("fresh_network_backed_verification", production)
        self.assertIn("production_state_reconciled", production)
        self.assertNotIn("exact_main_deployment", acceptance)

    def test_reference_implementation_and_document_are_present(self) -> None:
        contract = self.load_contract()
        ref = contract["reference_implementation"]

        for relative in (
            ref["baseline"],
            ref["assessment_contract"],
            ref["assessment_discovery"],
        ):
            self.assertTrue((ROOT / relative).is_file(), relative)

        text = DOC.read_text(encoding="utf-8")
        self.assertIn("one jurisdiction package at a time", text)
        self.assertIn("no silent jurisdiction inheritance", text)
        self.assertIn("Do not change the core object schema", text)
        self.assertIn("single-country source-readiness probe", text)


if __name__ == "__main__":
    unittest.main()
