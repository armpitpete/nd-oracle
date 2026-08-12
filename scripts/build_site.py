from __future__ import annotations

import html
import json
import shutil
from datetime import date
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
OBJECTS_DIR = ROOT / "objects" / "concepts"
SITE_DIR = ROOT / "site"
DEFAULT_OUTPUT_DIR = ROOT / "dist"
OUTPUT_MARKER = "nd-oracle-site-v0.2\n"
PUBLIC_ORIGIN = "https://ndoracle.org"

PRIMARY_NAV = [
    ("understand", "Understand"),
    ("how-it-works", "How it works"),
    ("about", "About"),
]

# The reading layer is deliberately separate from the authoritative evidence
# objects. Evidence summaries can stay precise while the first public sentence
# is written for someone who simply needs to understand the topic.
SIMPLE_EXPLANATIONS = {
    "neurodiversity": (
        "People's brains and nervous systems vary. Neurodiversity is a word for that variation, "
        "and it is also used when people talk about rights, disability, support and how neurological differences should be understood."
    ),
    "autism": (
        "Autistic people can experience communication, social situations, routines, interests and sensory input differently. "
        "Autism looks different from person to person, and support needs can vary."
    ),
    "adhd": (
        "ADHD can affect attention, activity, impulsivity and managing everyday tasks. "
        "It can look different between people and situations, and diagnosis needs more than a checklist or a single test."
    ),
    "executive-function": (
        "Executive functions help us hold things in mind, switch attention, pause responses and organise actions towards a goal. "
        "Difficulties with them can make starting, planning or finishing tasks hard, but they are not a diagnosis by themselves."
    ),
    "sensory-processing": (
        "People differ in how strongly they notice and respond to sound, light, touch, movement and other sensory input. "
        "These differences can affect comfort and everyday life, and they are not unique to one diagnosis."
    ),
    "dyslexia": (
        "Dyslexia mainly affects learning and using word reading and spelling. "
        "It can continue into adulthood, and it does not mean that someone has low intelligence."
    ),
    "developmental-coordination-disorder": (
        "Developmental co-ordination disorder (DCD) affects how easily someone learns and carries out coordinated movements. "
        "Everyday activities can take more effort, and the difficulties can continue into adulthood."
    ),
    "tourette-syndrome": (
        "Tourette syndrome involves motor and vocal tics that change over time. "
        "Swearing is not what defines Tourette syndrome, and support or treatment should depend on what is actually difficult for the person."
    ),
    "learning-disability": (
        "In the UK, a learning disability means lifelong difficulty learning or understanding new information together with difficulty managing everyday life independently. "
        "It is not the same thing as a specific learning difficulty such as dyslexia."
    ),
    "developmental-language-disorder": (
        "Developmental language disorder (DLD) is a persistent difficulty understanding and/or using language that affects everyday life. "
        "Bilingualism does not cause DLD, and DLD can occur alongside other developmental conditions."
    ),
}

COMMON_QUESTIONS = [
    ("What does neurodiversity mean?", "neurodiversity"),
    ("What is autism?", "autism"),
    ("What is ADHD?", "adhd"),
    ("Why can starting or organising tasks feel hard?", "executive-function"),
    ("Why can sound, light or touch feel intense?", "sensory-processing"),
    ("Why can reading or spelling stay difficult?", "dyslexia"),
    ("Why can coordination and everyday movement be hard?", "developmental-coordination-disorder"),
    ("What are tics and Tourette syndrome?", "tourette-syndrome"),
    ("What does learning disability mean in the UK?", "learning-disability"),
    ("Why can understanding or using language be difficult?", "developmental-language-disorder"),
]

STATIC_PAGES = {
    "how-it-works": {
        "title": "How this site works",
        "intro": "Start with a short explanation. Open the evidence, uncertainty and provenance only when you want the deeper route.",
        "body": (
            "<section><h2>Useful first</h2>"
            "<p>The public pages are written for reading, not for navigating an internal database. "
            "Each topic starts with a deliberately simple explanation. A more precise evidence summary is still available when you want it.</p></section>"
            "<section id=\"confidence\"><h2>What the confidence labels mean</h2>"
            "<p>A confidence label applies only to the exact statement beside it. It is not a score for a whole topic, person or source, and high confidence does not mean certainty.</p>"
            "<dl class=\"confidence-key\">"
            "<dt>High</dt><dd>The bounded statement has strong, consistent support from the evidence used for it, with no known disagreement large enough to change the statement substantially.</dd>"
            "<dt>Moderate</dt><dd>The statement is supported, but important limits, narrower evidence, transfer problems or remaining uncertainty mean it should be read with more caution.</dd>"
            "<dt>Low</dt><dd>The statement has some support but the evidence is limited, indirect or fragile. Treat it as provisional.</dd>"
            "<dt>Contested</dt><dd>Credible evidence or perspectives materially disagree. The label preserves that disagreement rather than forcing a false consensus.</dd>"
            "<dt>Not applicable</dt><dd>An epistemic confidence score is not the right description for that statement; this must not be used merely to avoid assessing evidence.</dd>"
            "</dl></section>"
            "<section><h2>Uncertainty stays visible</h2>"
            "<p>If an important question is unresolved, the site keeps it unresolved. The aim is to save the next person from having to rediscover the same gap.</p></section>"
            "<section><h2>Evidence is inspectable</h2>"
            "<p>Evidence links sit behind the statements they support. Source details and provenance remain available lower on each topic page without dominating the first read.</p></section>"
            "<section><h2>Review dates are visible</h2>"
            "<p>Each topic shows when its current evidence record was last reviewed. A review date is not a promise that nothing newer exists; it tells you how fresh this site's review is.</p></section>"
            "<section><h2>This is not a diagnosis service</h2>"
            "<p>The site is for understanding and research traceability. It does not diagnose individuals or replace appropriate clinical, legal, educational or safeguarding judgement.</p></section>"
        ),
        "indexable": True,
    },
    "about": {
        "title": "About",
        "intro": "The Neurodiverse Oracle is a provenance-first knowledge commons built to reduce repeated research and unnecessary decoding.",
        "body": (
            "<section><h2>What it is for</h2>"
            "<p>The aim is to make useful knowledge easier to reach while keeping the route back to evidence, disagreement and uncertainty intact.</p></section>"
            "<section><h2>What exists now</h2>"
            "<p>The current public release covers the evidence-linked topics listed under Understand. "
            "The site widens when new material is useful and sufficiently traceable, rather than displaying empty sections in advance.</p></section>"
            "<section><h2>What it is not</h2>"
            "<p>It is not a diagnosis engine, a treatment marketplace, an AI authority or a replacement for professional judgement.</p></section>"
        ),
        "indexable": True,
    },
    "accessibility": {
        "title": "Accessibility",
        "intro": "The site is designed to reduce cognitive and sensory burden rather than add to it.",
        "body": (
            "<section><h2>Current approach</h2>"
            "<p>The site uses semantic HTML, visible keyboard focus, restrained colours, a reading-width content column and no required JavaScript.</p>"
            "<p>Evidence and provenance use native disclosure controls so readers can choose depth without losing keyboard access.</p></section>"
            "<section><h2>Accessibility problems are defects</h2>"
            "<p>Future interactive features must preserve keyboard access, reduced-motion preferences, readable language and a usable no-script baseline wherever practical.</p>"
            "<p>If something here is difficult to use, <a href=\"/feedback/\">report the accessibility problem</a>.</p></section>"
        ),
        "indexable": True,
    },
    "privacy": {
        "title": "Privacy",
        "intro": "The current public site is designed to collect no personal data.",
        "body": (
            "<section><h2>Current release</h2>"
            "<p>There are no accounts, forms, analytics scripts, advertising trackers or personalised features in the generated site.</p>"
            "<p>The feedback page links to the public GitHub issue tracker; following that link leaves this site and uses GitHub's service.</p></section>"
            "<section><h2>Future features</h2>"
            "<p>Anything that stores queries, profiles, health information or community submissions requires a separate privacy and threat-model review before release.</p></section>"
        ),
        "indexable": True,
    },
    "feedback": {
        "title": "Feedback",
        "intro": "Found something inaccessible, unclear, outdated or broken? You can report it without adding tracking or a form to this site.",
        "body": (
            "<section><h2>Report a problem</h2>"
            "<p>Use the public ND Oracle issue tracker for accessibility problems, factual concerns, confusing wording, broken links or other defects. "
            "Please do not include private health information, contact details or anything else you would not want published.</p>"
            "<p><a href=\"https://github.com/armpitpete/nd-oracle/issues/new\" rel=\"noopener noreferrer\">Open the public issue tracker</a></p></section>"
            "<section><h2>What helps</h2>"
            "<ul><li>The page address.</li><li>What you expected to happen.</li><li>What actually happened or what was difficult to understand.</li><li>For an evidence concern, the exact statement you think needs checking.</li></ul></section>"
            "<section class=\"notice\"><h2>Current limitation</h2>"
            "<p>This release does not yet offer a private feedback channel. If the public GitHub route is itself inaccessible to you, that is a known limitation rather than a reason to treat the problem as resolved.</p></section>"
        ),
        "indexable": True,
    },
    # These routes existed in Site Shell v0.1. Keep them as quiet compatibility
    # pages so old links do not become dead ends, but do not advertise them as
    # active parts of the current product or include them in the sitemap.
    "tools": {
        "title": "Tools",
        "intro": "Tools are not part of the current public release.",
        "body": "<p>Rather than publish an empty catalogue, this release keeps the useful knowledge pages front and centre. <a href=\"/understand/\">Browse current topics</a>.</p>",
        "indexable": False,
    },
    "games": {
        "title": "Games",
        "intro": "Games are not part of the current public release.",
        "body": "<p>This route is retained so older links still lead somewhere useful. <a href=\"/understand/\">Browse current topics</a>.</p>",
        "indexable": False,
    },
    "resources": {
        "title": "Resources",
        "intro": "A resource catalogue is not part of the current public release.",
        "body": "<p>The site will not present an empty directory as a finished feature. <a href=\"/understand/\">Browse current topics</a>.</p>",
        "indexable": False,
    },
    "community": {
        "title": "Community",
        "intro": "Community accounts and submissions are not part of the current public release.",
        "body": "<p>No accounts, profiles, comments or public submissions are active. <a href=\"/understand/\">Browse current topics</a>.</p>",
        "indexable": False,
    },
    "oracle": {
        "title": "Oracle",
        "intro": "The deeper provenance system is the foundation of these pages, not a chatbot presented as an authority.",
        "body": "<p>The current public interface exposes validated knowledge through the topic pages. Generated answers are not the source of truth. <a href=\"/how-it-works/\">See how the evidence route works</a>.</p>",
        "indexable": False,
    },
}

INDEXED_STATIC_PAGES = tuple(
    slug for slug, page in STATIC_PAGES.items() if page.get("indexable", True)
)


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def safe_http_url(value: object) -> str | None:
    if not isinstance(value, str):
        return None
    parsed = urlsplit(value)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        return None
    return value


def human_date(value: str | None) -> str:
    if value is None:
        return "Not yet reviewed"
    parsed = date.fromisoformat(value)
    return parsed.strftime("%d %B %Y").lstrip("0")


def load_concepts() -> list[dict]:
    concepts = []
    for path in sorted(OBJECTS_DIR.glob("*.json")):
        with path.open("r", encoding="utf-8") as handle:
            concepts.append(json.load(handle))
    return sorted(concepts, key=lambda item: item["name"].casefold())


def validate_reading_layer(concepts: list[dict]) -> None:
    concept_ids = {concept["id"] for concept in concepts}
    explanation_ids = set(SIMPLE_EXPLANATIONS)
    question_ids = {concept_id for _, concept_id in COMMON_QUESTIONS}
    if explanation_ids != concept_ids:
        raise ValueError(
            "Public-reading explanation set must exactly match authoritative concepts: "
            f"missing={sorted(concept_ids - explanation_ids)}; unexpected={sorted(explanation_ids - concept_ids)}"
        )
    if question_ids != concept_ids or len(COMMON_QUESTIONS) != len(concept_ids):
        raise ValueError(
            "Homepage question set must provide exactly one route for every authoritative concept: "
            f"missing={sorted(concept_ids - question_ids)}; unexpected={sorted(question_ids - concept_ids)}"
        )


def reader_intro(concept: dict) -> str:
    return SIMPLE_EXPLANATIONS[concept["id"]]


def list_items(values: list[str]) -> str:
    return "<ul>" + "".join(f"<li>{esc(value)}</li>" for value in values) + "</ul>"


def nav(current: str | None = None) -> str:
    links = []
    for slug, label in PRIMARY_NAV:
        current_attr = ' aria-current="page"' if slug == current else ""
        links.append(f'<a href="/{slug}/"{current_attr}>{esc(label)}</a>')
    return '<nav class="primary-nav" aria-label="Primary">' + "".join(links) + "</nav>"


def page_shell(
    title: str,
    intro: str,
    body: str,
    *,
    current: str | None = None,
    path: str | None = None,
    indexable: bool = True,
) -> str:
    canonical = ""
    if path is not None:
        canonical_url = PUBLIC_ORIGIN + path
        canonical = f'  <link rel="canonical" href="{esc(canonical_url)}">\n'
    robots = "" if indexable else '  <meta name="robots" content="noindex, follow">\n'
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="color-scheme" content="light">
  <meta name="theme-color" content="#f5f4ef">
  <meta name="description" content="{esc(intro)}">
{robots}{canonical}  <title>{esc(title)} · The Neurodiverse Oracle</title>
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
    <span>Useful first. Evidence when you want it.</span>
    <nav aria-label="Footer">
      <a href="/how-it-works/">How it works</a>
      <a href="/accessibility/">Accessibility</a>
      <a href="/feedback/">Feedback</a>
      <a href="/privacy/">Privacy</a>
    </nav>
  </div>
</footer>
</body>
</html>
"""


def topic_link(concept: dict) -> str:
    return f"""<article class="topic-row">
  <h2><a href="/understand/{esc(concept['id'])}/">{esc(concept['name'])}</a></h2>
  <p>{esc(reader_intro(concept))}</p>
</article>"""


def render_index(concepts: list[dict]) -> str:
    concept_map = {concept["id"]: concept for concept in concepts}
    question_links = []
    for question, concept_id in COMMON_QUESTIONS:
        if concept_id not in concept_map:
            raise ValueError(f"Common-question target is missing: {concept_id}")
        question_links.append(
            f'<li><a href="/understand/{esc(concept_id)}/">{esc(question)}</a></li>'
        )

    topics = "".join(topic_link(concept) for concept in concepts)
    body = f"""
<section class="start-section" aria-labelledby="start-heading">
  <h2 id="start-heading">Start with a question</h2>
  <p class="section-intro">Choose the question closest to what you are trying to understand. Every current topic has a route from here.</p>
  <ul class="question-list">{''.join(question_links)}</ul>
</section>
<section aria-labelledby="topics-heading">
  <div class="section-heading-row">
    <div><h2 id="topics-heading">Browse current topics</h2><p class="section-intro">{len(concepts)} evidence-linked topics are available now. No empty feature catalogue is presented as finished content.</p></div>
    <a class="quiet-link" href="/understand/">See all topics</a>
  </div>
  <div class="topic-list">{topics}</div>
</section>
<section class="reading-guide" aria-labelledby="guide-heading">
  <h2 id="guide-heading">Choose how deep to go</h2>
  <div class="guide-grid">
    <div><strong>Read the simple version</strong><p>Each topic starts with a short explanation written for a first read.</p></div>
    <div><strong>Check the reasoning</strong><p>Open the evidence and uncertainty behind individual statements when you need it.</p></div>
    <div><strong>Follow the source</strong><p>Source citations, review dates and provenance remain available without dominating the page.</p></div>
  </div>
  <p><a href="/how-it-works/">How the evidence, confidence and uncertainty system works →</a></p>
</section>
"""
    return page_shell(
        "Understand neurodivergence without doing all the digging yourself",
        "Start with an ordinary question, get a clear explanation, and inspect the evidence or uncertainty only when you want to go deeper.",
        body,
        path="/",
    )


def render_understand_index(concepts: list[dict]) -> str:
    topics = "".join(topic_link(concept) for concept in concepts)
    body = f"""
<section class="notice">
  <strong>Orientation, not diagnosis.</strong> These pages explain concepts and preserve their evidence routes. They do not diagnose individuals or replace appropriate professional judgement.
</section>
<section aria-labelledby="concepts-heading">
  <h2 id="concepts-heading">Current topics</h2>
  <p class="section-intro">There are {len(concepts)} reviewed topic pages. Each starts simply and keeps the deeper evidence route available when you want it.</p>
  <div class="topic-list">{topics}</div>
</section>
"""
    return page_shell(
        "Understand",
        "Plain-language topic pages with evidence, uncertainty and different perspectives available without forcing you through them first.",
        body,
        current="understand",
        path="/understand/",
    )


def render_concept(concept: dict, concept_map: dict[str, dict]) -> str:
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
            f'<a href="#source-{esc(source_id)}">{esc(source_map[source_id]["citation"])}</a>'
            for source_id in claim["source_ids"]
        )
        uncertainty_links = ", ".join(
            f'<a href="#uncertainty-{esc(uncertainty_id)}">{esc(uncertainty_map[uncertainty_id]["question"])}</a>'
            for uncertainty_id in claim["uncertainty_ids"]
        )
        claims.append(
            f"""<article class="claim" id="claim-{esc(claim['id'])}">
  <div class="claim-head"><h3>{esc(claim['text'])}</h3><span class="confidence">{esc(claim['confidence'])} confidence</span></div>
  <details class="evidence-detail">
    <summary>Evidence and uncertainty behind this statement</summary>
    <div class="route"><div><span class="route-label">Evidence:</span> {source_links}</div><div><span class="route-label">Uncertainty:</span> {uncertainty_links}</div></div>
  </details>
</article>"""
        )

    uncertainties = []
    for item in concept["uncertainties"]:
        uncertainties.append(
            f"""<article class="uncertainty" id="uncertainty-{esc(item['id'])}">
  <h3>{esc(item['question'])}</h3>
  <p>{esc(item['why_it_matters'])}</p>
  <details><summary>What could reduce this uncertainty?</summary>{list_items(item['what_would_reduce_it'])}</details>
  <div class="status">Status: {esc(item['status'])}</div>
</article>"""
        )

    perspectives = []
    for item in concept["perspectives"]:
        source_links = ", ".join(
            f'<a href="#source-{esc(source_id)}">source</a>' for source_id in item["source_ids"]
        )
        perspectives.append(
            f"""<article class="perspective">
  <h3>{esc(item['held_by'])}</h3>
  <p>{esc(item['summary'])}</p>
  <div class="meta">Evidence route: {source_links}</div>
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
        target_id = relation["target_id"]
        if target_id not in concept_map:
            raise ValueError(f"{concept['id']}: missing related concept {target_id}")
        relations.append(
            f'<li><a href="/understand/{esc(target_id)}/">{esc(concept_map[target_id]["name"])}</a> — {esc(relation["note"])}</li>'
        )

    reviewed = human_date(concept["provenance"].get("last_reviewed"))
    body = f"""
<p class="back-link"><a href="/understand/">← All topics</a></p>
<p class="review-meta">Last reviewed: <strong>{esc(reviewed)}</strong></p>
<details class="technical-summary"><summary>More precise description</summary><p>{esc(concept['summary'])}</p></details>
<section class="at-a-glance" aria-labelledby="glance-heading">
  <h2 id="glance-heading">At a glance</h2>
  <div class="scope-grid">
    <div><h3>This page covers</h3>{list_items(concept['scope']['includes'])}</div>
    <div><h3>It does not mean</h3>{list_items(concept['scope']['excludes'])}</div>
  </div>
</section>
<section aria-labelledby="known-heading"><h2 id="known-heading">What we can say</h2><p class="section-intro">These are bounded statements from the current evidence record. <a href="/how-it-works/#confidence">See what the confidence labels mean</a>. Open a statement only if you want its evidence route.</p>{''.join(claims)}</section>
<section aria-labelledby="uncertainty-heading"><h2 id="uncertainty-heading">What remains uncertain</h2>{''.join(uncertainties)}</section>
<section aria-labelledby="perspectives-heading"><h2 id="perspectives-heading">Different perspectives</h2>{''.join(perspectives)}</section>
<section aria-labelledby="related-heading"><h2 id="related-heading">Related topics</h2><ul>{''.join(relations)}</ul></section>
<section aria-labelledby="sources-heading"><h2 id="sources-heading">Sources</h2>{''.join(sources)}</section>
<details class="provenance"><summary>Page provenance and review state</summary><p>{esc(concept['provenance']['method'])}</p><div class="meta">Created {esc(concept['provenance']['created'])} · last reviewed {esc(reviewed)} · review state {esc(concept['provenance']['review_state'])}</div></details>
"""
    return page_shell(
        concept["name"],
        reader_intro(concept),
        body,
        current="understand",
        path=f"/understand/{concept['id']}/",
    )


def render_static_page(slug: str) -> str:
    page = STATIC_PAGES[slug]
    return page_shell(
        page["title"],
        page["intro"],
        page["body"],
        current=slug if slug in dict(PRIMARY_NAV) else None,
        path=f"/{slug}/",
        indexable=page.get("indexable", True),
    )


def render_not_found() -> str:
    body = """
<section>
  <h2>Try one of these instead</h2>
  <ul class="question-list">
    <li><a href="/">Go to the homepage</a></li>
    <li><a href="/understand/">Browse current topics</a></li>
    <li><a href="/how-it-works/">See how the site works</a></li>
    <li><a href="/feedback/">Report a broken or confusing page</a></li>
  </ul>
</section>
"""
    return page_shell(
        "Page not found",
        "That address does not match a current page, but you can get back to the useful parts of the site here.",
        body,
        indexable=False,
    )


def sitemap_paths(concepts: list[dict]) -> list[str]:
    paths = ["/", "/understand/"]
    paths.extend(f"/understand/{concept['id']}/" for concept in concepts)
    paths.extend(f"/{slug}/" for slug in INDEXED_STATIC_PAGES)
    return paths


def render_sitemap(concepts: list[dict]) -> str:
    urls = "".join(
        f"  <url><loc>{html.escape(PUBLIC_ORIGIN + path)}</loc></url>\n"
        for path in sitemap_paths(concepts)
    )
    return f"<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">\n{urls}</urlset>\n"


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
    validate_reading_layer(concepts)
    concept_map = {concept["id"]: concept for concept in concepts}

    prepare_output(output_dir)
    shutil.copy2(SITE_DIR / "styles.css", output_dir / "styles.css")
    shutil.copy2(SITE_DIR / "_headers", output_dir / "_headers")

    (output_dir / "index.html").write_text(render_index(concepts), encoding="utf-8")
    write_route(output_dir, "understand", render_understand_index(concepts))

    for concept in concepts:
        write_route(output_dir, f"understand/{concept['id']}", render_concept(concept, concept_map))

    for slug in STATIC_PAGES:
        write_route(output_dir, slug, render_static_page(slug))

    (output_dir / "404.html").write_text(render_not_found(), encoding="utf-8")
    (output_dir / "sitemap.xml").write_text(render_sitemap(concepts), encoding="utf-8")
    (output_dir / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\nSitemap: {PUBLIC_ORIGIN}/sitemap.xml\n",
        encoding="utf-8",
    )

    return output_dir


if __name__ == "__main__":
    destination = build()
    print(f"Built The Neurodiverse Oracle public site v0.5 at {destination}")
