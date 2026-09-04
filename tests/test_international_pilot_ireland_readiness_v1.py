from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "contracts" / "international-pilot-ireland-readiness-v1.json"
DOC = ROOT / "docs" / "INTERNATIONAL_PILOT_IRELAND_READINESS_v1.md"


class IrelandPilotReadinessV1Tests(unittest.TestCase):
    def load_contract(self) -> dict:
        return json.loads(CONTRACT.read_text(encoding="utf-8"))

    def test_readiness_pass_is_bounded_to_republic_of_ireland(self) -> None:
        contract = self.load_contract()
        jurisdiction = contract["jurisdiction"]
        self.assertEqual("readiness_pass", contract["status"])
        self.assertEqual("Republic of Ireland", jurisdiction["canonical_name"])
        self.assertIn("Northern Ireland", jurisdiction["country_scope_must_exclude"])
        self.assertEqual("Health Service Executive", jurisdiction["public_health_authority"])

    def test_initial_candidate_is_small_and_child_adhd_is_deferred(self) -> None:
        contract = self.load_contract()
        self.assertEqual(4, len(contract["initial_candidate_routes"]))
        self.assertIn(
            "child_adhd_assessment_republic_of_ireland",
            contract["deferred_routes"],
        )
        self.assertFalse(
            contract["journeys"]["child_adhd_assessment"]["strong_national_access_route_allowed_now"]
        )

    def test_diagnostic_and_service_boundaries_are_explicit(self) -> None:
        journeys = self.load_contract()["journeys"]
        self.assertFalse(
            journeys["adult_autism_assessment"]["provider_endorsement_allowed"]
        )
        self.assertFalse(
            journeys["adult_adhd_assessment"]["universal_current_public_team_availability"]
        )
        self.assertTrue(
            journeys["assessment_of_need_vs_diagnosis"]["must_remain_distinct_from_clinical_diagnosis"]
        )
        self.assertFalse(
            journeys["assessment_of_need_vs_diagnosis"]["required_for_hse_service_access"]
        )

    def test_cross_border_hostile_boundaries_are_required(self) -> None:
        hostile = set(self.load_contract()["hostile_boundaries"])
        required = {
            "no_england_right_to_choose_in_ireland",
            "no_northern_ireland_hsc_as_republic_of_ireland_hse",
            "no_republic_of_ireland_hse_as_northern_ireland_hsc",
            "assessment_of_need_is_not_clinical_diagnosis",
            "adult_adhd_model_is_not_universal_service_availability",
            "diagnosis_does_not_authorize_medication_decisions",
        }
        self.assertTrue(required.issubset(hostile))

    def test_probe_does_not_authorize_broad_country_expansion(self) -> None:
        contract = self.load_contract()
        self.assertFalse(contract["broad_country_expansion_authorized"])
        self.assertEqual(
            "build_bounded_ireland_assessment_diagnosis_candidate",
            contract["next_action"],
        )
        text = DOC.read_text(encoding="utf-8")
        self.assertIn("PASS — suitable first international pilot", text)
        self.assertIn("Do not create a broad Ireland corpus yet", text)


if __name__ == "__main__":
    unittest.main()
