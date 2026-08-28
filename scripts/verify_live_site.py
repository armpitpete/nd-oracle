from __future__ import annotations

import argparse
import html
import sys
import urllib.error

from scripts import verify_live_site_v06 as _v06
from scripts.verify_live_site_v06 import *

USER_AGENT = "nd-oracle-live-verifier/0.7"
_v06.USER_AGENT = USER_AGENT

QUESTION_MARKERS = {
    "/questions/task-starting-and-organisation/": "I keep losing track of tasks or struggle to get started. What might help me organise the next step?",
    "/questions/low-time-pressure-games/": "Which current games might suit me if I want little or no time pressure?",
    "/questions/workplace-support-great-britain/": "Where can I look for workplace support in Great Britain if disability or a health condition affects my work?",
    "/questions/autism-information-and-support/": "I want autism information or support. Which kind of organisation am I actually looking for?",
    "/questions/autism-anxiety-tools/": "Are there practical anxiety or self-management tools in the current catalogue that were made with autistic people in mind?",
}

V07_ROUTES = ROUTES + (
    ("/questions/", "<h1>Questions</h1>"),
    *((path, f"<h1>{html.escape(question, quote=True)}</h1>") for path, question in QUESTION_MARKERS.items()),
)
_v06.ROUTES = V07_ROUTES


def verify_v07_question_contract(origin: str, *, fetcher=fetch_url) -> list[str]:
    failures: list[str] = []

    homepage = fetcher(expected_url(origin, "/"))
    question_index = fetcher(expected_url(origin, "/questions/"))
    for path, question in QUESTION_MARKERS.items():
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
        print(f"PASS v0.7 question-led discovery contract ({len(QUESTION_MARKERS)} questions)")
    return failures


def verify_production(origin: str, *, fetcher=fetch_url) -> list[str]:
    failures = _v06.verify_production(origin, fetcher=fetcher)
    failures.extend(verify_v07_question_contract(origin, fetcher=fetcher))
    return failures


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Verify the ND Oracle production HTTP, v0.6 ecosystem and v0.7 question-led discovery contracts over HTTPS."
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
        f"Verified {len(V07_ROUTES)} canonical routes plus v0.6 reading/resource and v0.7 question-led discovery production contracts at {origin}."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
