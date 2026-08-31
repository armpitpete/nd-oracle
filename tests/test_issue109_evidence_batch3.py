from __future__ import annotations

import json
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

# Scope is taken from the governed title/audience/current-understanding of the
# current catalogue, not inferred from a publisher name. UK-wide routes are
# omitted because all four nations are compatible by definition.
SCOPED_ROUTES = {
    "/questions/adhd-driving-dvla-great-britain/": ("Great Britain", "ADHD driving notification"),
    "/questions/workplace-support-great-britain/": ("Great Britain", "workplace disability support"),
    "/questions/job-interview-adjustments-great-britain/": ("Great Britain", "job interview disability adjustments"),
    "/questions/reasonable-adjustments-at-work-great-britain/": ("Great Britain", "reasonable adjustments at work"),
    "/questions/adult-adhd-assessment-england/": ("England", "adult ADHD assessment"),
    "/questions/adult-autism-assessment-england/": ("England", "adult autism assessment"),
    "/questions/disabled-student-support-england/": ("England", "university disability support"),
    "/questions/send-support-school-college-england/": ("England", "SEND school college support"),
    "/questions/healthcare-communication-adjustments-england/": ("England", "health appointment communication adjustments"),
    "/questions/disabled-travel-support-scotland/": ("Scotland", "disabled concessionary travel"),
    "/questions/disabled-travel-support-wales/": ("Wales", "disabled concessionary travel"),
    "/questions/disabled-travel-support-northern-ireland/": ("Northern Ireland", "disabled concessionary travel"),
    "/resources/access-to-work/": ("Great Britain", "Access to Work"),
    "/resources/acas-reasonable-adjustments/": ("Great Britain", "Acas reasonable adjustments at work"),
    "/resources/govuk-adhd-driving/": ("Great Britain", "GOV.UK ADHD driving"),
    "/resources/govuk-pip-england-wales/": ("England and Wales", "personal independence payment PIP"),
    "/resources/nhs-england-accessible-information-adjustments/": ("England", "NHS accessible information reasonable adjustments"),
    "/resources/disabled-students-allowance/": ("England", "disabled students allowance DSA"),
    "/resources/ipsea/": ("England", "SEND legal advice IPSEA"),
    "/resources/govuk-send-code-practice/": ("England", "SEND code of practice"),
    "/resources/nhs-adhd-adults/": ("England", "NHS adult ADHD information assessment"),
    "/resources/autism-central-adult-diagnosis/": ("England", "Autism Central adult diagnosis"),
    "/resources/nice-adhd-guideline/": ("England and Wales", "NICE ADHD diagnosis management"),
    "/resources/nice-autism-adults-guideline/": ("England and Wales", "NICE adult autism diagnosis management"),
    "/resources/scotland-adult-disability-payment/": ("Scotland", "adult disability payment"),
    "/resources/scotland-disabled-bus-pass/": ("Scotland", "disabled bus pass"),
    "/resources/wales-disabled-concessionary-travel/": ("Wales", "disabled concessionary travel card"),
    "/resources/northern-ireland-disabled-concessionary-travel/": ("Northern Ireland", "disabled concessionary travel"),
    "/resources/nidirect-pip/": ("Northern Ireland", "PIP nidirect"),
}

JURISDICTIONS = ["England", "Scotland", "Wales", "Northern Ireland"]
COMPATIBLE = {
    "England": {"England"},
    "Scotland": {"Scotland"},
    "Wales": {"Wales"},
    "Northern Ireland": {"Northern Ireland"},
    "Great Britain": {"England", "Scotland", "Wales"},
    "England and Wales": {"England", "Wales"},
}
GENERIC_RISK_TOKENS = {"how", "where", "need", "help", "support", "find", "information", "work", "should", "change", "use", "adult"}


def compact(query: str) -> dict:
    mode, results = discovery.search(query, limit=5)
    return {"query": query, "mode": mode, "results": [{"route": r.route, "score": r.score} for r in results]}


def refusal_hit(query: str) -> bool:
    qnorm = discovery._normalise(query)
    return any(pattern in qnorm for pattern in discovery.REFUSAL_PATTERNS)


def scoped_top(route: str | None) -> str | None:
    if route in SCOPED_ROUTES:
        return SCOPED_ROUTES[route][0]
    if route and (route.endswith("-uk/") or "-uk/" in route):
        return "UK"
    return None


class Issue109EvidenceBatch3(unittest.TestCase):
    def test_emit_batch3_evidence(self) -> None:
        diagnosis_missed = [q for q in CLINICAL_DIAGNOSIS if not refusal_hit(q)]
        medication_missed = [q for q in CLINICAL_MEDICATION if not refusal_hit(q)]
        diagnosis_accidental_no_answer = [q for q in diagnosis_missed if compact(q)["mode"] == "no_answer"]
        medication_accidental_no_answer = [q for q in medication_missed if compact(q)["mode"] == "no_answer"]
        positive_false_boundary = [q for q in CLINICAL_POSITIVE if refusal_hit(q)]
        positive_no_coverage = [q for q in CLINICAL_POSITIVE if compact(q)["mode"] == "no_answer" and not refusal_hit(q)]
        print("E109B3_CLINICAL_CORRECTED", json.dumps({
            "diagnosis_total": len(CLINICAL_DIAGNOSIS), "diagnosis_boundary_missed": len(diagnosis_missed),
            "diagnosis_accidental_no_answer": diagnosis_accidental_no_answer,
            "medication_total": len(CLINICAL_MEDICATION), "medication_boundary_missed": len(medication_missed),
            "medication_accidental_no_answer": medication_accidental_no_answer,
            "positive_total": len(CLINICAL_POSITIVE), "positive_false_boundary_hits": positive_false_boundary,
            "positive_no_coverage_not_refusal": positive_no_coverage,
        }, sort_keys=True))

        index_routes = {record["route"] for record in discovery.build_index()}
        missing_inventory = sorted(set(SCOPED_ROUTES) - index_routes)
        conflict_rows = []
        compatible_rows = []
        incompatible_top1 = []
        source_leak_top1 = []
        for source_route, (scope, stem) in SCOPED_ROUTES.items():
            for jurisdiction in JURISDICTIONS:
                query = f"{stem} {jurisdiction}"
                row = compact(query)
                top_route = row["results"][0]["route"] if row["results"] else None
                top_scope = scoped_top(top_route)
                is_compatible_query = jurisdiction in COMPATIBLE[scope]
                evidence = {"source_route": source_route, "source_scope": scope, "query": query,
                            "query_jurisdiction": jurisdiction, "top_route": top_route, "top_scope": top_scope}
                if is_compatible_query:
                    compatible_rows.append(evidence)
                else:
                    conflict_rows.append(evidence)
                    if top_scope not in {None, "UK"} and jurisdiction not in COMPATIBLE[top_scope]:
                        incompatible_top1.append(evidence)
                    if top_route == source_route:
                        source_leak_top1.append(evidence)
        print("E109B3_JURISDICTION_CORRECTED", json.dumps({
            "scoped_route_inventory": len(SCOPED_ROUTES), "missing_from_index": missing_inventory,
            "conflict_probe_total": len(conflict_rows), "conflict_incompatible_top1": len(incompatible_top1),
            "conflict_source_route_still_top1": len(source_leak_top1),
            "compatible_probe_total": len(compatible_rows), "failures": incompatible_top1,
            "source_leaks": source_leak_top1,
        }, sort_keys=True))

        info_failures = []
        action_failures = []
        for info_query, info_route, action_query, action_route in ORIENTATION_PAIRS:
            info = compact(info_query); action = compact(action_query)
            info_top = info["results"][0]["route"] if info["results"] else None
            action_top = action["results"][0]["route"] if action["results"] else None
            row = {"info_query": info_query, "expected_info": info_route, "info_top": info_top,
                   "action_query": action_query, "expected_action": action_route, "action_top": action_top}
            if info_top != info_route:
                info_failures.append(row)
            if action_top != action_route:
                action_failures.append(row)
        print("E109B3_ORIENTATION_CORRECTED", json.dumps({
            "pair_total": len(ORIENTATION_PAIRS), "info_wrong_top1": len(info_failures),
            "action_wrong_top1": len(action_failures), "info_failures": info_failures,
            "action_failures": action_failures,
        }, sort_keys=True))

        index = discovery.build_index()
        title_tokens = sorted({token for record in index for token in discovery._tokens(record["title"])})
        token_rows = []
        for token in title_tokens:
            mode, results = discovery.search(token, limit=200, index=index)
            count = len(results) if mode == "results" else 0
            token_rows.append({"token": token, "eligible_results": count,
                               "top_score": results[0].score if results else 0,
                               "top_route": results[0].route if results else None})
        token_rows.sort(key=lambda row: (-row["eligible_results"], -row["top_score"], row["token"]))
        generic_rows = [row for row in token_rows if row["token"] in GENERIC_RISK_TOKENS]
        benign_false_positives = [compact(q) for q in BENIGN_OUT_OF_DOMAIN if compact(q)["mode"] == "results"]
        print("E109B3_PRECISION_CORRECTED", json.dumps({
            "single_title_tokens_tested": len(token_rows), "top_20_all_tokens": token_rows[:20],
            "generic_risk_tokens": generic_rows, "benign_total": len(BENIGN_OUT_OF_DOMAIN),
            "benign_false_positive_count": len(benign_false_positives),
            "benign_false_positives": benign_false_positives,
        }, sort_keys=True))
        self.assertEqual(missing_inventory, [])
