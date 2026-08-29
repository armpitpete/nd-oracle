from __future__ import annotations

import html
import json
import sys
from collections import defaultdict
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts import build_site_v09 as _v09
from scripts.build_site_v09 import *
from scripts import discovery

EVIDENCE_DIR = ROOT / "objects" / "evidence"
V10_ROUTE_COUNT = 142

QUESTION_GROUPS = [
    ("Daily life & technology", [
        "task-starting-and-organisation", "make-device-easier-to-use",
        "meal-planning-and-everyday-food-tasks",
    ]),
    ("Sensory & environment", [
        "make-noisy-bright-place-easier", "sensory-overload-what-can-i-change",
    ]),
    ("Communication", [
        "aac-and-nonspeaking-communication", "phone-calls-are-difficult",
        "processing-time-in-conversations-meetings",
    ]),
    ("Work", [
        "workplace-support-great-britain", "reasonable-adjustments-at-work-great-britain",
        "disabled-person-looking-for-work-uk", "disclosing-disability-neurodivergence-at-work",
        "job-interview-adjustments-great-britain",
    ]),
    ("Education & study", [
        "disabled-student-support-england", "organising-study-and-assignments",
        "send-support-school-college-england",
    ]),
    ("Assessment & diagnosis", [
        "adult-adhd-assessment-england", "adult-autism-assessment-england",
    ]),
    ("Health & wellbeing", [
        "autism-anxiety-tools", "masking-exhaustion-and-autistic-burnout",
        "sleep-and-winding-down-routines", "healthcare-communication-adjustments-england",
    ]),
    ("Relationships & family", [
        "autistic-parent-support-uk", "communication-needs-in-relationships",
        "neurodivergent-parent-overwhelmed-by-admin",
    ]),
    ("Money & administration", ["disability-benefits-where-start-uk"]),
    ("Mobility & travel", [
        "adhd-driving-dvla-great-britain", "disabled-travel-support-scotland",
        "disabled-travel-support-wales", "disabled-travel-support-northern-ireland",
    ]),
    ("Information & support", [
        "autism-information-and-support", "dyslexia-information-and-support-uk",
        "tourette-information-and-support-uk", "learning-disability-information-and-support-uk",
        "dld-information-and-support", "adult-dyspraxia-information-uk",
        "dyscalculia-information-and-support-uk",
    ]),
    ("Games & downtime", ["low-time-pressure-games"]),
]

# The accepted v0.9 builder is frozen for compatibility. Configure its explicit
# editorial navigation for the expanded v1.0 corpus before invoking it.
_v09.QUESTION_GROUPS = QUESTION_GROUPS
_v09._v08.QUESTION_GROUPS = QUESTION_GROUPS
_v09.V09_ROUTE_COUNT = 141


def load_evidence() -> list[dict]:
    if not EVIDENCE_DIR.is_dir():
        return []
    items = []
    for path in sorted(EVIDENCE_DIR.glob("*.json")):
        items.append(json.loads(path.read_text(encoding="utf-8")))
    return sorted(items, key=lambda item: item["title"].casefold())


def validate_question_navigation(questions: list[dict]) -> None:
    question_ids = {item["id"] for item in questions}
    grouped = [item for _group, ids in QUESTION_GROUPS for item in ids]
    if len(grouped) != len(set(grouped)):
        raise ValueError("Question navigation groups contain duplicates")
    if set(grouped) != question_ids:
        raise ValueError(
            "v1.0 Question groups must exactly cover current Questions: "
            f"missing={sorted(question_ids - set(grouped))}; unexpected={sorted(set(grouped) - question_ids)}"
        )
    _v09.validate_question_navigation(questions)


def resource_scope(resource: dict) -> tuple[str, str]:
    audience = str(resource.get("audience_or_context", "")).casefold()
    whole = " ".join([
        str(resource.get("description", "")), audience,
        *[str(item) for item in resource.get("limitations", [])],
    ]).casefold()
    if "great britain" in audience or "england, scotland and wales" in audience:
        return "Great Britain", "The reviewed scope identifies Great Britain (England, Scotland and Wales); Northern Ireland may use a different system."
    if ("england or wales" in audience or "england and wales" in audience) and "scotland" not in audience:
        return "England and Wales", "The reviewed scope specifically identifies England and Wales."
    if "northern ireland" in audience and all(term not in audience for term in ("england", "scotland", "wales")):
        return "Northern Ireland", "The reviewed scope specifically identifies Northern Ireland."
    if "scotland" in audience and all(term not in audience for term in ("england", "wales", "northern ireland")):
        return "Scotland", "The reviewed scope specifically identifies Scotland."
    if "wales" in audience and all(term not in audience for term in ("england", "scotland", "northern ireland")):
        return "Wales", "The reviewed scope specifically identifies Wales."
    if "england" in audience and all(term not in audience for term in ("scotland", "wales", "northern ireland")):
        return "England", "The reviewed scope specifically identifies England."
    if "united kingdom" in audience or " uk " in f" {audience} " or "uk-wide" in whole:
        return "United Kingdom", "The reviewed listing describes a UK-wide or United Kingdom scope."
    return "International / not jurisdiction-specific", "No narrower UK jurisdiction is asserted by the reviewed scope; check the resource itself for local availability and eligibility."


_v09.resource_scope = resource_scope


def _evidence_contribution(evidence: dict, claim_ref: str) -> dict | None:
    for item in evidence.get("contributions", []):
        if item.get("claim_ref") == claim_ref:
            return item
    return None


def render_governed_resource_claims(resource: dict, evidence_map: dict[str, dict]) -> str:
    claims = resource.get("claims", [])
    if not claims:
        return ""
    rows = []
    for claim in claims:
        claim_ref = f"{resource['id']}#{claim['id']}"
        evidence_rows = []
        for evidence_id in claim.get("evidence_ids", []):
            evidence = evidence_map.get(evidence_id)
            if evidence is None:
                raise ValueError(f"{claim_ref}: missing evidence {evidence_id}")
            contribution = _evidence_contribution(evidence, claim_ref)
            if contribution is None:
                raise ValueError(f"{evidence_id}: missing contribution for {claim_ref}")
            locator = evidence.get("locator", {})
            raw_url = locator.get("value") if locator.get("type") == "url" else None
            citation = esc(evidence["citation"])
            if raw_url and safe_http_url(raw_url):
                citation = f'<a href="{esc(raw_url)}">{citation}</a>'
            limits = list_items([item["text"] for item in contribution.get("limitations", [])])
            evidence_rows.append(
                f'<article class="evidence-card"><h4>{esc(evidence["title"])}</h4>'
                f'<p>{citation}</p><p><strong>Finding used here:</strong> {esc(contribution["finding"])}</p>'
                f'<p class="meta">Context: {esc(contribution["population_or_context"])} · Method: {esc(contribution["methodology"])}</p>'
                f'<div><strong>Evidence limitations</strong>{limits}</div></article>'
            )
        uncertainty_rows = "".join(
            f'<li id="uncertainty-{esc(item["id"])}"><strong>{esc(item["text"])}</strong><br>'
            f'<span class="meta">Why it matters: {esc(item["why_it_matters"])}</span></li>'
            for item in claim.get("uncertainties", [])
        )
        confidence = claim["confidence"].replace("_", " ").title()
        rows.append(
            f'<article class="claim-card" id="claim-{esc(claim["id"])}">'
            f'<h3>{esc(claim["text"])}</h3>'
            f'<p class="meta">Confidence: <a href="/how-it-works/#confidence">{esc(confidence)}</a></p>'
            f'<h4>Evidence route</h4>{"".join(evidence_rows)}'
            f'<h4>Uncertainty and limits</h4><ul>{uncertainty_rows}</ul></article>'
        )
    return (
        '<section aria-labelledby="governed-resource-claims-heading">'
        '<h2 id="governed-resource-claims-heading">Governed claims and evidence</h2>'
        '<section class="notice"><strong>A supported claim is not a recommendation or an individual decision.</strong> '
        'Read the exact wording, evidence context and open uncertainty together.</section>'
        + "".join(rows) + "</section>"
    )


def render_resource(resource: dict, concept_map: dict[str, dict], questions: list[dict], evidence_map: dict[str, dict] | None = None) -> str:
    page = _v09.render_resource(resource, concept_map, questions)
    if evidence_map is None:
        evidence_map = {item["id"]: item for item in load_evidence()}
    claims = render_governed_resource_claims(resource, evidence_map)
    if claims:
        marker = '<section aria-labelledby="limits-heading">'
        if marker not in page:
            raise ValueError(f"{resource['id']}: cannot locate limits section for governed claims")
        page = page.replace(marker, claims + marker, 1)
    return page


def render_places_index(resources: list[dict]) -> str:
    grouped: dict[str, list[dict]] = defaultdict(list)
    explanations: dict[str, str] = {}
    for resource in resources:
        label, explanation = resource_scope(resource)
        grouped[label].append(resource)
        explanations[label] = explanation
    order = [
        "United Kingdom", "Great Britain", "England and Wales", "England", "Scotland",
        "Wales", "Northern Ireland", "International / not jurisdiction-specific",
    ]
    sections = []
    for label in order:
        items = sorted(grouped.get(label, []), key=lambda item: item["name"].casefold())
        if not items:
            continue
        links = "".join(f'<li><a href="/resources/{esc(item["id"])}/">{esc(item["name"])}</a></li>' for item in items)
        sections.append(f'<section><h2>{esc(label)}</h2><p class="meta">{esc(explanations[label])}</p><ul>{links}</ul></section>')
    body = (
        '<section class="notice"><strong>Navigation scope, not eligibility.</strong> These groups come from reviewed audience/scope text. '
        'UK-wide, Great Britain, England and Wales, England, Scotland, Wales and Northern Ireland are kept distinct where the governed material supports that distinction.</section>'
        + "".join(sections)
    )
    return page_shell(
        "Browse by geographic scope",
        "Distinguish national and jurisdiction-specific support instead of treating every UK route as interchangeable.",
        body, current="resources", path="/places/",
    )


FIND_JS = r'''(() => {
  "use strict";
  const input = document.getElementById("find-input");
  const button = document.getElementById("find-button");
  const output = document.getElementById("find-results");
  const raw = document.getElementById("search-index").content.textContent;
  const index = JSON.parse(raw);
  const stop = new Set(["a","an","and","are","can","do","for","i","in","is","it","me","my","of","on","or","the","to","what","with","you","your"]);
  const refusals = ["diagnose me","am i autistic","do i have autism","do i have adhd","what medication dose","what dose should i take","stop my medication","which medication should i take","tell me if i am autistic","tell me if i have adhd"];
  const norm = s => (s || "").toLowerCase().match(/[a-z0-9]+/g)?.join(" ") || "";
  const tokens = s => norm(s).split(" ").filter(t => t.length > 1 && !stop.has(t));
  function score(query, record) {
    const qn = norm(query); const qt = new Set(tokens(query));
    const tn = norm(record.title); const bn = norm(record.body); let s = 0;
    if (qn === tn) s += 120; else if (tn.includes(qn)) s += 55;
    if (bn.includes(qn)) s += 20;
    const tt = new Set(tokens(record.title)); const bt = new Set(tokens(record.body));
    qt.forEach(t => { if (tt.has(t)) s += 12; if (bt.has(t)) s += 3; });
    (record.intent || []).forEach(p => { const pn = norm(p); const pt = new Set(tokens(p));
      if (qn === pn) s += 100; else if (pn.includes(qn) || qn.includes(pn)) s += 45;
      qt.forEach(t => { if (pt.has(t)) s += 9; });
    });
    return s;
  }
  function run() {
    const query = input.value.trim(); output.replaceChildren();
    if (!query) { output.textContent = "Type a problem or question first."; return; }
    const qn = norm(query);
    if (refusals.some(p => qn.includes(p))) {
      output.innerHTML = '<h2>No governed answer</h2><p>ND Oracle cannot diagnose you, choose medication or make an individual clinical decision. Try browsing <a href="/questions/">Questions</a> or <a href="/needs/">needs</a> instead.</p>';
      return;
    }
    const ranked = index.map(r => [score(query,r),r]).filter(x => x[0] >= 12)
      .sort((a,b) => b[0]-a[0] || a[1].kind.localeCompare(b[1].kind) || a[1].title.localeCompare(b[1].title)).slice(0,5);
    if (!ranked.length) {
      output.innerHTML = '<h2>No governed answer yet</h2><p>The current catalogue does not have a strong enough route for that wording. Your query is not stored or sent to a search service. Try <a href="/needs/">browse by need</a>, <a href="/a-z/">A–Z</a>, or report a non-private content gap through <a href="/feedback/">feedback</a>.</p>';
      return;
    }
    const h = document.createElement("h2"); h.textContent = "Governed routes to inspect"; output.appendChild(h);
    const note = document.createElement("p"); note.className="meta"; note.textContent="Ranked locally from reviewed ND Oracle content. Relevance is not recommendation."; output.appendChild(note);
    const list = document.createElement("ol");
    ranked.forEach(([s,r]) => { const li=document.createElement("li"); const a=document.createElement("a"); a.href=r.route; a.textContent=r.title; li.appendChild(a); const m=document.createElement("span"); m.className="meta"; m.textContent=` ${r.kind}`; li.appendChild(m); list.appendChild(li); });
    output.appendChild(list);
  }
  button.addEventListener("click", run);
  input.addEventListener("keydown", e => { if (e.key === "Enter") { e.preventDefault(); run(); } });
})();
'''


def render_find_page() -> str:
    index_json = html.escape(discovery.browser_index_json())
    body = f'''
<section class="notice"><strong>Local governed discovery.</strong> Your words stay in this browser page. ND Oracle does not submit the query to a server, AI model, analytics system or search provider.</section>
<section aria-labelledby="find-heading">
  <h2 id="find-heading">Describe the problem in your own words</h2>
  <label for="find-input">Problem or question</label>
  <input id="find-input" type="search" autocomplete="off" spellcheck="true" maxlength="500">
  <button id="find-button" type="button">Find governed routes</button>
  <p class="meta">Examples: “work is too noisy”, “I keep putting off paperwork”, “phone calls are hard”.</p>
</section>
<section id="find-results" aria-live="polite" aria-atomic="false"><p>Results will appear here. Relevance means worth inspecting, not recommended.</p></section>
<noscript><section><h2>Discovery needs JavaScript</h2><p>The rest of ND Oracle works without JavaScript. Use <a href="/questions/">Questions</a>, <a href="/needs/">browse by need</a> or the <a href="/a-z/">A–Z</a> instead.</p></section></noscript>
<template id="search-index">{index_json}</template>
<script src="/find.js" defer></script>
'''
    return page_shell(
        "Find a governed route",
        "Start with ordinary language. Matching happens locally in your browser and points only to governed ND Oracle pages.",
        body, current=None, path="/find/",
    )


def _append_before_main_end(page: str, section: str) -> str:
    if "</main>" not in page:
        raise ValueError("Cannot locate main element")
    return page.replace("</main>", section + "</main>", 1)


def sitemap_paths(concepts: list[dict], resources: list[dict] | None = None, questions: list[dict] | None = None) -> list[str]:
    if resources is None:
        resources = load_resources()
    if questions is None:
        questions = load_questions()
    paths = list(_v09.sitemap_paths(concepts, resources, questions))
    paths.append("/find/")
    if len(paths) != len(set(paths)):
        raise ValueError("v1.0 sitemap contains duplicate routes")
    return paths


def render_sitemap(concepts: list[dict], resources: list[dict], questions: list[dict] | None = None) -> str:
    if questions is None:
        questions = load_questions()
    urls = "".join(f"  <url><loc>{html.escape(PUBLIC_ORIGIN + path)}</loc></url>\n" for path in sitemap_paths(concepts, resources, questions))
    return '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + "</urlset>\n"


def build(output_dir=DEFAULT_OUTPUT_DIR):
    questions = load_questions()
    validate_question_navigation(questions)
    destination = _v09.build(output_dir)
    concepts = load_concepts()
    resources = load_resources()
    evidence = load_evidence()
    concept_map = {item["id"]: item for item in concepts}
    evidence_map = {item["id"]: item for item in evidence}

    # Replace expanded Resource pages with the v1.0 evidence-aware renderer.
    for resource in resources:
        write_route(destination, f"resources/{resource['id']}", render_resource(resource, concept_map, questions, evidence_map))

    write_route(destination, "places", render_places_index(resources))
    write_route(destination, "find", render_find_page())
    (destination / "find.js").write_text(FIND_JS, encoding="utf-8")

    home = (destination / "index.html").read_text(encoding="utf-8")
    find_section = '''<section class="start-section" aria-labelledby="find-oracle-heading"><h2 id="find-oracle-heading">Describe the problem in your own words</h2><p>Use local governed discovery when you do not know the name of the Topic, Question or Resource you need.</p><p><a href="/find/">Find a governed route →</a></p></section>'''
    (destination / "index.html").write_text(_append_before_main_end(home, find_section), encoding="utf-8")

    for route, section in {
        "privacy": '<section><h2>Local discovery privacy</h2><p>The /find/ tool ranks the static governed catalogue in your browser. Query text is not submitted in a URL, sent to an AI or search service, stored by ND Oracle, or used for analytics. The page itself and its local script are served like other static site files.</p></section>',
        "how-it-works": '<section><h2>Governed discovery</h2><p>The /find/ tool uses deterministic local text and editorial-intent matching. It can rank governed routes, but it cannot create a new fact, diagnose a person or convert relevance into a recommendation. If no route clears the threshold, it says that the catalogue does not have a governed answer yet.</p></section>',
    }.items():
        path = destination / route / "index.html"
        path.write_text(_append_before_main_end(path.read_text(encoding="utf-8"), section), encoding="utf-8")

    headers = (destination / "_headers").read_text(encoding="utf-8")
    headers = headers.replace("script-src 'none'", "script-src 'self'")
    (destination / "_headers").write_text(headers, encoding="utf-8")

    paths = sitemap_paths(concepts, resources, questions)
    if len(paths) != V10_ROUTE_COUNT:
        raise ValueError(f"Expected {V10_ROUTE_COUNT} v1.0 canonical routes, found {len(paths)}")
    (destination / "sitemap.xml").write_text(render_sitemap(concepts, resources, questions), encoding="utf-8")
    return destination


if __name__ == "__main__":
    destination = build()
    print(f"Built The Neurodiverse Oracle public site v1.0 candidate at {destination}")
