from __future__ import annotations

import argparse
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass

DEFAULT_ORIGIN = "https://ndoracle.org"
USER_AGENT = "nd-oracle-live-verifier/0.1"

ROUTES = (
    ("/", "Understand neurodivergence without doing all the digging yourself"),
    ("/understand/", "<h1>Understand</h1>"),
    ("/understand/neurodiversity/", "<h1>Neurodiversity</h1>"),
    ("/understand/autism/", "<h1>Autism</h1>"),
    ("/understand/adhd/", "<h1>ADHD</h1>"),
    ("/understand/executive-function/", "<h1>Executive function</h1>"),
    ("/understand/sensory-processing/", "<h1>Sensory processing</h1>"),
    ("/how-it-works/", "<h1>How this site works</h1>"),
    ("/about/", "<h1>About</h1>"),
    ("/accessibility/", "<h1>Accessibility</h1>"),
    ("/privacy/", "<h1>Privacy</h1>"),
)


@dataclass(frozen=True)
class Response:
    status: int
    final_url: str
    content_type: str
    body: str


def fetch_html(url: str, timeout: float = 20.0) -> Response:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            payload = response.read().decode("utf-8", errors="replace")
            return Response(
                status=response.status,
                final_url=response.geturl(),
                content_type=response.headers.get("Content-Type", ""),
                body=payload,
            )
    except urllib.error.HTTPError as exc:
        payload = exc.read().decode("utf-8", errors="replace")
        return Response(
            status=exc.code,
            final_url=exc.geturl(),
            content_type=exc.headers.get("Content-Type", ""),
            body=payload,
        )


def expected_url(origin: str, path: str) -> str:
    return origin.rstrip("/") + path


def canonical_marker(url: str) -> str:
    return f'<link rel="canonical" href="{url}">'


def verify_route(
    origin: str,
    path: str,
    marker: str,
    *,
    fetcher=fetch_html,
) -> list[str]:
    url = expected_url(origin, path)
    response = fetcher(url)
    failures: list[str] = []

    if response.status != 200:
        failures.append(f"{path}: expected HTTP 200, got {response.status}")
    if response.final_url != url:
        failures.append(f"{path}: unexpected final URL {response.final_url!r}; expected {url!r}")
    if "text/html" not in response.content_type.lower():
        failures.append(f"{path}: expected text/html, got {response.content_type!r}")
    if marker not in response.body:
        failures.append(f"{path}: expected page marker not found: {marker!r}")
    canonical = canonical_marker(url)
    if canonical not in response.body:
        failures.append(f"{path}: expected canonical link not found: {canonical!r}")

    return failures


def verify_routes(origin: str, *, fetcher=fetch_html) -> list[str]:
    failures: list[str] = []
    for path, marker in ROUTES:
        route_failures = verify_route(origin, path, marker, fetcher=fetcher)
        if route_failures:
            failures.extend(route_failures)
        else:
            print(f"PASS {path}")
    return failures


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Verify the canonical ND Oracle production reading routes over HTTPS."
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
        failures = verify_routes(origin)
    except (OSError, urllib.error.URLError) as exc:
        print(f"LIVE VERIFICATION ERROR: {exc}", file=sys.stderr)
        return 1

    if failures:
        print("LIVE VERIFICATION FAIL", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1

    print(f"Verified {len(ROUTES)} canonical production routes at {origin}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
