from __future__ import annotations

import json
import re
import unittest

from scripts import discovery

CLINICAL_DIAGNOSIS = [
    "Could these symptoms mean autism?", "Does this sound like ADHD?", "Can you tell whether I am autistic?",
    "Do these traits look autistic to you?", "Would you say I have ADHD?", "Is this enough to say I am autistic?",
    "Based on this am I probably ADHD?", "Does my behaviour mean I have autism?", "Could I be on the autism spectrum?",
    "Do my problems point to ADHD?", "Am I likely to be autistic from these signs?", "Can you work out if I have ADHD?",
    "Is this basically an autism diagnosis?", "Do these answers prove I am autistic?", "Does this checklist show I have ADHD?",
    "Would these symptoms qualify as autism?", "Tell me whether these are ADHD symptoms in me", "Can you confirm I am autistic?",
    "Is my executive dysfunction definitely ADHD?", "Is my sensory overload proof of autism?",
]

CLINICAL_MEDICATION = [
    "Should I take more ADHD medication?", "Should I increase my ADHD tablets?", "Can I skip my ADHD meds today?",
    "Should I lower my ADHD dose?", "Can I double my ADHD medication tomorrow?", "Should I stop taking my ADHD tablets for a week?",
    "Is it safe for me to take an extra ADHD tablet?", "Should I switch ADHD medicines?", "Can I take my stimulant later than usual?",
    "I missed my ADHD dose, should I take it now?", "My ADHD medicine feels too weak, should I take more?",
    "My ADHD medicine makes me anxious, should I reduce it?", "Can I split my ADHD tablet in half?",
    "Should I change from one ADHD drug to another?", "Can I stop my stimulant suddenly?", "Should I take less medication on weekends?",
    "Can I change the time I take my ADHD medication?", "My medication is not working, what should I change?",
    "What should I do with my dose if I cannot sleep?", "Can I take another dose because the first wore off?",
]

CLINICAL_POSITIVE = [
    "what is autism", "what is ADHD", "how is autism diagnosed in adults", "how is ADHD diagnosed in adults",
    "what does an autism assessment usually involve", "what does an ADHD assessment usually involve",
    "what is stimulant medication", "what does NICE say about ADHD diagnosis", "where can I read NHS information about adult ADHD",
    "where can I read autism information", "what is executive function", "what is sensory processing", "what is masking",
    "what is autistic burnout", "what is dyslexia", "what is Tourette syndrome",
]

ORIENTATION_PAIRS = [
    ("what is autism", "/understand/autism/", "how do I get an adult autism assessment in England", "/questions/adult-autism-assessment-england/"),
    ("what is ADHD", "/understand/adhd/", "how do I get an adult ADHD assessment in England", "/questions/adult-adhd-assessment-england/"),
    ("what is dyslexia", "/understand/dyslexia/", "where can I find dyslexia information and support in the UK", "/questions/dyslexia-information-and-support-uk/"),
    ("what is dyscalculia", "/understand/dyscalculia/", "where can I find dyscalculia information and support in the UK", "/questions/dyscalculia-information-and-support-uk/"),
    ("what is Tourette syndrome", "/understand/tourette-syndrome/", "where can I find Tourette information and support in the UK", "/questions/tourette-information-and-support-uk/"),
    ("what is developmental language disorder", "/understand/developmental-language-disorder/", "where can I find DLD information and support", "/questions/dld-information-and-support/"),
    ("what is dyspraxia", "/understand/developmental-coordination-disorder/", "where can I find adult dyspraxia information in the UK", "/questions/adult-dyspraxia-information-uk/"),
    ("what is sensory overload", "/understand/sensory-overload/", "what can I change when sensory input overwhelms me", "/questions/sensory-overload-what-can-i-change/"),
    ("what are communication differences", "/understand/communication-differences/", "how can I explain my communication needs in a relationship", "/questions/communication-needs-in-relationships/"),
    ("what is task initiation", "/understand/task-initiation/", "I cannot get started and keep losing track of tasks", "/questions/task-starting-and-organisation/"),
]

BENIGN_OUT_OF_DOMAIN = [
    "how do I make tea", "where do I buy stamps", "can I grow tomatoes", "how do I fix a bicycle", "what time is sunset",
    "need help choosing paint", "how do I wash a coat", "where can I recycle glass", "how do I sharpen a pencil",
    "booking a restaurant table", "recipe for vegetable soup", "how do I change a light bulb", "where do I find a plumber",
    "my printer has no ink", "train timetable to London", "how do I clean a window", "how do I plant potatoes",
    "need ideas for a birthday cake", "where can I buy batteries", "how do I mend a chair",
]

JURISDICTIONS = {
    "England": {"England", "Great Britain", "England and Wales", "UK"},
    "Scotland": {"Scotland", "Great Britain", "UK"},
    "Wales": {"Wales", "Great Britain", "England and Wales", "UK"},
    "Northern Ireland": {"Northern Ireland", "UK"},
}


def route_scope(route: str) -> str | None:
    if "northern-ireland" in route:
        return "Northern Ireland"
    if "great-britain" in route:
        return "Great Britain"
    if "england-wales" in route:
        return "England and Wales"
    if "scotland" in route:
        return "Scotland"
    if "wales" in route:
        return "Wales"
    if "england" in route:
        return "England"
    if route.endswith("-uk/") or "-uk/" in route:
        return "UK"
    return None


def swap_scope(title: str, target: str) -> str:
    value = title
    for marker in ["Northern Ireland", "Great Britain", "England and Wales", "Scotland", "England", "Wales", "the UK", "UK"]:
        value = re.sub(re.escape(marker), target, value, flags=re.IGNORECASE)
    return value


def compact(query: str) -> dict:
    mode, results = discovery.search(query, limit=5)
    return {"query": query, "mode": mode, "results": [{"route": r.route, "score": r.score} for r in results]}


class Issue109EvidenceBatch3(unittest.TestCase):
    def test_emit_batch3_evidence(self) -> None:
        diagnosis_failures = [row for row in (compact(q) for q in CLINICAL_DIAGNOSIS) if row["mode"] != "no_answer"]
        medication_failures = [row for row in (compact(q) for q in CLINICAL_MEDICATION) if row["mode"] != "no_answer"]
        positive_false_refusals = [row for row in (compact(q) for q in CLINICAL_POSITIVE) if row["mode"] == "no_answer"]
        print("E109B3_CLINICAL", json.dumps({
            "diagnosis_total": len(CLINICAL_DIAGNOSIS), "diagnosis_escaped": len(diagnosis_failures),
            "medication_total": len(CLINICAL_MEDICATION), "medication_escaped": len(medication_failures),
            "positive_total": len(CLINICAL_POSITIVE), "positive_false_refusals": len(positive_false_refusals),
            "diagnosis_failures": diagnosis_failures, "medication_failures": medication_failures,
            "positive_failures": positive_false_refusals,
        }, sort_keys=True))

        index = discovery.build_index()
        scoped_records = [r for r in index if route_scope(r["route"]) is not None]
        jurisdiction_rows = []
        incompatible_top1 = []
        for record in scoped_records:
            source_scope = route_scope(record["route"])
            for jurisdiction in JURISDICTIONS:
                query = swap_scope(record["title"], jurisdiction)
                row = compact(query)
                top_route = row["results"][0]["route"] if row["results"] else None
                top_scope = route_scope(top_route) if top_route else None
                incompatible = bool(top_scope and top_scope not in JURISDICTIONS[jurisdiction])
                evidence = {"source_route": record["route"], "source_scope": source_scope,
                            "query_jurisdiction": jurisdiction, "query": query, "top_route": top_route,
                            "top_scope": top_scope, "incompatible_top1": incompatible}
                jurisdiction_rows.append(evidence)
                if incompatible:
                    incompatible_top1.append(evidence)
        print("E109B3_JURISDICTION", json.dumps({
            "scoped_records": len(scoped_records), "probe_total": len(jurisdiction_rows),
            "incompatible_top1": len(incompatible_top1), "failures": incompatible_top1,
        }, sort_keys=True))

        orientation_failures = []
        action_failures = []
        orientation_rows = []
        for info_query, info_route, action_query, action_route in ORIENTATION_PAIRS:
            info = compact(info_query); action = compact(action_query)
            info_top = info["results"][0]["route"] if info["results"] else None
            action_top = action["results"][0]["route"] if action["results"] else None
            row = {"info_query": info_query, "expected_info": info_route, "info_top": info_top,
                   "action_query": action_query, "expected_action": action_route, "action_top": action_top}
            orientation_rows.append(row)
            if info_top != info_route:
                orientation_failures.append(row)
            if action_top != action_route:
                action_failures.append(row)
        print("E109B3_ORIENTATION", json.dumps({
            "pair_total": len(ORIENTATION_PAIRS), "info_wrong_top1": len(orientation_failures),
            "action_wrong_top1": len(action_failures), "info_failures": orientation_failures,
            "action_failures": action_failures, "rows": orientation_rows,
        }, sort_keys=True))

        title_tokens: dict[str, int] = {}
        for record in index:
            for token in set(discovery._tokens(record["title"])):
                title_tokens[token] = title_tokens.get(token, 0) + 1
        token_rows = []
        for token, title_occurrences in title_tokens.items():
            mode, results = discovery.search(token, limit=200, index=index)
            token_rows.append({"token": token, "title_occurrences": title_occurrences,
                               "eligible_results": len(results) if mode == "results" else 0,
                               "top_score": results[0].score if results else 0,
                               "top_route": results[0].route if results else None})
        token_rows.sort(key=lambda row: (-row["eligible_results"], -row["top_score"], row["token"]))
        benign_false_positives = [row for row in (compact(q) for q in BENIGN_OUT_OF_DOMAIN) if row["mode"] == "results"]
        print("E109B3_PRECISION", json.dumps({
            "single_title_tokens_tested": len(token_rows), "top_damaging_tokens": token_rows[:30],
            "benign_total": len(BENIGN_OUT_OF_DOMAIN), "benign_false_positive_count": len(benign_false_positives),
            "benign_false_positives": benign_false_positives,
        }, sort_keys=True))
        self.assertTrue(True)
