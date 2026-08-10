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


def page_shell(title: str, body: str, stylesheet: str) -> str:
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="color-scheme" content="light">
  <title>{esc(title)} · ND Oracle</title>
  <link rel="stylesheet" href="{esc(stylesheet)}">
</head>
<body>
{body}
</body>
</html>
"""


def render_index(concepts: list[dict]) -> str:
    cards = []
    for concept in concepts:
        cards.append(
            f"""<article class="card">
  <div class="status">{esc(concept['status'])}</div>
  <h2><a href="concepts/{esc(concept['id'])}.html">{esc(concept['name'])}</a></h2>
  <p>{esc(concept['summary'])}</p>
</article>"""
        )

    body = f"""<header class="site-header">
  <div class="site-shell reading-column">
    <div class="eyebrow">A provenance-first knowledge commons</div>
    <h1>ND Oracle</h1>
    <p class="lede">A reading-first window onto neurodiversity knowledge, with evidence, uncertainty and competing perspectives kept visible.</p>
  </div>
</header>
<main class="site-shell">
  <div class="notice reading-column"><strong>Early seed material.</strong> This site is for orientation and research traceability. It is not diagnosis or medical advice.</div>
  <section aria-labelledby="concepts-heading">
    <h2 id="concepts-heading">Concepts</h2>
    <div class="grid">{''.join(cards)}</div>
  </section>
</main>
<footer class="site-footer"><div class="site-shell">Every serious claim should retain a route back to its evidence and uncertainty.</div></footer>"""
    return page_shell("Home", body, "styles.css")


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
            f'<li><a href="{esc(relation["target_id"])}.html">{esc(relation["target_id"])}</a> — {esc(relation["note"])}</li>'
        )

    body = f"""<header class="site-header">
  <div class="site-shell reading-column">
    <a href="../index.html">← All concepts</a>
    <div class="eyebrow">{esc(concept['type'])} · {esc(concept['status'])}</div>
    <h1>{esc(concept['name'])}</h1>
    <p class="lede">{esc(concept['summary'])}</p>
  </div>
</header>
<main class="site-shell reading-column">
  <div class="notice"><strong>Early seed material.</strong> This page is not diagnosis or medical advice. Claims remain linked to their recorded evidence and uncertainty.</div>

  <section><h2>Scope</h2><h3>Includes</h3>{list_items(concept['scope']['includes'])}<h3>Excludes</h3>{list_items(concept['scope']['excludes'])}</section>
  <section><h2>Claims</h2>{''.join(claims)}</section>
  <section><h2>Uncertainties</h2>{''.join(uncertainties)}</section>
  <section><h2>Perspectives</h2>{''.join(perspectives)}</section>
  <section><h2>Related concepts</h2><ul>{''.join(relations)}</ul></section>
  <section><h2>Sources</h2>{''.join(sources)}</section>
  <section><h2>Provenance</h2><p>{esc(concept['provenance']['method'])}</p><div class="meta">Created {esc(concept['provenance']['created'])} · review state {esc(concept['provenance']['review_state'])}</div></section>
</main>
<footer class="site-footer"><div class="site-shell reading-column">Stable object ID: {esc(concept['id'])} · schema {esc(concept['schema_version'])}</div></footer>"""

    return page_shell(concept["name"], body, "../styles.css")


def prepare_output(output_dir: Path) -> None:
    marker = output_dir / ".nd-oracle-generated"
    if output_dir.is_symlink():
        raise ValueError(f"Refusing to replace symlink output directory: {output_dir}")
    if output_dir.exists():
        if not marker.is_file() or marker.read_text(encoding="utf-8") != OUTPUT_MARKER:
            raise ValueError(f"Refusing to replace unmarked output directory: {output_dir}")
        shutil.rmtree(output_dir)
    (output_dir / "concepts").mkdir(parents=True)
    marker.write_text(OUTPUT_MARKER, encoding="utf-8")


def build(output_dir: Path = DEFAULT_OUTPUT_DIR) -> Path:
    concepts = load_concepts()
    if not concepts:
        raise ValueError("No concept objects found")

    prepare_output(output_dir)
    shutil.copy2(SITE_DIR / "styles.css", output_dir / "styles.css")
    shutil.copy2(SITE_DIR / "_headers", output_dir / "_headers")

    (output_dir / "index.html").write_text(render_index(concepts), encoding="utf-8")
    for concept in concepts:
        (output_dir / "concepts" / f"{concept['id']}.html").write_text(render_concept(concept), encoding="utf-8")

    return output_dir


if __name__ == "__main__":
    destination = build()
    print(f"Built ND Oracle website candidate at {destination}")
