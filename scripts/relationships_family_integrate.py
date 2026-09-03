from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def replace_once(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    if new in text:
        return
    if old not in text:
        raise RuntimeError(f"integration anchor missing: {path}: {old[:80]!r}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


def update_question(object_id: str, *, question: str) -> None:
    path = ROOT / "objects" / "questions" / f"{object_id}.json"
    item = json.loads(path.read_text(encoding="utf-8"))
    if item["question"] == question:
        return
    item["question"] = question
    path.write_text(json.dumps(item, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")


def update_benchmark() -> None:
    path = ROOT / "benchmarks" / "relationships-family-uk-v1.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    changes = {
        "friend does not understand my autistic communication": [
            "/questions/friendship-misunderstandings-neurodivergent/",
            "/questions/communication-needs-in-relationships/",
        ],
        "sensory boundary touch relationship": [
            "/questions/boundaries-neurodivergent-relationships/",
            "/questions/intimacy-consent-sensory-communication/",
        ],
        "need time before replying relationship boundary": [
            "/questions/boundaries-neurodivergent-relationships/",
            "/questions/processing-time-in-conversations-meetings/",
            "/questions/partner-communication-processing-sensory-needs/",
        ],
        "prefer text instead of phone boundary relationship": [
            "/questions/boundaries-neurodivergent-relationships/",
            "/questions/phone-calls-are-difficult/",
        ],
        "relationship sexual pressure domestic abuse support": [
            "/questions/relationship-safety-domestic-abuse-help/",
            "/resources/govuk-domestic-abuse-help/",
        ],
    }
    for case in data["cases"]:
        if case["query"] in changes:
            case["acceptable_routes"] = changes[case["query"]]
    path.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")


def main() -> None:
    build = ROOT / "scripts" / "build_site.py"
    replace_once(build, "V10_ROUTE_COUNT = 274", "V10_ROUTE_COUNT = 292")
    replace_once(build, "_compat09__V09_ROUTE_COUNT = 212", "_compat09__V09_ROUTE_COUNT = 230")
    replace_once(
        build,
        "('Relationships & family', ['autistic-parent-support-uk', 'communication-needs-in-relationships', 'neurodivergent-parent-overwhelmed-by-admin'])",
        "('Relationships & family', ['autistic-parent-support-uk', 'communication-needs-in-relationships', 'neurodivergent-parent-overwhelmed-by-admin', 'friendship-misunderstandings-neurodivergent', 'partner-communication-processing-sensory-needs', 'boundaries-neurodivergent-relationships', 'conflict-repair-processing-time-relationships', 'intimacy-consent-sensory-communication', 'parenting-neurodivergent-child-uk', 'disabled-neurodivergent-parent-service-access-uk', 'family-events-sensory-social-load', 'relationship-safety-domestic-abuse-help', 'should-i-leave-or-stay-relationship-boundary'])",
    )

    update_question(
        "partner-communication-processing-sensory-needs",
        question="How can partners handle routine changes, written communication, processing time and sensory needs?",
    )
    update_question(
        "conflict-repair-processing-time-relationships",
        question="How can I pause and return to a difficult conversation when communication or shutdown is hard to process?",
    )
    update_question(
        "should-i-leave-or-stay-relationship-boundary",
        question="Can ND Oracle tell me whether I should leave or stay with a partner?",
    )
    update_benchmark()

    healthcare = ROOT / "tests" / "test_v12_healthcare_parity.py"
    replace_once(
        healthcare,
        "    def test_current_governed_object_counts(self) -> None:\n        counts = {\n            kind: len(list((OBJECTS / kind).glob(\"*.json\")))\n            for kind in (\"concepts\", \"resources\", \"questions\", \"evidence\")\n        }\n        self.assertEqual({\"concepts\": 20, \"resources\": 91, \"questions\": 76, \"evidence\": 3}, counts)\n        self.assertEqual(190, sum(counts.values()))\n",
        "    def test_v12_governed_object_floor_is_preserved(self) -> None:\n        counts = {\n            kind: len(list((OBJECTS / kind).glob(\"*.json\")))\n            for kind in (\"concepts\", \"resources\", \"questions\", \"evidence\")\n        }\n        self.assertEqual(20, counts[\"concepts\"])\n        self.assertGreaterEqual(counts[\"resources\"], 91)\n        self.assertGreaterEqual(counts[\"questions\"], 76)\n        self.assertEqual(3, counts[\"evidence\"])\n        self.assertGreaterEqual(sum(counts.values()), 190)\n",
    )

    need = ROOT / "tests" / "test_v12_need_coverage.py"
    replace_once(
        need,
        "    def test_expected_governed_object_counts(self) -> None:\n        counts = {\n            kind: len(list((OBJECTS / kind).glob(\"*.json\")))\n            for kind in (\"concepts\", \"resources\", \"questions\", \"evidence\")\n        }\n        self.assertEqual({\"concepts\": 20, \"resources\": 91, \"questions\": 76, \"evidence\": 3}, counts)\n        self.assertEqual(190, sum(counts.values()))\n",
        "    def test_v12_governed_object_floor_is_preserved(self) -> None:\n        counts = {\n            kind: len(list((OBJECTS / kind).glob(\"*.json\")))\n            for kind in (\"concepts\", \"resources\", \"questions\", \"evidence\")\n        }\n        self.assertEqual(20, counts[\"concepts\"])\n        self.assertGreaterEqual(counts[\"resources\"], 91)\n        self.assertGreaterEqual(counts[\"questions\"], 76)\n        self.assertEqual(3, counts[\"evidence\"])\n        self.assertGreaterEqual(sum(counts.values()), 190)\n",
    )

    release = ROOT / "tests" / "test_release_state_integrity.py"
    replace_once(
        release,
        "    def test_current_corpus_and_route_counts_match_build_contract(self) -> None:\n        current = load_current()\n        corpus = current[\"corpus\"]\n        self.assertEqual(len(build_site.load_concepts()), corpus[\"concepts\"])\n        self.assertEqual(len(build_site.load_resources()), corpus[\"resources\"])\n        self.assertEqual(len(build_site.load_questions()), corpus[\"questions\"])\n        self.assertEqual(len(build_site.load_evidence()), corpus[\"evidence_objects\"])\n        self.assertEqual(\n            corpus[\"concepts\"] + corpus[\"resources\"] + corpus[\"questions\"] + corpus[\"evidence_objects\"],\n            corpus[\"governed_objects\"],\n        )\n        self.assertEqual(build_site.V10_ROUTE_COUNT, current[\"verification\"][\"canonical_routes_verified\"])\n        self.assertEqual(274, build_site.V10_ROUTE_COUNT)\n        self.assertEqual(190, corpus[\"governed_objects\"])\n",
        "    def test_accepted_production_remains_a_floor_while_repository_head_may_advance(self) -> None:\n        current = load_current()\n        corpus = current[\"corpus\"]\n        self.assertEqual(\n            corpus[\"concepts\"] + corpus[\"resources\"] + corpus[\"questions\"] + corpus[\"evidence_objects\"],\n            corpus[\"governed_objects\"],\n        )\n        self.assertEqual(190, corpus[\"governed_objects\"])\n        self.assertEqual(274, current[\"verification\"][\"canonical_routes_verified\"])\n        self.assertGreaterEqual(len(build_site.load_concepts()), corpus[\"concepts\"])\n        self.assertGreaterEqual(len(build_site.load_resources()), corpus[\"resources\"])\n        self.assertGreaterEqual(len(build_site.load_questions()), corpus[\"questions\"])\n        self.assertGreaterEqual(len(build_site.load_evidence()), corpus[\"evidence_objects\"])\n        self.assertGreaterEqual(build_site.V10_ROUTE_COUNT, current[\"verification\"][\"canonical_routes_verified\"])\n",
    )

    readme = ROOT / "README.md"
    replace_once(
        readme,
        "The current repository and accepted production corpus contain exactly 190 governed objects:\n\n- 20 reviewed Concept objects;\n- 91 reviewed Resource objects spanning tools/apps, accessibility and AAC, practical guides, games, work/study support, organisations, services, books and media;\n- 76 reviewed Question objects that route ordinary practical needs across governed Concepts and Resources;\n- 3 normalized v0.2 Evidence objects plus 57 accepted legacy v0.1 embedded source records, giving 60 governed source records across 49 governed Claims. The authoritative object count is 190 because legacy source projections are not duplicated into new objects.\n",
        "The current repository candidate contains exactly 208 governed objects, while the accepted production corpus remains the separately recorded 190-object deployment described under **Production state** below:\n\n- 20 reviewed Concept objects;\n- 99 reviewed Resource objects spanning tools/apps, accessibility and AAC, practical guides, games, work/study support, organisations, services, books and media;\n- 86 reviewed Question objects that route ordinary practical needs across governed Concepts and Resources;\n- 3 normalized v0.2 Evidence objects plus 57 accepted legacy v0.1 embedded source records, giving 60 governed source records across 49 governed Claims. The repository candidate object count is 208 because legacy source projections are not duplicated into new objects.\n\nThe Relationships & family UK v1 candidate adds bounded friendship, partner, boundaries/conflict, intimacy/consent, parenting and disabled-parent access routes while preserving the existing clinical, jurisdiction, evidence, privacy and non-recommendation boundaries. It is not production until separately merged, deployed and verified through the protected exact-SHA release process.\n",
    )


if __name__ == "__main__":
    main()
