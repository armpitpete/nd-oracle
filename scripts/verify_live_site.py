from __future__ import annotations

import argparse
import html
import sys
import urllib.error
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts import build_site as _builder
from scripts import verify_live_site_v08 as _v08
from scripts.verify_live_site_v08 import *

USER_AGENT = "nd-oracle-live-verifier/0.9"
_v08.USER_AGENT = USER_AGENT
_v08._v06.USER_AGENT = USER_AGENT

RESOURCE_RECORDS = _builder.load_resources()
QUESTION_RECORDS = _builder.load_questions()
CONCEPT_RECORDS = _builder.load_concepts()
RESOURCE_RECORD_MAP = {item["id"]: item for item in RESOURCE_RECORDS}
QUESTION_RECORD_MAP = {item["id"]: item for item in QUESTION_RECORDS}

V08_RESOURCE_IDS = {
    "goblin-tools", "tiimo", "time-timer", "habitica", "unpacking", "minecraft",
    "stardew-valley", "access-to-work", "national-autistic-society", "adhd-uk",
    "autistica", "autistic-self-advocacy-network", "autistica-tips-hub",
    "molehill-mountain", "unmasking-autism", "british-dyslexia-association",
    "tourettes-action", "mencap", "radld", "speech-and-language-uk-adult-dld-support",
    "abilitynet-my-computer-my-way", "acas-reasonable-adjustments",
    "disabled-students-allowance", "scope-support-to-work", "nhs-dyspraxia-adults",
}
V08_QUESTION_IDS = {
    "task-starting-and-organisation", "low-time-pressure-games",
    "workplace-support-great-britain", "autism-information-and-support",
    "autism-anxiety-tools", "dyslexia-information-and-support-uk",
    "tourette-information-and-support-uk", "learning-disability-information-and-support-uk",
    "dld-information-and-support", "make-device-easier-to-use",
    "reasonable-adjustments-at-work-great-britain", "disabled-student-support-england",
    "disabled-person-looking-for-work-uk", "adult-dyspraxia-information-uk",
}

RESOURCE_MARKERS_V09 = {
    f"/resources/{resource['id']}/": (
        resource["name"],
        next(locator["value"] for locator in resource.get("locators", []) if locator.get("type") == "url"),
    )
    for resource in RESOURCE_RECORDS
}
QUESTION_MARKERS_V09 = {
    f"/questions/{question['id']}/": question["question"]
    for question in QUESTION_RECORDS
}
CONCEPT_MARKERS_V09 = {
    f"/understand/{concept['id']}/": concept["name"]
    for concept in CONCEPT_RECORDS
}

NAVIGATION_MARKERS = (
    ("/needs/", "<h1>Browse by need</h1>"),
    ("/needs/daily-life/", "<h1>Daily life</h1>"),
    ("/needs/sensory-environment/", "<h1>Sensory &amp; environment</h1>"),
    ("/needs/communication/", "<h1>Communication</h1>"),
    ("/needs/work/", "<h1>Work</h1>"),
    ("/needs/education-study/", "<h1>Education &amp; study</h1>"),
    ("/needs/assessment-diagnosis/", "<h1>Assessment &amp; diagnosis</h1>"),
    ("/needs/health-wellbeing/", "<h1>Health &amp; wellbeing</h1>"),
    ("/needs/relationships-family/", "<h1>Relationships &amp; family</h1>"),
    ("/types/", "<h1>Browse by content type</h1>"),
    ("/places/", "<h1>Browse by geographic scope</h1>"),
    ("/a-z/", "<h1>A–Z</h1>"),
)

STABLE_BASE_MARKERS = (
    ("/", "Understand neurodivergence without doing all the digging yourself"),
    ("/understand/", "<h1>Understand</h1>"),
    ("/resources/", "<h1>Resources</h1>"),
    ("/tools/", "<h1>Tools &amp; practical help</h1>"),
    ("/games/", "<h1>Games</h1>"),
    ("/community/", "<h1>Support &amp; organisations</h1>"),
    ("/books-media/", "<h1>Books &amp; media</h1>"),
    ("/questions/", "<h1>Questions</h1>"),
    ("/how-it-works/", "<h1>How this site works</h1>"),
    ("/about/", "<h1>About</h1>"),
    ("/accessibility/", "<h1>Accessibility</h1>"),
    ("/feedback/", "<h1>Feedback</h1>"),
    ("/privacy/", "<h1>Privacy</h1>"),
)

V09_ROUTES = (
    *STABLE_BASE_MARKERS[:2],
    *((path, f"<h1>{html.escape(name, quote=True)}</h1>") for path, name in CONCEPT_MARKERS_V09.items()),
    *STABLE_BASE_MARKERS[2:7],
    *((path, f"<h1>{html.escape(name, quote=True)}</h1>") for path, (name, _url) in RESOURCE_MARKERS_V09.items()),
    *STABLE_BASE_MARKERS[7:8],
    *((path, f"<h1>{html.escape(question, quote=True)}</h1>") for path, question in QUESTION_MARKERS_V09.items()),
    *STABLE_BASE_MARKERS[8:],
    *NAVIGATION_MARKERS,
)

if len(V09_ROUTES) != _builder.V09_ROUTE_COUNT:
    raise RuntimeError(
        f"v0.9 verifier route count mismatch: expected {_builder.V09_ROUTE_COUNT}, got {len(V09_ROUTES)}"
    )
if len({path for path, _marker in V09_ROUTES}) != len(V09_ROUTES):
    raise RuntimeError("v0.9 verifier contains duplicate routes")
_builder_paths = set(_builder.sitemap_paths(CONCEPT_RECORDS, RESOURCE_RECORDS, QUESTION_RECORDS))
_verifier_paths = {path for path, _marker in V09_ROUTES}
if _builder_paths != _verifier_paths:
    raise RuntimeError(
        "v0.9 builder/verifier route mismatch: "
        f"missing_from_verifier={sorted(_builder_paths - _verifier_paths)}; "
        f"unexpected_in_verifier={sorted(_verifier_paths - _builder_paths)}"
    )

# Keep the historical public constant frozen for legacy contract tests. The
# shared production verifier itself is extended to the full current route set.
ROUTES = V06_ROUTES
_v08._v06.ROUTES = V09_ROUTES


def verify_v08_subset_preserved() -> list[str]:
    failures: list[str] = []
    current_resources = set(RESOURCE_RECORD_MAP)
    current_questions = set(QUESTION_RECORD_MAP)
    missing_resources = sorted(V08_RESOURCE_IDS - current_resources)
    missing_questions = sorted(V08_QUESTION_IDS - current_questions)
    if missing_resources:
        failures.append(f"v0.8 compatibility: missing accepted Resources {missing_resources}")
    if missing_questions:
        failures.append(f"v0.8 compatibility: missing accepted Questions {missing_questions}")
    if not failures:
        print("PASS v0.8 accepted object-set compatibility (25 Resources, 14 Questions)")
    return failures


def verify_v09_concept_contract(origin: str, *, fetcher=fetch_url) -> list[str]:
    failures: list[str] = []
    understand = fetcher(expected_url(origin, "/understand/"))
    if f"There are {len(CONCEPT_RECORDS)} reviewed topic pages" not in understand.body:
        failures.append("/understand/: current Concept count is missing")
    for concept in CONCEPT_RECORDS:
        path = f"/understand/{concept['id']}/"
        if f'href="{path}"' not in understand.body:
            failures.append(f"/understand/: missing Concept route {path}")
        response = fetcher(expected_url(origin, path))
        first_read = html.escape(_builder.reader_intro(concept), quote=True)
        precise = html.escape(concept["summary"], quote=True)
        for marker in (
            first_read,
            precise,
            'class="review-meta">Last reviewed:',
            '<details class="technical-summary"><summary>More precise description</summary>',
            '<h2 id="next-routes-heading">Useful next routes</h2>',
            'href="/how-it-works/#confidence"',
        ):
            if marker not in response.body:
                failures.append(f"{path}: v0.9 Concept marker missing: {marker!r}")
    if not failures:
        print(f"PASS v0.9 Concept reading/navigation contract ({len(CONCEPT_RECORDS)} Concepts)")
    return failures


def verify_v09_question_contract(origin: str, *, fetcher=fetch_url) -> list[str]:
    failures: list[str] = []
    index = fetcher(expected_url(origin, "/questions/"))
    required_index = (
        "Relevant to inspect, not recommended.",
        f"{len(QUESTION_RECORDS)} governed practical questions",
        'href="/needs/"',
        'href="/a-z/"',
    )
    for marker in required_index:
        if marker not in index.body:
            failures.append(f"/questions/: v0.9 marker missing: {marker!r}")
    for group, _ids in _builder.QUESTION_GROUPS:
        escaped = html.escape(group, quote=True)
        if escaped not in index.body:
            failures.append(f"/questions/: missing need group {group!r}")

    for path, question in QUESTION_MARKERS_V09.items():
        escaped_question = html.escape(question, quote=True)
        if escaped_question not in index.body or f'href="{path}"' not in index.body:
            failures.append(f"/questions/: missing governed route {path}")
        response = fetcher(expected_url(origin, path))
        for marker in (
            "Relevant to inspect, not recommended.",
            '<h2 id="current-understanding-heading">Current understanding</h2>',
            '<h2 id="related-things-heading">Related things to inspect</h2>',
            '<h2 id="related-questions-heading">Related questions</h2>',
            '<h2 id="evidence-needed-heading">What evidence is still needed</h2>',
            '<h2 id="dissent-heading">Where people may disagree</h2>',
            '<h2 id="reopen-heading">When this answer should be revisited</h2>',
            "<summary>Question provenance and review state</summary>",
        ):
            if marker not in response.body:
                failures.append(f"{path}: v0.9 question marker missing: {marker!r}")
    if not failures:
        print(f"PASS v0.9 question contract ({len(QUESTION_RECORDS)} questions)")
    return failures


def verify_v09_resource_contract(origin: str, *, fetcher=fetch_url) -> list[str]:
    failures: list[str] = []
    for path, (name, official_url) in RESOURCE_MARKERS_V09.items():
        response = fetcher(expected_url(origin, path))
        for marker in (
            "Listed, not endorsed",
            "Last reviewed:",
            '<h2 id="use-heading">What it is for</h2>',
            '<h2 id="access-heading">Access</h2>',
            '<h2 id="related-heading">Related topics</h2>',
            '<h2 id="resource-question-heading">Questions that lead here</h2>',
            '<h2 id="scope-heading">Scope for navigation</h2>',
            '<h2 id="limits-heading">Limitations and possible poor fit</h2>',
            '<h2 id="cost-heading">Cost and access notes</h2>',
            '<h2 id="conflict-heading">Ownership and conflicts</h2>',
            '<h2 id="evidence-status-heading">Evidence status</h2>',
            'href="/places/"',
            'href="/types/"',
            f'href="{html.escape(official_url, quote=True)}"',
        ):
            if marker not in response.body:
                failures.append(f"{path}: v0.9 resource marker missing for {name}: {marker!r}")
    resources_index = fetcher(expected_url(origin, "/resources/"))
    for marker in ('href="/types/"', 'href="/places/"', 'href="/a-z/"'):
        if marker not in resources_index.body:
            failures.append(f"/resources/: missing catalogue navigation {marker!r}")
    if not failures:
        print(f"PASS v0.9 resource contract ({len(RESOURCE_RECORDS)} resources)")
    return failures


def verify_v09_navigation_contract(origin: str, *, fetcher=fetch_url) -> list[str]:
    failures: list[str] = []
    homepage = fetcher(expected_url(origin, "/"))
    for marker in ('href="/needs/"', 'href="/types/"', 'href="/places/"', 'href="/a-z/"'):
        if marker not in homepage.body:
            failures.append(f"/: missing v0.9 browse route {marker!r}")

    needs = fetcher(expected_url(origin, "/needs/"))
    for question in QUESTION_RECORDS:
        route = f'/questions/{question["id"]}/'
        if f'href="{route}"' not in needs.body:
            failures.append(f"/needs/: missing Question {question['id']}")

    for path, marker in NAVIGATION_MARKERS[1:9]:
        response = fetcher(expected_url(origin, path))
        if marker not in response.body:
            failures.append(f"{path}: hub heading missing")
        if "Relevant to inspect, not recommended." not in response.body:
            failures.append(f"{path}: hub safety boundary missing")

    types = fetcher(expected_url(origin, "/types/"))
    for marker in ("<h2>Questions</h2>", "<h2>Topics</h2>"):
        if marker not in types.body:
            failures.append(f"/types/: missing {marker!r}")
    for resource in RESOURCE_RECORDS:
        route = f'/resources/{resource["id"]}/'
        if f'href="{route}"' not in types.body:
            failures.append(f"/types/: missing Resource {resource['id']}")

    places = fetcher(expected_url(origin, "/places/"))
    if "Navigation scope, not eligibility." not in places.body:
        failures.append("/places/: jurisdiction boundary missing")
    for resource in RESOURCE_RECORDS:
        route = f'/resources/{resource["id"]}/'
        if f'href="{route}"' not in places.body:
            failures.append(f"/places/: missing Resource {resource['id']}")

    az = fetcher(expected_url(origin, "/a-z/"))
    for concept in CONCEPT_RECORDS:
        if f'href="/understand/{concept["id"]}/"' not in az.body:
            failures.append(f"/a-z/: missing Concept {concept['id']}")
    for resource in RESOURCE_RECORDS:
        if f'href="/resources/{resource["id"]}/"' not in az.body:
            failures.append(f"/a-z/: missing Resource {resource['id']}")
    for question in QUESTION_RECORDS:
        if f'href="/questions/{question["id"]}/"' not in az.body:
            failures.append(f"/a-z/: missing Question {question['id']}")

    if not failures:
        print("PASS v0.9 need/type/place/A–Z navigation contract")
    return failures


def verify_production(origin: str, *, fetcher=fetch_url) -> list[str]:
    failures = verify_v08_subset_preserved()
    failures.extend(_v08._v06.verify_production(origin, fetcher=fetcher))
    failures.extend(_v08.verify_v07_question_contract(origin, fetcher=fetcher))
    failures.extend(verify_v09_concept_contract(origin, fetcher=fetcher))
    failures.extend(verify_v09_question_contract(origin, fetcher=fetcher))
    failures.extend(verify_v09_resource_contract(origin, fetcher=fetcher))
    failures.extend(verify_v09_navigation_contract(origin, fetcher=fetcher))
    return failures


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Verify ND Oracle production HTTP plus v0.9 100-object content and 125-route navigation contracts over HTTPS."
    )
    parser.add_argument("--origin", default=DEFAULT_ORIGIN)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    origin = args.origin.rstrip("/")
    if not origin.startswith("https://"):
        print("Refusing non-HTTPS production origin.", file=sys.stderr)
        return 2
    try:
        failures = verify_production(origin)
    except (OSError, urllib.error.URLError) as exc:
        print(f"LIVE VERIFICATION ERROR: {exc}", file=sys.stderr)
        return 1
    if failures:
        print("LIVE VERIFICATION FAIL", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1
    print(
        f"Verified {len(V09_ROUTES)} canonical routes plus inherited reading and v0.9 content/navigation contracts at {origin}."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
