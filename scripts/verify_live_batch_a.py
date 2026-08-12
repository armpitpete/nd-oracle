from __future__ import annotations

import argparse
import sys
import xml.etree.ElementTree as ET

from scripts import verify_live_site


BATCH_A_ROUTES = (
    ("/understand/dyslexia/", "<h1>Dyslexia</h1>"),
    ("/understand/developmental-coordination-disorder/", "<h1>Developmental co-ordination disorder</h1>"),
    ("/understand/tourette-syndrome/", "<h1>Tourette syndrome</h1>"),
    ("/understand/learning-disability/", "<h1>Learning disability</h1>"),
    ("/understand/developmental-language-disorder/", "<h1>Developmental language disorder</h1>"),
)


def verify_batch_a(origin: str) -> list[str]:
    failures: list[str] = []
    for path, marker in BATCH_A_ROUTES:
        route_failures = verify_live_site.verify_route(origin, path, marker)
        if route_failures:
            failures.extend(route_failures)
        else:
            print(f"PASS Batch A canonical {path}")

    sitemap_url = verify_live_site.expected_url(origin, "/sitemap.xml")
    sitemap = verify_live_site.fetch_url(sitemap_url)
    if sitemap.status != 200:
        failures.append(f"sitemap.xml: expected HTTP 200, got {sitemap.status}")
        return failures
    try:
        root = ET.fromstring(sitemap.body)
        actual_urls = {
            (element.text or "").strip()
            for element in root.findall(
                "{http://www.sitemaps.org/schemas/sitemap/0.9}url/{http://www.sitemaps.org/schemas/sitemap/0.9}loc"
            )
        }
    except ET.ParseError as exc:
        failures.append(f"sitemap.xml: invalid XML: {exc}")
        return failures

    for path, _ in BATCH_A_ROUTES:
        expected = verify_live_site.expected_url(origin, path)
        if expected not in actual_urls:
            failures.append(f"sitemap.xml: missing Batch A route {expected}")
    if not failures:
        print("PASS Batch A routes present in sitemap.xml")
    return failures


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Verify the five Batch A topic routes on live ND Oracle production.")
    parser.add_argument("--origin", default=verify_live_site.DEFAULT_ORIGIN)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    origin = args.origin.rstrip("/")
    if not origin.startswith("https://"):
        print("Refusing non-HTTPS production origin.", file=sys.stderr)
        return 2
    failures = verify_batch_a(origin)
    for failure in failures:
        print(f"FAIL {failure}", file=sys.stderr)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
