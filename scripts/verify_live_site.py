from __future__ import annotations

import argparse
import sys
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from html.parser import HTMLParser
from urllib.parse import urljoin, urlsplit

DEFAULT_ORIGIN = "https://ndoracle.org"
USER_AGENT = "nd-oracle-live-verifier/0.4"

ROUTES = (
    ("/", "Understand neurodivergence without doing all the digging yourself"),
    ("/understand/", "<h1>Understand</h1>"),
    ("/understand/neurodiversity/", "<h1>Neurodiversity</h1>"),
    ("/understand/autism/", "<h1>Autism</h1>"),
    ("/understand/adhd/", "<h1>ADHD</h1>"),
    ("/understand/executive-function/", "<h1>Executive function</h1>"),
    ("/understand/sensory-processing/", "<h1>Sensory processing</h1>"),
    ("/understand/dyslexia/", "<h1>Dyslexia</h1>"),
    ("/understand/developmental-coordination-disorder/", "<h1>Developmental co-ordination disorder</h1>"),
    ("/understand/tourette-syndrome/", "<h1>Tourette syndrome</h1>"),
    ("/understand/learning-disability/", "<h1>Learning disability</h1>"),
    ("/understand/developmental-language-disorder/", "<h1>Developmental language disorder</h1>"),
    ("/how-it-works/", "<h1>How this site works</h1>"),
    ("/about/", "<h1>About</h1>"),
    ("/accessibility/", "<h1>Accessibility</h1>"),
    ("/privacy/", "<h1>Privacy</h1>"),
)

LEGACY_ROUTES = ("/tools/", "/games/", "/resources/", "/community/", "/oracle/")
NOINDEX_MARKER = '<meta name="robots" content="noindex, follow">'
NOT_FOUND_PATH = "/__nd_oracle_live_verifier_missing_page__/"
NOT_FOUND_MARKER = "<h1>Page not found</h1>"
CLOUDFLARE_MANAGED_BEGIN = "# BEGIN Cloudflare Managed content"
CLOUDFLARE_MANAGED_END = "# END Cloudflare Managed Content"
CLOUDFLARE_CONTENT_SIGNAL = "Content-Signal: search=yes,ai-train=no,use=reference"

SECURITY_HEADERS = {
    "content-security-policy": "default-src 'none'; style-src 'self'; img-src 'self' data:; font-src 'self'; script-src 'none'; connect-src 'none'; media-src 'self'; manifest-src 'self'; object-src 'none'; base-uri 'none'; form-action 'none'; frame-ancestors 'none'; upgrade-insecure-requests",
    "strict-transport-security": "max-age=31536000",
    "cross-origin-opener-policy": "same-origin",
    "cross-origin-resource-policy": "same-origin",
    "x-frame-options": "DENY",
    "x-content-type-options": "nosniff",
    "x-permitted-cross-domain-policies": "none",
    "referrer-policy": "no-referrer",
    "permissions-policy": "accelerometer=(), camera=(), geolocation=(), gyroscope=(), magnetometer=(), microphone=(), payment=(), usb=()",
}


@dataclass(frozen=True)
class Response:
    status: int
    final_url: str
    content_type: str
    body: str
    headers: dict[str, str] = field(default_factory=dict)


class SurfaceParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.forms = 0
        self.scripts = 0
        self.iframes = 0
        self.loaded_resources: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {name.lower(): value or "" for name, value in attrs}
        lowered = tag.lower()
        if lowered == "form":
            self.forms += 1
        if lowered == "script":
            self.scripts += 1
        if lowered == "iframe":
            self.iframes += 1
        if lowered in {"img", "script", "iframe", "audio", "video", "source"}:
            source = values.get("src", "").strip()
            if source:
                self.loaded_resources.append(source)
        elif lowered == "link":
            rel = {item.lower() for item in values.get("rel", "").split()}
            if rel.intersection({"stylesheet", "preload", "modulepreload", "icon", "manifest"}):
                href = values.get("href", "").strip()
                if href:
                    self.loaded_resources.append(href)

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)


def normalize_header_value(value: str) -> str:
    return " ".join(value.split())


def fetch_url(url: str, timeout: float = 20.0) -> Response:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "*/*"})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            payload = response.read().decode("utf-8", errors="replace")
            return Response(
                status=response.status,
                final_url=response.geturl(),
                content_type=response.headers.get("Content-Type", ""),
                body=payload,
                headers={key.lower(): value for key, value in response.headers.items()},
            )
    except urllib.error.HTTPError as exc:
        payload = exc.read().decode("utf-8", errors="replace")
        return Response(
            status=exc.code,
            final_url=exc.geturl(),
            content_type=exc.headers.get("Content-Type", ""),
            body=payload,
            headers={key.lower(): value for key, value in exc.headers.items()},
        )


fetch_html = fetch_url


def expected_url(origin: str, path: str) -> str:
    return origin.rstrip("/") + path


def canonical_marker(url: str) -> str:
    return f'<link rel="canonical" href="{url}">'


def verify_security_headers(path: str, response: Response) -> list[str]:
    failures: list[str] = []
    for name, expected in SECURITY_HEADERS.items():
        actual = response.headers.get(name)
        if actual is None:
            failures.append(f"{path}: missing security header {name}")
        elif normalize_header_value(actual) != normalize_header_value(expected):
            failures.append(
                f"{path}: security header {name} mismatch: got {actual!r}; expected {expected!r}"
            )
    return failures


def verify_passive_surface(origin: str, path: str, response: Response) -> list[str]:
    parser = SurfaceParser()
    parser.feed(response.body)
    failures: list[str] = []
    if parser.forms:
        failures.append(f"{path}: unexpected form element present")
    if parser.scripts:
        failures.append(f"{path}: unexpected script element present")
    if parser.iframes:
        failures.append(f"{path}: unexpected iframe element present")

    origin_host = urlsplit(origin).netloc.lower()
    for resource in parser.loaded_resources:
        if resource.startswith("data:"):
            continue
        parsed = urlsplit(urljoin(origin + "/", resource))
        if parsed.scheme not in {"http", "https"} or parsed.netloc.lower() != origin_host:
            failures.append(f"{path}: unexpected externally loaded resource {resource!r}")
    return failures


def verify_route(origin: str, path: str, marker: str, *, fetcher=fetch_url) -> list[str]:
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
    failures.extend(verify_security_headers(path, response))
    failures.extend(verify_passive_surface(origin, path, response))
    return failures


def verify_routes(origin: str, *, fetcher=fetch_url) -> list[str]:
    failures: list[str] = []
    for path, marker in ROUTES:
        route_failures = verify_route(origin, path, marker, fetcher=fetcher)
        if route_failures:
            failures.extend(route_failures)
        else:
            print(f"PASS canonical {path}")
    return failures


def verify_not_found(origin: str, *, fetcher=fetch_url) -> list[str]:
    url = expected_url(origin, NOT_FOUND_PATH)
    response = fetcher(url)
    failures: list[str] = []
    if response.status != 404:
        failures.append(f"404: expected HTTP 404, got {response.status}")
    if response.final_url != url:
        failures.append(f"404: unexpected final URL {response.final_url!r}; expected {url!r}")
    if "text/html" not in response.content_type.lower():
        failures.append(f"404: expected text/html, got {response.content_type!r}")
    if NOT_FOUND_MARKER not in response.body:
        failures.append("404: expected not-found page marker is missing")
    if NOINDEX_MARKER not in response.body:
        failures.append("404: expected noindex marker is missing")
    failures.extend(verify_security_headers("404", response))
    failures.extend(verify_passive_surface(origin, "404", response))
    if not failures:
        print("PASS 404")
    return failures


def verify_legacy_routes(origin: str, *, fetcher=fetch_url) -> list[str]:
    failures: list[str] = []
    for path in LEGACY_ROUTES:
        url = expected_url(origin, path)
        response = fetcher(url)
        route_failures: list[str] = []
        if response.status != 200:
            route_failures.append(f"{path}: expected compatibility HTTP 200, got {response.status}")
        if response.final_url != url:
            route_failures.append(f"{path}: unexpected final URL {response.final_url!r}; expected {url!r}")
        if "text/html" not in response.content_type.lower():
            route_failures.append(f"{path}: expected text/html, got {response.content_type!r}")
        if NOINDEX_MARKER not in response.body:
            route_failures.append(f"{path}: expected noindex marker is missing")
        route_failures.extend(verify_security_headers(path, response))
        route_failures.extend(verify_passive_surface(origin, path, response))
        if route_failures:
            failures.extend(route_failures)
        else:
            print(f"PASS legacy-noindex {path}")
    return failures


def expected_sitemap_urls(origin: str) -> set[str]:
    return {expected_url(origin, path) for path, _ in ROUTES}


def expected_origin_robots(origin: str) -> str:
    return "User-agent: *\nAllow: /\n" f"Sitemap: {origin}/sitemap.xml\n"


def verify_robots_content(origin: str, body: str) -> list[str]:
    actual = body.replace("\r\n", "\n")
    expected_tail = expected_origin_robots(origin)
    failures: list[str] = []
    if not actual.endswith(expected_tail):
        failures.append(
            "robots.txt: origin indexing/sitemap block is missing or changed: "
            f"expected trailing block={expected_tail!r}"
        )

    managed_present = CLOUDFLARE_MANAGED_BEGIN in actual or CLOUDFLARE_MANAGED_END in actual
    if managed_present:
        if CLOUDFLARE_MANAGED_BEGIN not in actual or CLOUDFLARE_MANAGED_END not in actual:
            failures.append("robots.txt: incomplete Cloudflare managed-content block")
        compact = "".join(actual.lower().split())
        expected_signal = "".join(CLOUDFLARE_CONTENT_SIGNAL.lower().split())
        if expected_signal not in compact:
            failures.append(
                "robots.txt: Cloudflare managed content signal changed; expected search=yes, ai-train=no, use=reference"
            )
    return failures


def verify_metadata_files(origin: str, *, fetcher=fetch_url) -> list[str]:
    failures: list[str] = []
    robots_url = expected_url(origin, "/robots.txt")
    robots = fetcher(robots_url)
    robots_failures: list[str] = []
    if robots.status != 200:
        robots_failures.append(f"robots.txt: expected HTTP 200, got {robots.status}")
    if robots.final_url != robots_url:
        robots_failures.append(f"robots.txt: unexpected final URL {robots.final_url!r}")
    robots_failures.extend(verify_robots_content(origin, robots.body))
    if robots_failures:
        failures.extend(robots_failures)
    else:
        print("PASS robots.txt")

    sitemap_url = expected_url(origin, "/sitemap.xml")
    sitemap = fetcher(sitemap_url)
    sitemap_failures: list[str] = []
    if sitemap.status != 200:
        sitemap_failures.append(f"sitemap.xml: expected HTTP 200, got {sitemap.status}")
    if sitemap.final_url != sitemap_url:
        sitemap_failures.append(f"sitemap.xml: unexpected final URL {sitemap.final_url!r}")
    try:
        root = ET.fromstring(sitemap.body)
        actual_urls = {
            (element.text or "").strip()
            for element in root.findall(
                "{http://www.sitemaps.org/schemas/sitemap/0.9}url/{http://www.sitemaps.org/schemas/sitemap/0.9}loc"
            )
        }
    except ET.ParseError as exc:
        sitemap_failures.append(f"sitemap.xml: invalid XML: {exc}")
        actual_urls = set()
    expected_urls = expected_sitemap_urls(origin)
    if actual_urls != expected_urls:
        sitemap_failures.append(
            "sitemap.xml: URL set mismatch: "
            f"missing={sorted(expected_urls - actual_urls)}; unexpected={sorted(actual_urls - expected_urls)}"
        )
    if sitemap_failures:
        failures.extend(sitemap_failures)
    else:
        print("PASS sitemap.xml")
    return failures


def verify_www_redirect(origin: str, *, fetcher=fetch_url) -> list[str]:
    failures: list[str] = []
    target = f"{origin}/understand/?q=nd-oracle-live-verify"
    for scheme in ("http", "https"):
        source = f"{scheme}://www.ndoracle.org/understand/?q=nd-oracle-live-verify"
        response = fetcher(source)
        if response.status != 200:
            failures.append(f"www redirect from {scheme}: final response expected HTTP 200, got {response.status}")
        if response.final_url != target:
            failures.append(
                f"www redirect from {scheme}: expected final URL {target!r}, got {response.final_url!r}"
            )
        if "<h1>Understand</h1>" not in response.body:
            failures.append(f"www redirect from {scheme}: target page marker is missing")
        failures.extend(verify_security_headers(f"www-{scheme}", response))
    if not failures:
        print("PASS www redirect with path/query preservation")
    return failures


def verify_production(origin: str, *, fetcher=fetch_url) -> list[str]:
    failures: list[str] = []
    failures.extend(verify_routes(origin, fetcher=fetcher))
    failures.extend(verify_not_found(origin, fetcher=fetcher))
    failures.extend(verify_metadata_files(origin, fetcher=fetcher))
    failures.extend(verify_legacy_routes(origin, fetcher=fetcher))
    failures.extend(verify_www_redirect(origin, fetcher=fetcher))
    return failures


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Verify the ND Oracle production HTTP and public-surface contract over HTTPS."
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
        f"Verified {len(ROUTES)} canonical routes plus production HTTP/public-surface contract at {origin}."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
