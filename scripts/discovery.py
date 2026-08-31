from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OBJECTS = ROOT / "objects"

STOP_WORDS = {
    "a", "an", "and", "are", "can", "do", "for", "i", "in", "is", "it", "me",
    "my", "of", "on", "or", "the", "to", "what", "with", "you", "your",
}

# Editorial phrases are routing hints, not claims. They let ordinary wording reach
# governed objects without changing those objects' evidence status.
INTENT_PHRASES: dict[str, tuple[str, ...]] = {
    "/questions/task-starting-and-organisation/": (
        "can't get started", "cannot get started", "keep putting things off", "paperwork piles up",
        "starting tasks", "organising tasks", "procrastinating admin",
    ),
    "/questions/make-noisy-bright-place-easier/": (
        "too noisy", "too bright", "busy places overwhelm me", "office noise", "bright lights",
    ),
    "/questions/sensory-overload-what-can-i-change/": (
        "sensory overload", "everything feels too much", "overwhelmed by sound", "overwhelmed by light",
    ),
    "/questions/phone-calls-are-difficult/": (
        "phone calls are hard", "hate phone calls", "can't use the phone", "telephone anxiety",
    ),
    "/questions/processing-time-in-conversations-meetings/": (
        "need more time to answer", "processing time", "meetings move too fast", "people interrupt before i answer",
    ),
    "/questions/aac-and-nonspeaking-communication/": (
        "can't speak sometimes", "non speaking", "nonspeaking", "aac", "alternative communication",
    ),
    "/questions/reasonable-adjustments-at-work-great-britain/": (
        "adjustments at work", "workplace adjustments", "work is too noisy", "reasonable adjustments",
    ),
    "/questions/workplace-support-great-britain/": (
        "help staying in work", "support at work", "access to work", "equipment for work disability",
    ),
    "/questions/disclosing-disability-neurodivergence-at-work/": (
        "should i tell my employer", "disclose autism at work", "disclose adhd at work", "tell work i'm neurodivergent",
    ),
    "/questions/job-interview-adjustments-great-britain/": (
        "interview adjustments", "job interview disability", "adjustment for interview",
    ),
    "/questions/disabled-student-support-england/": (
        "help at university", "disabled student support", "dsa", "support with study costs",
    ),
    "/questions/organising-study-and-assignments/": (
        "can't organise assignments", "study organisation", "deadlines at university", "starting coursework",
    ),
    "/questions/adult-autism-assessment-england/": (
        "autism assessment adult", "getting assessed for autism", "adult autism diagnosis england",
    ),
    "/questions/adult-adhd-assessment-england/": (
        "adhd assessment adult", "getting assessed for adhd", "adult adhd diagnosis england",
    ),
    "/questions/masking-exhaustion-and-autistic-burnout/": (
        "exhausted from masking", "autistic burnout", "masking all day", "too exhausted to function after socialising",
    ),
    "/questions/sleep-and-winding-down-routines/": (
        "can't wind down", "sleep routine", "brain won't switch off at night",
    ),
    "/questions/meal-planning-and-everyday-food-tasks/": (
        "forget to eat", "meal planning is hard", "cooking feels impossible", "food admin",
    ),
    "/questions/dyscalculia-information-and-support-uk/": (
        "numbers make no sense", "dyscalculia", "maths difficulty", "difficulty with numbers",
    ),
    "/questions/autistic-parent-support-uk/": (
        "autistic parent", "neurodivergent parent", "parenting while autistic",
    ),
    "/questions/make-device-easier-to-use/": (
        "make my phone easier", "computer accessibility", "device accessibility", "text is hard to read on screen",
    ),
    "/questions/low-time-pressure-games/": (
        "relaxing games", "games without time pressure", "low pressure games", "calm game",
    ),
    "/understand/monotropism/": ("attention tunnel", "monotropism", "deep narrow attention"),
    "/understand/interoception/": ("can't tell when hungry", "body signals", "interoception", "don't notice thirst"),
    "/understand/alexithymia/": ("can't identify emotions", "don't know what i'm feeling", "alexithymia"),
    "/understand/stimming/": ("why do i stim", "repetitive movement", "stimming"),
    "/understand/communication-differences/": ("communication differences", "misunderstand people", "communication feels hard"),
    "/understand/task-initiation/": ("task initiation", "want to do it but can't start"),
    "/resources/access-to-work/": ("access to work grant", "government workplace support"),
    "/resources/acas-reasonable-adjustments/": ("acas adjustments", "employment adjustment guidance"),
    "/resources/disabled-students-allowance/": ("student finance disability support", "disabled students allowance"),
}

REFUSAL_PATTERNS = (
    "diagnose me", "am i autistic", "do i have autism", "do i have adhd",
    "what medication dose", "what dose should i take", "stop my medication",
    "which medication should i take", "tell me if i am autistic", "tell me if i have adhd",
)


@dataclass(frozen=True)
class SearchResult:
    route: str
    kind: str
    object_id: str
    title: str
    excerpt: str
    score: int


def _normalise(value: str) -> str:
    return " ".join(re.findall(r"[a-z0-9]+", value.casefold()))


def _tokens(value: str) -> list[str]:
    return [token for token in _normalise(value).split() if token not in STOP_WORDS and len(token) > 1]


def _load_dir(name: str) -> list[dict]:
    directory = OBJECTS / name
    if not directory.is_dir():
        return []
    output = []
    for path in sorted(directory.glob("*.json")):
        output.append(json.loads(path.read_text(encoding="utf-8")))
    return output


def build_index() -> list[dict]:
    records: list[dict] = []
    for item in _load_dir("questions"):
        title = item["question"]
        body = " ".join([
            item.get("why_it_matters", ""), item.get("current_understanding", ""),
            *item.get("evidence_needed", []), *item.get("dissent", []),
        ])
        route = f"/questions/{item['id']}/"
        records.append({"route": route, "kind": "Question", "id": item["id"], "title": title, "body": body})
    for item in _load_dir("concepts"):
        title = item["name"]
        claim_text = " ".join(claim.get("text", "") for claim in item.get("claims", []))
        aliases = " ".join(item.get("aliases", []))
        body = " ".join([item.get("summary", ""), aliases, claim_text])
        route = f"/understand/{item['id']}/"
        records.append({"route": route, "kind": "Topic", "id": item["id"], "title": title, "body": body})
    for item in _load_dir("resources"):
        title = item["name"]
        body = " ".join([
            item.get("description", ""), item.get("intended_use", ""), item.get("audience_or_context", ""),
            *item.get("limitations", []), *item.get("cost_or_access_notes", []),
        ])
        route = f"/resources/{item['id']}/"
        records.append({"route": route, "kind": "Resource", "id": item["id"], "title": title, "body": body})
    return sorted(records, key=lambda item: (item["kind"], item["title"].casefold()))


def _score(query: str, record: dict) -> int:
    qnorm = _normalise(query)
    if not qnorm:
        return 0
    qtokens = set(_tokens(query))
    title_norm = _normalise(record["title"])
    body_norm = _normalise(record["body"])
    score = 0
    if qnorm == title_norm:
        score += 120
    elif qnorm in title_norm:
        score += 55
    if qnorm and qnorm in body_norm:
        score += 20
    title_tokens = set(_tokens(record["title"]))
    body_tokens = set(_tokens(record["body"]))
    score += 12 * len(qtokens & title_tokens)
    score += 3 * len(qtokens & body_tokens)
    for phrase in INTENT_PHRASES.get(record["route"], ()):
        phrase_norm = _normalise(phrase)
        phrase_tokens = set(_tokens(phrase))
        if qnorm == phrase_norm:
            score += 100
        elif qnorm in phrase_norm or phrase_norm in qnorm:
            score += 45
        score += 9 * len(qtokens & phrase_tokens)
    return score


def search(query: str, *, limit: int = 5, index: list[dict] | None = None) -> tuple[str, list[SearchResult]]:
    qnorm = _normalise(query)
    if not qnorm:
        return "empty", []
    if any(pattern in qnorm for pattern in REFUSAL_PATTERNS):
        return "no_answer", []
    if index is None:
        index = build_index()
    ranked = []
    for record in index:
        score = _score(query, record)
        if score >= 12:
            ranked.append((score, record["kind"], record["title"].casefold(), record))
    ranked.sort(key=lambda item: (-item[0], item[1], item[2]))
    results = [
        SearchResult(
            route=record["route"], kind=record["kind"], object_id=record["id"],
            title=record["title"], excerpt=record["body"][:220].strip(), score=score,
        )
        for score, _kind, _title, record in ranked[:limit]
    ]
    return ("results" if results else "no_answer"), results


def browser_index_json() -> str:
    payload = []
    for record in build_index():
        payload.append({
            **record,
            "intent": list(INTENT_PHRASES.get(record["route"], ())),
        })
    return json.dumps(payload, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Run deterministic ND Oracle governed discovery.")
    parser.add_argument("query")
    args = parser.parse_args()
    mode, results = search(args.query)
    print(mode)
    for item in results:
        print(f"{item.score:3d} {item.route} {item.title}")
