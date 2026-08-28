from __future__ import annotations

import argparse
import html
import json
import sys
import urllib.error
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts import verify_live_site_v06 as _v06
from scripts.verify_live_site_v06 import *

ROOT = Path(__file__).resolve().parents[1]
RESOURCE_DIR = ROOT / "objects" / "resources"
QUESTION_DIR = ROOT / "objects" / "questions"
USER_AGENT = "nd-oracle-live-verifier/0.8"
_v06.USER_AGENT = USER_AGENT

# Preserve the immutable v0.6 route contract even when this module is loaded or
# reloaded more than once in one interpreter. The live v0.8 verifier extends
# the shared compatibility module, but legacy contract tests still need the
# exact original 36-route baseline.
if not hasattr(_v06, "_V08_ORIGINAL_ROUTES"):
    _v06._V08_ORIGINAL_ROUTES = tuple(_v06.ROUTES)
V06_ROUTES = tuple(_v06._V08_ORIGINAL_ROUTES)
ROUTES = V06_ROUTES


def _load_records(directory: Path) -> list[dict]:
    records = []
    for path in sorted(directory.glob("*.json")):
        with path.open("r", encoding="utf-8") as handle:
            records.append(json.load(handle))
    return records


RESOURCE_RECORDS = _load_records(RESOURCE_DIR)
QUESTION_RECORDS = _load_records(QUESTION_DIR)
QUESTION_RECORD_MAP = {question["id"]: question for question in QUESTION_RECORDS}

V07_QUESTION_IDS = (
    "task-starting-and-organisation",
    "low-time-pressure-games",
    "workplace-support-great-britain",
    "autism-information-and-support",
    "autism-anxiety-tools",
)
V07_QUESTION_MARKERS = {
    f"/questions/{question_id}/": QUESTION_RECORD_MAP[question_id]["question"]
    for question_id in V07_QUESTION_IDS
}
V07_ROUTES = V06_ROUTES + (
    ("/questions/", "<h1>Questions</h1>"),
    *((path, f"<h1>{html.escape(question, quote=True)}</h1>") for path, question in V07_QUESTION_MARKERS.items()),
)

RESOURCE_MARKERS_V08 = {
    f"/resources/{resource['id']}/": (
        resource["name"],
        next(
            locator["value"]
            for locator in resource.get("locators", [])
            if locator.get("type") == "url"
        ),
    )
    for resource in RESOURCE_RECORDS
}
QUESTION_MARKERS = {
    f"/questions/{question['id']}/": question["question"]
    for question in QUESTION_RECORDS
}

# Start from the proven v0.6 route set, but replace its fixed resource-detail
# routes with the complete current Resource corpus. Collection route labels can
# evolve while their canonical paths remain stable.
BASE_ROUTES = tuple(
    (
        path,
        "<h1>Resources</h1>"
        if path == "/resources/"
        else "<h1>Tools &amp; practical help</h1>"
        if path == "/tools/"
        else marker,
    )
    for path, marker in V06_ROUTES
    if not (path.startswith("/resources/") and path != "/resources/")
)

V08_ROUTES = BASE_ROUTES + (
    *((path, f"<h1>{html.escape(name, quote=True)}</h1>") for path, (name, _url) in RESOURCE_MARKERS_V08.items()),
    ("/books-media/", "<h1>Books &amp; media</h1>"),
    ("/questions/", "<h1>Questions</h1>"),
    *((path, f"<h1>{html.escape(question, quote=True)}</h1>") for path, question in QUESTION_MARKERS.items()),
)
_v06.ROUTES = V08_ROUTES


def verify_v07_question_contract(origin: str, *, fetcher=fetch_url) -> list[str]:
    """Retain the accepted v0.7 five-question contract as a compatibility layer."""
    failures: list[str] = []

    homepage = fetcher(expected_url(origin, "/"))
    question_index = fetcher(expected_url(origin, "/questions/"))
    for path, question in V07_QUESTION_MARKERS.items():
        escaped_question = html.escape(question, quote=True)
        if escaped_question not in homepage.body:
            failures.append(f"/: missing v0.7 practical question {question!r}")
        if f'href="{path}"' not in homepage.body:
            failures.append(f"/: missing v0.7 practical question route {path}")
        if escaped_question not in question_index.body:
            failures.append(f"/questions/: missing governed question {question!r}")
        if f'href="{path}"' not in question_index.body:
            failures.append(f"/questions/: missing route to governed question {path}")

        response = fetcher(expected_url(origin, path))
        for marker in (
            "Relevant to inspect, not recommended.",
            '<h2 id="current-understanding-heading">Current understanding</h2>',
            '<h2 id="related-things-heading">Related things to inspect</h2>',
            '<h2 id="evidence-needed-heading">What evidence is still needed</h2>',
            '<h2 id="dissent-heading">Where people may disagree</h2>',
            '<h2 id="reopen-heading">When this answer should be revisited</h2>',
            'class="review-meta">Last reviewed:',
            "<summary>Question provenance and review state</summary>",
        ):
            if marker not in response.body:
                failures.append(f"{path}: v0.7 question contract marker missing: {marker!r}")

    for marker in (
        "Relevant to inspect, not recommended.",
        "governed practical questions",
    ):
        if marker not in question_index.body:
            failures.append(f"/questions/: question-index boundary marker missing: {marker!r}")

    how = fetcher(expected_url(origin, "/how-it-works/"))
    if "<h2>Question-led discovery</h2>" not in how.body:
        failures.append("/how-it-works/: question-led discovery explanation is missing")

    if not failures:
        print(f"PASS v0.7 question-led discovery contract ({len(V07_QUESTION_MARKERS)} questions)")
    return failures


def verify_v08_question_contract(origin: str, *, fetcher=fetch_url) -> list[str]:
    failures: list[str] = []
    question_index = fetcher(expected_url(origin, "/questions/"))

    for marker in (
        "Relevant to inspect, not recommended.",
        "governed practical questions",
        "Everyday life &amp; technology",
        "Work &amp; study",
        "Finding information &amp; support",
        "Games &amp; downtime",
        "Anxiety &amp; self-management",
    ):
        if marker not in question_index.body:
            failures.append(f"/questions/: v0.8 navigation marker missing: {marker!r}")

    for path, question in QUESTION_MARKERS.items():
        escaped_question = html.escape(question, quote=True)
        if escaped_question not in question_index.body:
            failures.append(f"/questions/: missing governed question {question!r}")
        if f'href="{path}"' not in question_index.body:
            failures.append(f"/questions/: missing route to governed question {path}")

        response = fetcher(expected_url(origin, path))
        for marker in (
            "Relevant to inspect, not recommended.",
            '<h2 id="current-understanding-heading">Current understanding</h2>',
            '<h2 id="related-things-heading">Related things to inspect</h2>',
            '<h2 id="evidence-needed-heading">What evidence is still needed</h2>',
            '<h2 id="dissent-heading">Where people may disagree</h2>',
            '<h2 id="reopen-heading">When this answer should be revisited</h2>',
            'class="review-meta">Last reviewed:',
            "<summary>Question provenance and review state</summary>",
        ):
            if marker not in response.body:
                failures.append(f"{path}: v0.8 question contract marker missing: {marker!r}")

    if not failures:
        print(f"PASS v0.8 question contract ({len(QUESTION_MARKERS)} questions)")
    return failures


def verify_v08_resource_contract(origin: str, *, fetcher=fetch_url) -> list[str]:
    failures: list[str] = []
    for path, (name, official_url) in RESOURCE_MARKERS_V08.items():
        response = fetcher(expected_url(origin, path))
        required = (
            "Listed, not endorsed",
            "Last reviewed:",
            '<h2 id="use-heading">What it is for</h2>',
            '<h2 id="access-heading">Access</h2>',
            '<h2 id="related-heading">Related topics</h2>',
            '<h2 id="resource-question-heading">Questions that lead here</h2>',
            '<h2 id="limits-heading">Limitations and possible poor fit</h2>',
            '<h2 id="cost-heading">Cost and access notes</h2>',
            '<h2 id="conflict-heading">Ownership and conflicts</h2>',
            '<h2 id="evidence-status-heading">Evidence status</h2>',
            "This listing makes no efficacy or safety claim",
            f'href="{html.escape(official_url, quote=True)}"',
        )
        for marker in required:
            if marker not in response.body:
                failures.append(f"{path}: v0.8 resource marker missing for {name}: {marker!r}")

    resources_index = fetcher(expected_url(origin, "/resources/"))
    for marker in (
        "<h1>Resources</h1>",
        "All resources",
        "Tools &amp; practical help",
        'href="/tools/"',
        'href="/games/"',
        'href="/books-media/"',
        'href="/community/"',
    ):
        if marker not in resources_index.body:
            failures.append(f"/resources/: v0.8 resource navigation marker missing: {marker!r}")

    books = fetcher(expected_url(origin, "/books-media/"))
    if "Listed, not endorsed" not in books.body:
        failures.append("/books-media/: listing boundary marker missing")

    if not failures:
        print(f"PASS v0.8 resource contract ({len(RESOURCE_MARKERS_V08)} resources)")
    return failures


def verify_v08_navigation_contract(origin: str, *, fetcher=fetch_url) -> list[str]:
    failures: list[str] = []
    homepage = fetcher(expected_url(origin, "/"))
    for marker in (
        ">Questions</a>",
        ">Topics</a>",
        ">Resources</a>",
        "Tools &amp; practical help",
        "Browse all",
        'href="/books-media/"',
    ):
        if marker not in homepage.body:
            failures.append(f"/: v0.8 navigation marker missing: {marker!r}")

    for path in TOPIC_FIRST_READ_MARKERS:
        response = fetcher(expected_url(origin, path))
        if '<h2 id="next-routes-heading">Useful next routes</h2>' not in response.body:
            failures.append(f"{path}: useful-next-routes navigation is missing")

    if not failures:
        print("PASS v0.8 cross-content navigation contract")
    return failures


def verify_production(origin: str, *, fetcher=fetch_url) -> list[str]:
    failures = _v06.verify_production(origin, fetcher=fetcher)
    failures.extend(verify_v08_question_contract(origin, fetcher=fetcher))
    failures.extend(verify_v08_resource_contract(origin, fetcher=fetcher))
    failures.extend(verify_v08_navigation_contract(origin, fetcher=fetcher))
    return failures


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Verify the ND Oracle production HTTP, inherited v0.6 contracts and v0.8 content/navigation contract over HTTPS."
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
        f"Verified {len(V08_ROUTES)} canonical routes plus inherited v0.6 and v0.8 content/navigation production contracts at {origin}."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
