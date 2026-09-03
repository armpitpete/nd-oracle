from __future__ import annotations

import argparse
import html
import json
import sys
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlsplit

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts import build_site

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ORIGIN = "https://ndoracle.org"
USER_AGENT = "nd-oracle-live-verifier/1.0"
COMPATIBILITY_FIXTURE = ROOT / "contracts" / "public-compatibility-v1.json"

TOPIC_FIRST_READ_MARKERS = {
    "/understand/neurodiversity/": "People's brains and nervous systems vary.",
    "/understand/autism/": "Autistic people can experience communication, social situations, routines, interests and sensory input differently.",
    "/understand/adhd/": "ADHD can affect attention, activity, impulsivity and managing everyday tasks.",
    "/understand/executive-function/": "Executive functions help us hold things in mind, switch attention, pause responses and organise actions towards a goal.",
    "/understand/sensory-processing/": "People differ in how strongly they notice and respond to sound, light, touch, movement and other sensory input.",
    "/understand/dyslexia/": "Dyslexia mainly affects learning and using word reading and spelling.",
    "/understand/developmental-coordination-disorder/": "Developmental co-ordination disorder (DCD) affects how easily someone learns and carries out coordinated movements.",
    "/understand/tourette-syndrome/": "Tourette syndrome involves motor and vocal tics that change over time.",
    "/understand/learning-disability/": "In the UK, a learning disability means lifelong difficulty learning or understanding new information together with difficulty managing everyday life independently.",
    "/understand/developmental-language-disorder/": "Developmental language disorder (DLD) is a persistent difficulty understanding and/or using language that affects everyday life.",
}
HOMEPAGE_QUESTIONS = (
    ("What does neurodiversity mean?", "/understand/neurodiversity/"),
    ("What is autism?", "/understand/autism/"),
    ("What is ADHD?", "/understand/adhd/"),
    ("Why can starting or organising tasks feel hard?", "/understand/executive-function/"),
    ("Why can sound, light or touch feel intense?", "/understand/sensory-processing/"),
    ("Why can reading or spelling stay difficult?", "/understand/dyslexia/"),
    ("Why can coordination and everyday movement be hard?", "/understand/developmental-coordination-disorder/"),
    ("What are tics and Tourette syndrome?", "/understand/tourette-syndrome/"),
    ("What does learning disability mean in the UK?", "/understand/learning-disability/"),
    ("Why can understanding or using language be difficult?", "/understand/developmental-language-disorder/"),
)
RESOURCE_RECORDS = build_site.load_resources()
QUESTION_RECORDS = build_site.load_questions()
CONCEPT_RECORDS = build_site.load_concepts()
EVIDENCE_RECORDS = build_site.load_evidence()
RESOURCE_RECORD_MAP = {x["id"]: x for x in RESOURCE_RECORDS}
QUESTION_RECORD_MAP = {x["id"]: x for x in QUESTION_RECORDS}
CONCEPT_RECORD_MAP = {x["id"]: x for x in CONCEPT_RECORDS}
EVIDENCE_RECORD_MAP = {x["id"]: x for x in EVIDENCE_RECORDS}
RESOURCE_MARKERS = {
    f"/resources/{rid}/": (RESOURCE_RECORD_MAP[rid]["name"], next(l["value"] for l in RESOURCE_RECORD_MAP[rid].get("locators", []) if l.get("type") == "url"))
    for rid in ("access-to-work", "adhd-uk", "autistic-self-advocacy-network", "autistica", "autistica-tips-hub", "goblin-tools", "habitica", "minecraft", "molehill-mountain", "national-autistic-society", "stardew-valley", "tiimo", "time-timer", "unmasking-autism", "unpacking") if rid in RESOURCE_RECORD_MAP
}
RESOURCE_MARKERS_V10 = {f"/resources/{x['id']}/": (x["name"], next(l["value"] for l in x.get("locators", []) if l.get("type") == "url")) for x in RESOURCE_RECORDS}
QUESTION_MARKERS_V10 = {f"/questions/{x['id']}/": x["question"] for x in QUESTION_RECORDS}
CONCEPT_MARKERS_V10 = {f"/understand/{x['id']}/": x["name"] for x in CONCEPT_RECORDS}
COMPATIBILITY_NOINDEX_ROUTES = ("/oracle/",)
NOINDEX_MARKER = '<meta name="robots" content="noindex, follow">'
NOT_FOUND_PATH = "/__nd_oracle_live_verifier_missing_page__/"
NOT_FOUND_MARKER = "<h1>Page not found</h1>"
CLOUDFLARE_MANAGED_BEGIN = "# BEGIN Cloudflare Managed content"
CLOUDFLARE_MANAGED_END = "# END Cloudflare Managed Content"
CLOUDFLARE_CONTENT_SIGNAL = "Content-Signal: search=yes,ai-train=no,use=reference"
SECURITY_HEADERS = {
    "content-security-policy": "default-src 'none'; style-src 'self'; img-src 'self' data:; font-src 'self'; script-src 'self'; connect-src 'none'; media-src 'self'; manifest-src 'self'; object-src 'none'; base-uri 'none'; form-action 'none'; frame-ancestors 'none'; upgrade-insecure-requests",
    "strict-transport-security": "max-age=31536000",
    "cross-origin-opener-policy": "same-origin", "cross-origin-resource-policy": "same-origin",
    "x-frame-options": "DENY", "x-content-type-options": "nosniff",
    "x-permitted-cross-domain-policies": "none", "referrer-policy": "no-referrer",
    "permissions-policy": "accelerometer=(), camera=(), geolocation=(), gyroscope=(), magnetometer=(), microphone=(), payment=(), usb=()",
}
STABLE_BASE_MARKERS = (
    ("/", "Understand neurodivergence without doing all the digging yourself"), ("/understand/", "<h1>Understand</h1>"),
    ("/resources/", "<h1>Resources</h1>"), ("/tools/", "<h1>Tools &amp; practical help</h1>"),
    ("/games/", "<h1>Games</h1>"), ("/community/", "<h1>Support &amp; organisations</h1>"),
    ("/books-media/", "<h1>Books &amp; media</h1>"), ("/questions/", "<h1>Questions</h1>"),
    ("/how-it-works/", "<h1>How this site works</h1>"), ("/about/", "<h1>About</h1>"),
    ("/accessibility/", "<h1>Accessibility</h1>"), ("/feedback/", "<h1>Feedback</h1>"), ("/privacy/", "<h1>Privacy</h1>"),
)
NAVIGATION_MARKERS = (
    ("/needs/", "<h1>Browse by need</h1>"), ("/needs/daily-life/", "<h1>Daily life</h1>"),
    ("/needs/sensory-environment/", "<h1>Sensory &amp; environment</h1>"), ("/needs/communication/", "<h1>Communication</h1>"),
    ("/needs/work/", "<h1>Work</h1>"), ("/needs/education-study/", "<h1>Education &amp; study</h1>"),
    ("/needs/assessment-diagnosis/", "<h1>Assessment &amp; diagnosis</h1>"), ("/needs/health-wellbeing/", "<h1>Health &amp; wellbeing</h1>"),
    ("/needs/relationships-family/", "<h1>Relationships &amp; family</h1>"), ("/types/", "<h1>Browse by content type</h1>"),
    ("/places/", "<h1>Browse by geographic scope</h1>"), ("/a-z/", "<h1>A–Z</h1>"), ("/find/", "<h1>Find a governed route</h1>"),
)
ROUTES = tuple([STABLE_BASE_MARKERS[0], STABLE_BASE_MARKERS[1]] + [(p, f"<h1>{html.escape(n, quote=True)}</h1>") for p, n in CONCEPT_MARKERS_V10.items()] + list(STABLE_BASE_MARKERS[2:7]) + [(p, f"<h1>{html.escape(n, quote=True)}</h1>") for p, (n, _u) in RESOURCE_MARKERS_V10.items()] + [STABLE_BASE_MARKERS[7]] + [(p, f"<h1>{html.escape(q, quote=True)}</h1>") for p, q in QUESTION_MARKERS_V10.items()] + list(STABLE_BASE_MARKERS[8:]) + list(NAVIGATION_MARKERS))
EVIDENCE_MARKERS = tuple(build_site.evidence_route_markers())
ROUTES = tuple(list(ROUTES) + list(EVIDENCE_MARKERS))
V10_ROUTES = ROUTES
V09_ROUTES = ROUTES
if len(ROUTES) != build_site.V10_ROUTE_COUNT: raise RuntimeError(f"v1.0 verifier route count mismatch: expected {build_site.V10_ROUTE_COUNT}, got {len(ROUTES)}")
if len({p for p, _ in ROUTES}) != len(ROUTES): raise RuntimeError("v1.0 verifier contains duplicate routes")
if {p for p, _ in ROUTES} != set(build_site.sitemap_paths(CONCEPT_RECORDS, RESOURCE_RECORDS, QUESTION_RECORDS)): raise RuntimeError("v1.0 builder/verifier route sets differ")

@dataclass(frozen=True)
class Response:
    status: int; final_url: str; content_type: str; body: str; headers: dict[str, str] = field(default_factory=dict)
class SurfaceParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True); self.forms=0; self.iframes=0; self.scripts=[]; self.loaded_resources=[]
    def handle_starttag(self, tag, attrs) -> None:
        values={n.lower():v or "" for n,v in attrs}; tag=tag.lower()
        if tag=="form": self.forms+=1
        if tag=="iframe": self.iframes+=1
        if tag=="script": self.scripts.append(values)
        if tag in {"img","script","iframe","audio","video","source"}:
            src=values.get("src","").strip()
            if src: self.loaded_resources.append(src)
        elif tag=="link":
            rel={x.lower() for x in values.get("rel","").split()}
            if rel.intersection({"stylesheet","preload","modulepreload","icon","manifest"}):
                href=values.get("href","").strip()
                if href: self.loaded_resources.append(href)
    def handle_startendtag(self,tag,attrs): self.handle_starttag(tag,attrs)
def normalize_header_value(value: str) -> str: return " ".join(value.split())
def fetch_url(url: str, timeout: float=20.0) -> Response:
    request=urllib.request.Request(url,headers={"User-Agent":USER_AGENT,"Accept":"*/*"})
    try:
        with urllib.request.urlopen(request,timeout=timeout) as r: return Response(r.status,r.geturl(),r.headers.get("Content-Type",""),r.read().decode("utf-8",errors="replace"),{k.lower():v for k,v in r.headers.items()})
    except urllib.error.HTTPError as exc: return Response(exc.code,exc.geturl(),exc.headers.get("Content-Type",""),exc.read().decode("utf-8",errors="replace"),{k.lower():v for k,v in exc.headers.items()})
fetch_html=fetch_url
def expected_url(origin: str,path: str) -> str: return origin.rstrip("/")+path
def canonical_marker(url: str) -> str: return f'<link rel="canonical" href="{url}">'
def verify_security_headers(path: str,response: Response) -> list[str]:
    failures=[]
    for name,expected in SECURITY_HEADERS.items():
        actual=response.headers.get(name)
        if actual is None: failures.append(f"{path}: missing security header {name}")
        elif normalize_header_value(actual)!=normalize_header_value(expected): failures.append(f"{path}: security header {name} mismatch: got {actual!r}; expected {expected!r}")
    return failures
def verify_passive_surface(origin: str,path: str,response: Response) -> list[str]:
    parser=SurfaceParser(); parser.feed(response.body); failures=[]
    if parser.forms: failures.append(f"{path}: unexpected form element present")
    if parser.iframes: failures.append(f"{path}: unexpected iframe element present")
    if path=="/find/":
        if len(parser.scripts)!=1 or parser.scripts[0].get("src")!="/find.js": failures.append("/find/: exactly one local /find.js script is required")
    elif parser.scripts: failures.append(f"{path}: unexpected script element present")
    host=urlsplit(origin).netloc.lower()
    for resource in parser.loaded_resources:
        if resource.startswith("data:"): continue
        parsed=urlsplit(urljoin(origin+"/",resource))
        if parsed.scheme not in {"http","https"} or parsed.netloc.lower()!=host: failures.append(f"{path}: unexpected externally loaded resource {resource!r}")
    return failures
def verify_route(origin: str,path: str,marker: str,*,fetcher=fetch_url) -> list[str]:
    url=expected_url(origin,path); r=fetcher(url); failures=[]
    if r.status!=200: failures.append(f"{path}: expected HTTP 200, got {r.status}")
    if r.final_url!=url: failures.append(f"{path}: unexpected final URL {r.final_url!r}; expected {url!r}")
    if "text/html" not in r.content_type.lower(): failures.append(f"{path}: expected text/html, got {r.content_type!r}")
    if marker not in r.body: failures.append(f"{path}: expected page marker not found: {marker!r}")
    if canonical_marker(url) not in r.body: failures.append(f"{path}: expected canonical link not found")
    if NOINDEX_MARKER in r.body: failures.append(f"{path}: canonical public route unexpectedly carries noindex")
    failures.extend(verify_security_headers(path,r)); failures.extend(verify_passive_surface(origin,path,r)); return failures
def verify_routes(origin: str,*,fetcher=fetch_url) -> list[str]:
    failures=[]
    for path,marker in ROUTES:
        route_failures=verify_route(origin,path,marker,fetcher=fetcher)
        if route_failures: failures.extend(route_failures)
        else: print(f"PASS canonical {path}")
    return failures
def verify_v06_reading_contract(origin: str,*,fetcher=fetch_url) -> list[str]:
    failures=[]; home=fetcher(expected_url(origin,"/"))
    for question,target in HOMEPAGE_QUESTIONS:
        if question not in home.body: failures.append(f"/: missing v0.6 homepage question {question!r}")
        if f'href="{target}"' not in home.body: failures.append(f"/: missing v0.6 homepage route to {target}")
    for marker in ("Explore useful things",'href="/resources/"','href="/tools/"','href="/games/"','href="/community/"',"A listing is not an endorsement"):
        if marker not in home.body: failures.append(f"/: ecosystem marker missing: {marker!r}")
    for path,first in TOPIC_FIRST_READ_MARKERS.items():
        r=fetcher(expected_url(origin,path))
        for marker,label in ((html.escape(first,quote=True),"simple first-read explanation"),('class="review-meta">Last reviewed:',"visible Last reviewed metadata"),('<details class="technical-summary"><summary>More precise description</summary>',"precise-description disclosure"),('href="/how-it-works/#confidence"',"confidence explanation link")):
            if marker not in r.body: failures.append(f"{path}: {label} is missing")
    how=fetcher(expected_url(origin,"/how-it-works/"))
    for marker in ('<h2>What the confidence labels mean</h2>','<dt>High</dt>','<dt>Moderate</dt>','<dt>Low</dt>','<dt>Contested</dt>','<dt>Not applicable</dt>','<h2>Being listed is not being endorsed</h2>'):
        if marker not in how.body: failures.append(f"/how-it-works/: contract marker missing: {marker!r}")
    feedback=fetcher(expected_url(origin,"/feedback/"))
    for marker in ('<h2>Report a problem</h2>','href="https://github.com/armpitpete/nd-oracle/issues/new"','Please do not include private health information','<h2>Current limitation</h2>'):
        if marker not in feedback.body: failures.append(f"/feedback/: feedback boundary marker missing: {marker!r}")
    if not failures: print("PASS v0.6 public-reading compatibility contract")
    return failures
def verify_v06_resource_contract(origin: str,*,fetcher=fetch_url) -> list[str]:
    failures=[]
    for path,(name,url) in RESOURCE_MARKERS.items():
        r=fetcher(expected_url(origin,path)); rid=path.split("/")[-2]; required=["Listed, not endorsed","Last reviewed:",'<h2 id="use-heading">What it is for</h2>','<h2 id="access-heading">Access</h2>','<h2 id="limits-heading">Limitations and possible poor fit</h2>','<h2 id="cost-heading">Cost and access notes</h2>','<h2 id="conflict-heading">Ownership and conflicts</h2>','<h2 id="evidence-status-heading">Evidence status</h2>',f'href="{html.escape(url,quote=True)}"']
        if not RESOURCE_RECORD_MAP[rid].get("claims"): required.append("This listing makes no efficacy or safety claim")
        for marker in required:
            if marker not in r.body: failures.append(f"{path}: resource contract marker missing for {name}: {marker!r}")
    if not failures: print(f"PASS v0.6 resource compatibility contract ({len(RESOURCE_MARKERS)} resources)")
    return failures
def load_compatibility_fixture() -> dict: return json.loads(COMPATIBILITY_FIXTURE.read_text(encoding="utf-8"))
def verify_compatibility_fixture() -> list[str]:
    fixture=load_compatibility_fixture(); failures=[]; resources=set(RESOURCE_RECORD_MAP); questions=set(QUESTION_RECORD_MAP); concepts=set(CONCEPT_RECORD_MAP)
    for version in ("v06","v07","v08","v09"):
        data=fixture.get(version,{})
        for key,current in (("concept_ids",concepts),("resource_ids",resources),("question_ids",questions)):
            missing=set(data.get(key,[]))-current
            if missing: failures.append(f"{version} compatibility: missing {key} {sorted(missing)}")
    if not failures: print("PASS frozen public compatibility fixture")
    return failures
def verify_v08_subset_preserved() -> list[str]: return verify_compatibility_fixture()
def verify_v10_concept_contract(origin: str,*,fetcher=fetch_url) -> list[str]:
    failures=[]; idx=fetcher(expected_url(origin,"/understand/"))
    if f"There are {len(CONCEPT_RECORDS)} reviewed topic pages" not in idx.body: failures.append("/understand/: current Concept count is missing")
    for concept in CONCEPT_RECORDS:
        path=f'/understand/{concept["id"]}/'; r=fetcher(expected_url(origin,path))
        for marker in (html.escape(build_site.reader_intro(concept),quote=True),html.escape(concept["summary"],quote=True),'class="review-meta">Last reviewed:','<details class="technical-summary"><summary>More precise description</summary>','<h2 id="next-routes-heading">Useful next routes</h2>','href="/how-it-works/#confidence"'):
            if marker not in r.body: failures.append(f"{path}: concept marker missing: {marker!r}")
    if not failures: print(f"PASS v1.0 Concept contract ({len(CONCEPT_RECORDS)})")
    return failures
def verify_v10_question_contract(origin: str,*,fetcher=fetch_url) -> list[str]:
    failures=[]; idx=fetcher(expected_url(origin,"/questions/"))
    for marker in ("Relevant to inspect, not recommended.",f"{len(QUESTION_RECORDS)} governed practical questions",'href="/needs/"','href="/a-z/"'):
        if marker not in idx.body: failures.append(f"/questions/: marker missing {marker!r}")
    for path,_q in QUESTION_MARKERS_V10.items():
        r=fetcher(expected_url(origin,path))
        for marker in ("Relevant to inspect, not recommended.",'<h2 id="current-understanding-heading">Current understanding</h2>','<h2 id="related-things-heading">Related things to inspect</h2>','<h2 id="related-questions-heading">Related questions</h2>','<h2 id="evidence-needed-heading">What evidence is still needed</h2>','<h2 id="dissent-heading">Where people may disagree</h2>','<h2 id="reopen-heading">When this answer should be revisited</h2>'):
            if marker not in r.body: failures.append(f"{path}: question marker missing {marker!r}")
    if not failures: print(f"PASS v1.0 Question contract ({len(QUESTION_RECORDS)})")
    return failures
def verify_v10_resource_contract(origin: str,*,fetcher=fetch_url) -> list[str]:
    failures=[]
    for path,(name,url) in RESOURCE_MARKERS_V10.items():
        r=fetcher(expected_url(origin,path)); rid=path.split("/")[-2]
        for marker in ("Listed, not endorsed","Last reviewed:",'<h2 id="use-heading">What it is for</h2>','<h2 id="access-heading">Access</h2>','<h2 id="resource-question-heading">Questions that lead here</h2>','<h2 id="scope-heading">Scope for navigation</h2>','<h2 id="limits-heading">Limitations and possible poor fit</h2>','<h2 id="cost-heading">Cost and access notes</h2>','<h2 id="conflict-heading">Ownership and conflicts</h2>','<h2 id="evidence-status-heading">Evidence status</h2>',f'href="{html.escape(url,quote=True)}"'):
            if marker not in r.body: failures.append(f"{path}: resource marker missing for {name}: {marker!r}")
        claims=RESOURCE_RECORD_MAP[rid].get("claims",[])
        if claims:
            for marker in ('<h2 id="governed-resource-claims-heading">Governed claims and evidence</h2>',"A supported claim is not a recommendation or an individual decision.","Evidence route","Uncertainty and limits"):
                if marker not in r.body: failures.append(f"{path}: claim-bearing marker missing {marker!r}")
        elif "This listing makes no efficacy or safety claim" not in r.body: failures.append(f"{path}: claimless boundary missing")
    if not failures: print(f"PASS v1.0 Resource contract ({len(RESOURCE_RECORDS)})")
    return failures
def verify_v10_navigation_contract(origin: str,*,fetcher=fetch_url) -> list[str]:
    failures=[]; home=fetcher(expected_url(origin,"/"))
    for marker in ('href="/needs/"','href="/types/"','href="/places/"','href="/a-z/"','href="/find/"'):
        if marker not in home.body: failures.append(f"/: browse marker missing {marker!r}")
    needs=fetcher(expected_url(origin,"/needs/"))
    for q in QUESTION_RECORDS:
        if f'href="/questions/{q["id"]}/"' not in needs.body: failures.append(f"/needs/: missing {q['id']}")
    places=fetcher(expected_url(origin,"/places/"))
    for heading in ("England and Wales","Scotland","Wales","Northern Ireland"):
        if heading not in places.body: failures.append(f"/places/: missing jurisdiction {heading}")
    az=fetcher(expected_url(origin,"/a-z/"))
    for c in CONCEPT_RECORDS:
        if f'href="/understand/{c["id"]}/"' not in az.body: failures.append(f"/a-z/: missing concept {c['id']}")
    for r in RESOURCE_RECORDS:
        if f'href="/resources/{r["id"]}/"' not in az.body: failures.append(f"/a-z/: missing resource {r['id']}")
    for q in QUESTION_RECORDS:
        if f'href="/questions/{q["id"]}/"' not in az.body: failures.append(f"/a-z/: missing question {q['id']}")
    find=fetcher(expected_url(origin,"/find/"))
    for marker in ("Local governed discovery.","Your words stay in this browser page",'src="/find.js"',"Relevance means worth inspecting, not recommended."):
        if marker not in find.body: failures.append(f"/find/: marker missing {marker!r}")
    if not failures: print("PASS v1.0 navigation/discovery contract")
    return failures
verify_v09_concept_contract=verify_v10_concept_contract
verify_v09_question_contract=verify_v10_question_contract
verify_v09_resource_contract=verify_v10_resource_contract
verify_v09_navigation_contract=verify_v10_navigation_contract
def verify_not_found(origin: str,*,fetcher=fetch_url) -> list[str]:
    url=expected_url(origin,NOT_FOUND_PATH); r=fetcher(url); failures=[]
    if r.status!=404: failures.append(f"404: expected HTTP 404, got {r.status}")
    if r.final_url!=url: failures.append(f"404: unexpected final URL {r.final_url!r}; expected {url!r}")
    if "text/html" not in r.content_type.lower(): failures.append(f"404: expected text/html, got {r.content_type!r}")
    if NOT_FOUND_MARKER not in r.body: failures.append("404: expected not-found page marker is missing")
    if NOINDEX_MARKER not in r.body: failures.append("404: expected noindex marker is missing")
    failures.extend(verify_security_headers("404",r)); failures.extend(verify_passive_surface(origin,"404",r)); return failures
def verify_compatibility_noindex_routes(origin: str,*,fetcher=fetch_url) -> list[str]:
    failures=[]
    for path in COMPATIBILITY_NOINDEX_ROUTES:
        url=expected_url(origin,path); r=fetcher(url)
        if r.status!=200: failures.append(f"{path}: expected compatibility HTTP 200, got {r.status}")
        if r.final_url!=url: failures.append(f"{path}: unexpected final URL")
        if NOINDEX_MARKER not in r.body: failures.append(f"{path}: expected noindex marker is missing")
        failures.extend(verify_security_headers(path,r)); failures.extend(verify_passive_surface(origin,path,r))
    return failures
def expected_sitemap_urls(origin: str) -> set[str]: return {expected_url(origin,p) for p,_ in ROUTES}
def expected_origin_robots(origin: str) -> str: return f"User-agent: *\nAllow: /\nSitemap: {origin}/sitemap.xml\n"
def verify_robots_content(origin: str,body: str) -> list[str]:
    actual=body.replace("\r\n","\n"); expected=expected_origin_robots(origin); failures=[]
    if not actual.endswith(expected): failures.append(f"robots.txt: origin indexing/sitemap block is missing or changed: expected trailing block={expected!r}")
    managed=CLOUDFLARE_MANAGED_BEGIN in actual or CLOUDFLARE_MANAGED_END in actual
    if managed:
        if CLOUDFLARE_MANAGED_BEGIN not in actual or CLOUDFLARE_MANAGED_END not in actual: failures.append("robots.txt: incomplete Cloudflare managed-content block")
        if "".join(CLOUDFLARE_CONTENT_SIGNAL.lower().split()) not in "".join(actual.lower().split()): failures.append("robots.txt: Cloudflare managed content signal changed; expected search=yes, ai-train=no, use=reference")
    return failures
def verify_metadata_files(origin: str,*,fetcher=fetch_url) -> list[str]:
    failures=[]; robots_url=expected_url(origin,"/robots.txt"); robots=fetcher(robots_url)
    if robots.status!=200: failures.append(f"robots.txt: expected HTTP 200, got {robots.status}")
    if robots.final_url!=robots_url: failures.append("robots.txt: unexpected final URL")
    failures.extend(verify_robots_content(origin,robots.body)); sitemap_url=expected_url(origin,"/sitemap.xml"); sitemap=fetcher(sitemap_url)
    if sitemap.status!=200: failures.append(f"sitemap.xml: expected HTTP 200, got {sitemap.status}")
    try: root=ET.fromstring(sitemap.body); actual={(e.text or "").strip() for e in root.findall("{http://www.sitemaps.org/schemas/sitemap/0.9}url/{http://www.sitemaps.org/schemas/sitemap/0.9}loc")}
    except ET.ParseError as exc: failures.append(f"sitemap.xml: invalid XML: {exc}"); actual=set()
    expected=expected_sitemap_urls(origin)
    if actual!=expected: failures.append(f"sitemap.xml: URL set mismatch: missing={sorted(expected-actual)}; unexpected={sorted(actual-expected)}")
    return failures
def verify_www_redirect(origin: str,*,fetcher=fetch_url) -> list[str]:
    failures=[]; target=f"{origin}/understand/?q=nd-oracle-live-verify"
    for scheme in ("http","https"):
        source=f"{scheme}://www.ndoracle.org/understand/?q=nd-oracle-live-verify"; r=fetcher(source)
        if r.status!=200: failures.append(f"www redirect from {scheme}: final response expected HTTP 200, got {r.status}")
        if r.final_url!=target: failures.append(f"www redirect from {scheme}: expected final URL {target!r}, got {r.final_url!r}")
        if "<h1>Understand</h1>" not in r.body: failures.append(f"www redirect from {scheme}: target page marker is missing")
        failures.extend(verify_security_headers(f"www-{scheme}",r))
    return failures
def verify_production(origin: str,*,fetcher=fetch_url) -> list[str]:
    failures=[]
    for func in (verify_routes,verify_v06_reading_contract,verify_v06_resource_contract,verify_v10_concept_contract,verify_v10_question_contract,verify_v10_resource_contract,verify_v10_navigation_contract,verify_not_found,verify_metadata_files,verify_compatibility_noindex_routes,verify_www_redirect): failures.extend(func(origin,fetcher=fetcher))
    failures.extend(verify_compatibility_fixture()); return failures
def parse_args(argv: list[str]) -> argparse.Namespace:
    parser=argparse.ArgumentParser(description="Verify ND Oracle v1.0 production public-surface and governed discovery contracts over HTTPS."); parser.add_argument("--origin",default=DEFAULT_ORIGIN); return parser.parse_args(argv)
def main(argv: list[str]|None=None) -> int:
    args=parse_args(sys.argv[1:] if argv is None else argv); origin=args.origin.rstrip("/")
    if not origin.startswith("https://"): print("Refusing non-HTTPS production origin.",file=sys.stderr); return 2
    try: failures=verify_production(origin)
    except (OSError,urllib.error.URLError) as exc: print(f"LIVE VERIFICATION ERROR: {exc}",file=sys.stderr); return 1
    if failures:
        print("LIVE VERIFICATION FAIL",file=sys.stderr)
        for failure in failures: print(f"- {failure}",file=sys.stderr)
        return 1
    print(f"Verified {len(ROUTES)} canonical routes plus v1.0 governed discovery/evidence and frozen compatibility contracts at {origin}."); return 0
if __name__=="__main__": raise SystemExit(main())
