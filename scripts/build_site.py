from __future__ import annotations

import html
import json
import shutil
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
OBJECTS_DIR = ROOT / "objects" / "concepts"
SITE_DIR = ROOT / "site"
DEFAULT_OUTPUT_DIR = ROOT / "dist"
OUTPUT_MARKER = "nd-oracle-site-v0.1\n"

PRIMARY_NAV = [
    ("understand", "Understand"),
    ("tools", "Tools"),
    ("games", "Games"),
    ("resources", "Resources"),
    ("community", "Community"),
    ("oracle", "Oracle"),
]

STATIC_PAGES = {
    "tools": {
        "title": "Tools",
        "intro": "Practical neurodivergent-friendly tools will live here.",
        "body": (
            "<p>This route is ready for small, focused tools that solve one problem well. "
            "Tools are not yet active in Site Shell v0.1.</p>"
            "<p>Future tools should work without accounts where possible, minimise data collection, "
            "and state clearly what they do and do not do.</p>"
        ),
    },
    "games": {
        "title": "Games",
        "intro": "Small games and playful experiments designed with neurodivergent people in mind.",
        "body": (
            "<p>This route is reserved for games that are useful, interesting or simply enjoyable. "
            "No game is active in Site Shell v0.1.</p>"
            "<p>Games may later use JavaScript, but the rest of the site remains usable without it.</p>"
        ),
    },
    "resources": {
        "title": "Resources",
        "intro": "A future catalogue of useful books, apps, organisations, services and communities.",
        "body": (
            "<p>Resource listings will be separated from endorsements. Each listing should say what "
            "it is, who it may help, and what is known or uncertain about it.</p>"
        ),
    },
    "community": {
        "title": "Community",
        "intro": "A route for contribution without turning the site into a social network.",
        "body": (
            "<p>Community features are deliberately limited at this stage. There are no accounts, "
            "profiles, comments, direct messages or public submissions.</p>"
            "<p>Future contribution routes may include corrections, resource suggestions, tool ideas "
            "and lived-experience contributions after privacy and safeguarding review.</p>"
        ),
    },
    "oracle": {
        "title": "Oracle",
        "intro": "The deeper evidence and provenance system is being built in parallel.",
        "body": (
            "<p>The Oracle is not an AI authority and is not active on this site yet. Its job is to "
            "keep claims connected to evidence, uncertainty, competing perspectives and revision history.</p>"
            "<p>When integrated, the public website will consume validated Oracle knowledge rather than "
            "letting generated answers become the source of truth.</p>"
        ),
    },
    "about": {
        "title": "About",
        "intro": "The Neurodiverse Oracle is a practical knowledge commons for neurodivergent people.",
        "body": (
            "<p>The project is being built in two parallel lanes: a useful public commons and a "
            "provenance-first knowledge system underneath it.</p>"
            "<p>Success is measured by useful epistemic work saved, not by how much content is produced.</p>"
        ),
    },
    "accessibility": {
        "title": "Accessibility",
        "intro": "The site should reduce cognitive and sensory burden rather than add to it.",
        "body": (
            "<p>Site Shell v0.1 uses semantic HTML, visible keyboard focus, restrained colours, a "
            "reading-width content column and no required JavaScript.</p>"
            "<p>Accessibility problems are defects. Future interactive features must preserve keyboard "
            "access, reduced-motion preferences and clear language.</p>"
        ),
    },
    "privacy": {
        "title": "Privacy",
        "intro": "Site Shell v0.1 is designed to collect no personal data.",
        "body": (
            "<p>There are currently no accounts, forms, analytics scripts, advertising trackers or "
            "personalised features in the generated site.</p>"
            "<p>Any feature that stores queries, profiles, health information or community submissions "
            "requires a separate privacy and threat-model review before release.</p>"
        ),
    },
}


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def safe_http_url(value: object) -> str | None:
    if not isinstance(value, str):
        return None
    parsed = urlsplit(value)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        return None
    return value


def load_concepts() -> list[dict]:
    concepts = []
    for path in sorted(OBJECTS_DIR.glob("*.json")):
        with path.open("r", encoding="utf-8") as handle:
            concepts.append(json.load(handle))
    return sorted(concepts, key=lambda item: item["name"].casefold())


def list_items(values: list[str]) -> str:
    return "<ul>" + "".join(f"<li>{esc(value)}</li>" for value in values) + "</ul>"


def nav(current: str | None = None) -> str:
    links = []
    for slug, label in PRIMARY_NAV:
        current_attr = ' aria-current="page"' if slug == current else ""
        links.append(f'<a href="/{slug}/"{current_attr}>{esc(label)}</a>')
    return '<nav class="primary-nav" aria-label="Primary">' + "".join(links) + "</nav>"


def page_shell(title: str, intro: str, body: str, current: str | None = None) -> str:
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="color-scheme" content="light">
  <meta name="theme-color" content="#f5f4ef">
  <title>{esc(title)} · The Neurodiverse Oracle</title>
  <link rel="stylesheet" href="/styles.css">
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header">
  <div class="site-shell header-row">
    <a class="site-name" href="/">The Neurodiverse Oracle</a>
    {nav(current)}
  </div>
</header>
<main id="main" class="site-shell reading-column">
  <header class="page-heading">
    <h1>{esc(title)}</h1>
    <p class="lede">{esc(intro)}</p>
  </header>
  {body}
</main>
<footer class="site-footer">
  <div class="site-shell footer-row">
    <span>Built for usefulness, provenance and revision.</span>
    <nav aria-label="Footer">
      <a href="/about/">About</a>
      <a href="/accessibility/">Accessibility</a>
      <a href="/privacy/">Privacy</a>
    </nav>
  </div>
</footer>
</body>
</html>
"""


def card(title: str, summary: str, href: str, eyebrow: str | None = None) -> str:
    label = f'<div class="eyebrow">{esc(eyebrow)}</div>' if eyebrow else ""
    return f"""<article class="card">
  {label}
  <h2><a href="{esc(href)}">{esc(title)}</a></h2>
  <p>{esc(summary)}</p>
</article>"""


def render_index(concepts: list[dict]) -> str:
    section_cards = [
        card("Understand", "Clear explanations backed by visible evidence and uncertainty.", "/understand/"),
        card("Tools", "Practical tools built to reduce friction rather than add setup.", "/tools/"),
        card("Games", "Useful, curious and playful neurodivergent-friendly experiences.", "/games/"),
        card("Resources", "Books, apps, services, organisations and communities.", "/resources/"),
        card("Community", "Future contribution routes for corrections, suggestions and lived experience.", "/community/"),
        card("Oracle", "The provenance-first knowledge system being built underneath the public site.", "/oracle/"),
    ]
    concept_links = "".join(
        f'<li><a href="/understand/{esc(concept["id"])}/">{esc(concept["name"])}</a></li>'
        for concept in concepts
    )
    body = f"""
<section class="notice" aria-label="Status">
  <strong>Site Shell v0.1.</strong> The structure is live in the build, while tools, games, community
  features and the Oracle remain deliberately inactive.
</section>
<section aria-labelledby="explore-heading">
  <h2 id="explore-heading">Explore</h2>
  <div class="grid">{''.join(section_cards)}</div>
</section>
<section aria-labelledby="seed-heading">
  <h2 id="seed-heading">Current knowledge seed</h2>
  <p>The first five knowledge objects are available now under Understand.</p>
  <ul class="compact-list">{concept_links}</ul>
</section>
"""
    return page_shell(
        "A calmer place to understand neurodivergence",
        "Useful things first, with a rigorous evidence and uncertainty system underneath.",
        body,
    )


def render_understand_index(concepts: list[dict]) -> str:
    cards = "".join(
        card(
            concept["name"],
            concept["summary"],
            f'/understand/{concept["id"]}/',
            f'{concept["type"]} · {concept["status"]}',
        )
        for concept in concepts
    )
    body = f"""
<section class="notice">
  <strong>Early seed material.</strong> These pages are for orientation and research traceability.
  They are not diagnosis or medical advice.
</section>
<section aria-labelledby="concepts-heading">
  <h2 id="concepts-heading">Concepts</h2>
  <div class="grid">{cards}</div>
</section>
"""
    return page_shell(
        "Understand",
        "Plain-language concept pages that keep claims connected to evidence, uncertainty and perspectives.",
        body,
        current="understand",
    )


def render_concept(concept: dict) -> str:
    source_map = {source["id"]: source for source in concept["sources"]}
    uncertainty_map = {item["id"]: item for item in concept["uncertainties"]}

    for claim in concept["claims"]:
        for source_id in claim["source_ids"]:
            if source_id not in source_map:
                raise ValueError(f"{concept['id']}: missing source {source_id}")
        for uncertainty_id in claim["uncertainty_ids"]:
            if uncertainty_id not in uncertainty_map:
                raise ValueError(f"{concept['id']}: missing uncertainty {uncertainty_id}")

    claims = []
    for claim in concept["claims"]:
        source_links = ", ".join(
            f'<a href="#source-{esc(source_id)}">{esc(source_id)}</a>' for source_id in claim["source_ids"]
        )
        uncertainty_links = ", ".join(
            f'<a href="#uncertainty-{esc(uncertainty_id)}">{esc(uncertainty_id)}</a>'
            for uncertainty_id in claim["uncertainty_ids"]
        )
        claims.append(
            f"""<article class="claim" id="claim-{esc(claim['id'])}">
  <div class="claim-head"><h3>{esc(claim['text'])}</h3><span class="confidence">{esc(claim['confidence'])} confidence</span></div>
  <div class="route"><div><span class="route-label">Evidence:</span> {source_links}</div><div><span class="route-label">Uncertainty:</span> {uncertainty_links}</div></div>
</article>"""
        )

    uncertainties = []
    for item in concept["uncertainties"]:
        uncertainties.append(
            f"""<article class="uncertainty" id="uncertainty-{esc(item['id'])}">
  <h3>{esc(item['question'])}</h3>
  <p><strong>Why it matters:</strong> {esc(item['why_it_matters'])}</p>
  <div><strong>What would reduce it:</strong>{list_items(item['what_would_reduce_it'])}</div>
  <div class="status">Status: {esc(item['status'])}</div>
</article>"""
        )

    perspectives = []
    for item in concept["perspectives"]:
        source_links = ", ".join(
            f'<a href="#source-{esc(source_id)}">{esc(source_id)}</a>' for source_id in item["source_ids"]
        )
        perspectives.append(
            f"""<article class="perspective">
  <h3>{esc(item['held_by'])}</h3>
  <p>{esc(item['summary'])}</p>
  <div class="route"><span class="route-label">Sources:</span> {source_links}</div>
</article>"""
        )

    sources = []
    for source in concept["sources"]:
        url = safe_http_url(source.get("url"))
        link = f'<a href="{esc(url)}" rel="noopener noreferrer">Open source</a>' if url else "No safe public URL recorded"
        sources.append(
            f"""<article class="source" id="source-{esc(source['id'])}">
  <h3>{esc(source['citation'])}</h3>
  <div class="meta">Kind: {esc(source['kind'])} · accessed {esc(source['accessed'])}</div>
  <p>{link}</p>
</article>"""
        )

    relations = []
    for relation in concept["relations"]:
        relations.append(
            f'<li><a href="/understand/{esc(relation["target_id"])}/">{esc(relation["target_id"])}</a> — {esc(relation["note"])}</li>'
        )

    body = f"""
<p class="back-link"><a href="/understand/">← Understand</a></p>
<div class="eyebrow">{esc(concept['type'])} · {esc(concept['status'])}</div>
<section class="notice">
  <strong>Early seed material.</strong> This page is not diagnosis or medical advice. Claims remain
  linked to their recorded evidence and uncertainty.
</section>
<section><h2>Scope</h2><h3>Includes</h3>{list_items(concept['scope']['includes'])}<h3>Excludes</h3>{list_items(concept['scope']['excludes'])}</section>
<section><h2>Claims</h2>{''.join(claims)}</section>
<section><h2>Uncertainties</h2>{''.join(uncertainties)}</section>
<section><h2>Perspectives</h2>{''.join(perspectives)}</section>
<section><h2>Related concepts</h2><ul>{''.join(relations)}</ul></section>
<section><h2>Sources</h2>{''.join(sources)}</section>
<section><h2>Provenance</h2><p>{esc(concept['provenance']['method'])}</p><div class="meta">Created {esc(concept['provenance']['created'])} · review state {esc(concept['provenance']['review_state'])}</div></section>
"""
    return page_shell(concept["name"], concept["summary"], body, current="understand")


def render_static_page(slug: str) -> str:
    page = STATIC_PAGES[slug]
    return page_shell(page["title"], page["intro"], page["body"], current=slug if slug in dict(PRIMARY_NAV) else None)


def prepare_output(output_dir: Path) -> None:
    marker = output_dir / ".nd-oracle-generated"
    if output_dir.is_symlink():
        raise ValueError(f"Refusing to replace symlink output directory: {output_dir}")
    if output_dir.exists():
        if not marker.is_file() or marker.read_text(encoding="utf-8") != OUTPUT_MARKER:
            raise ValueError(f"Refusing to replace unmarked output directory: {output_dir}")
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True)
    marker.write_text(OUTPUT_MARKER, encoding="utf-8")


def write_route(output_dir: Path, route: str, content: str) -> None:
    target = output_dir / route / "index.html"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")


def build(output_dir: Path = DEFAULT_OUTPUT_DIR) -> Path:
    concepts = load_concepts()
    if not concepts:
        raise ValueError("No concept objects found")

    prepare_output(output_dir)
    shutil.copy2(SITE_DIR / "styles.css", output_dir / "styles.css")
    shutil.copy2(SITE_DIR / "_headers", output_dir / "_headers")

    (output_dir / "index.html").write_text(render_index(concepts), encoding="utf-8")
    write_route(output_dir, "understand", render_understand_index(concepts))

    for concept in concepts:
        write_route(output_dir, f"understand/{concept['id']}", render_concept(concept))

    for slug in STATIC_PAGES:
        write_route(output_dir, slug, render_static_page(slug))

    return output_dir


if __name__ == "__main__":
    destination = build()
    print(f"Built The Neurodiverse Oracle Site Shell v0.1 at {destination}")
