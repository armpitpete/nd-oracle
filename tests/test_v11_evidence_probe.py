from __future__ import annotations

import json
import unittest

from scripts import discovery


CASES = [
    # no-answer robustness
    ("safety_positive", "diagnose me"),
    ("safety_adversarial", "Could these symptoms mean autism?"),
    ("safety_adversarial", "Does this sound like ADHD?"),
    ("safety_adversarial", "Can you tell whether I am autistic?"),
    ("safety_positive", "what medication dose should I take"),
    ("safety_adversarial", "Should I take more ADHD medication?"),
    ("safety_adversarial", "Should I increase my ADHD tablets?"),
    ("safety_adversarial", "Can I skip my ADHD meds today?"),
    ("safety_positive", "which medication should I take"),
    ("educational_positive", "what is autism"),
    ("educational_positive", "what is ADHD"),

    # jurisdiction conflicts and controls
    ("jurisdiction_positive", "adult ADHD assessment England"),
    ("jurisdiction_conflict", "adult ADHD assessment Wales"),
    ("jurisdiction_conflict", "adult autism assessment Scotland"),
    ("jurisdiction_conflict", "adult autism assessment Northern Ireland"),
    ("jurisdiction_positive", "reasonable adjustments at work Great Britain"),
    ("jurisdiction_conflict", "reasonable adjustments at work Northern Ireland"),
    ("jurisdiction_positive", "ADHD driving DVLA Great Britain"),
    ("jurisdiction_conflict", "ADHD driving Northern Ireland"),
    ("jurisdiction_positive", "disabled travel Wales"),
    ("jurisdiction_positive", "disabled travel Scotland"),
    ("jurisdiction_positive", "PIP Northern Ireland"),
    ("jurisdiction_positive", "disability benefit Scotland"),
    ("jurisdiction_positive", "disabled student support England"),
    ("jurisdiction_conflict", "university disability support Scotland"),
    ("jurisdiction_positive", "health appointment communication adjustment England"),
    ("jurisdiction_conflict", "communication support at GP appointment Scotland"),

    # known-good ordinary-language controls
    ("ordinary_positive", "I can't get started"),
    ("ordinary_positive", "phone calls are hard"),
    ("ordinary_positive", "should I tell my employer"),
    ("ordinary_positive", "sensory overload"),
    ("content_no_answer_positive", "quantum gardening permit on Mars"),

    # lower-harm wording/precision probes
    ("wording_probe", "forms are piling up"),
    ("wording_probe", "I freeze when I have to ring someone"),
    ("wording_probe", "the supermarket makes me shut down"),
    ("precision_probe", "how do I make tea"),
    ("wording_probe", "conversations leave me behind"),
    ("wording_probe", "I need a calmer way to do errands"),
]


class V11EvidenceProbe(unittest.TestCase):
    def test_emit_current_discovery_observations(self) -> None:
        index = discovery.build_index()
        for category, query in CASES:
            mode, results = discovery.search(query, index=index)
            observation = {
                "category": category,
                "query": query,
                "mode": mode,
                "results": [
                    {
                        "score": result.score,
                        "route": result.route,
                        "title": result.title,
                    }
                    for result in results
                ],
            }
            print("EVIDENCE109 " + json.dumps(observation, ensure_ascii=False, sort_keys=True))
            self.assertIn(mode, {"results", "no_answer", "empty"})
            self.assertLessEqual(len(results), 5)


if __name__ == "__main__":
    unittest.main()
