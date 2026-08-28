from __future__ import annotations

import html
import json

from scripts import build_site_v06 as _v06
from scripts.build_site_v06 import *

QUESTIONS_DIR = ROOT / "objects" / "questions"

PRIMARY_NAV = [
    ("questions", "Questions"),
    ("understand", "Understand"),
    ("resources", "Explore"),
    ("how-it-works", "How it works"),
    ("about", "About"),
]
_v06.PRIMARY_NAV = PRIMARY_NAV

QUESTION_DISCOVERY_HOW_SECTION = (
    '<section><h2>Question-led discovery</h2>'
    '<p>Practical question pages route an ordinary need across already governed topics and resources. '
    'They show the current bounded synthesis, what is relevant to inspect, what evidence is still missing, '
    'where people may disagree and what should cause the answer to be revisited.</p>'
    '<p>A question route is not a personalised recommendation and does not turn a resource listing into proof that it works.</p></section>'
)
QUESTION_DISCOVERY_ABOUT_SECTION = (
    '<section><h2>Start with the problem, not the taxonomy</h2>'
    '<p>Question-led discovery lets a reader begin with an everyday problem and then move into the governed topics and resources behind the answer. '
    'The question page remains a route through the knowledge commons rather than a new source of authority.</p></section>'
)
if QUESTION_DISCOVERY_HOW_SECTION not in _v06.STATIC_PAGES["how-it-works"]["body"]:
    _v06.STATIC_PAGES["how-it-works"]["body"] += QUESTION_DISCOVERY_HOW_SECTION
if QUESTION_DISCOVERY_ABOUT_SECTION not in _v06.STATIC_PAGES["about"]["body"]:
    _v06.STATIC_PAGES["about"]["body"] += QUESTION_DISCOVERY_ABOUT_SECTION
_v06.STATIC_PAGES["oracle"]["body"] = (
    '<p>The current public interface exposes reviewed knowledge through topic, resource and governed question pages. '
    'Generated answers are not the source of truth. <a href="/questions/">Start with a governed question</a> or '
    '<a href="/how-it-works/">see how the evidence route works</a>.</p>'
)
STATIC_PAGES = _v06.STATIC_PAGES


def load_questions() -> list[dict]:
    questions = []
    if not QUESTIONS_DIR.is_dir():
        return questions
    for path in sorted(QUESTIONS_DIR.glob("*.json")):
        with path.open("r", encoding="utf-8") as handle:
            questions.append(json.load(handle))
    return sorted(questions, key=lambda item: item["question"].casefold())


def question_link(question: dict) -> str:
    return f"""<article class="topic-row">
  <h2><a href="/questions/{esc(question['id'])}/">{esc(question['question'])}</a></h2>
  <p>{esc(question['why_it_matters'])}</p>
</article>"""


def render_index(
    concepts: list[dict],
    resources: list[dict],
    questions: list[dict] | None = None,
) -> str:
    if questions is None:
        questions = load_questions()
    base = _v06.render_index(concepts, resources)
    practical_links = "".join(
        f'<li><a href="/questions/{esc(question["id"])}/">{esc(question["question"])}</a></li>'
        for question in questions
    )
    practical = f"""
<section class="start-section" aria-labelledby="practical-question-heading">
  <h2 id="practical-question-heading">Start with something you need to do</h2>
  <p class="section-intro">These are governed question routes across the current catalogue. They identify things worth inspecting without pretending one answer fits everyone.</p>
  <ul class="question-list">{practical_links}</ul>
  <p><a href="/questions/">See all practical questions →</a></p>
</section>
"""
    needle = '<section class="start-section" aria-labelledby="start-heading">'
    if needle not in base:
        raise ValueError("Cannot locate v0.6 homepage start section")
    return base.replace(needle, practical + needle, 1)


def render_questions_index(questions: list[dict]) -> str:
    rows = "".join(question_link(question) for question in questions)
    body = f"""
<section class="notice">
  <strong>Relevant to inspect, not recommended.</strong> These pages route ordinary needs through reviewed ND Oracle material. They do not diagnose you, choose for you or turn a resource listing into an efficacy claim.
</section>
<section aria-labelledby="questions-heading">
  <h2 id="questions-heading">{len(questions)} governed practical questions</h2>
  <p class="section-intro">Each page keeps the current synthesis, limitations, disagreement and evidence gaps visible.</p>
  <div class="topic-list">{rows}</div>
</section>
"""
    return page_shell(
        "Questions",
        "Start with an everyday problem and follow a governed route to relevant topics, tools, games, services or organisations.",
        body,
        current="questions",
        path="/questions/",
    )


def _related_question_items(
    question: dict,
    concept_map: dict[str, dict],
    resource_map: dict[str, dict],
) -> str:
    items = []
    for ref in question["related_objects"]:
        object_type = ref["type"]
        object_id = ref["id"]
        if object_type == "concept":
            target = concept_map.get(object_id)
            if target is None:
                raise ValueError(f"{question['id']}: missing related concept {object_id}")
            items.append(
                f'<li><a href="/understand/{esc(object_id)}/">{esc(target["name"])}</a> <span class="meta">Topic</span></li>'
            )
        elif object_type == "resource":
            target = resource_map.get(object_id)
            if target is None:
                raise ValueError(f"{question['id']}: missing related resource {object_id}")
            category = RESOURCE_CATEGORY_LABELS.get(
                target["category"], target["category"].replace("_", " ").title()
            )
            items.append(
                f'<li><a href="/resources/{esc(object_id)}/">{esc(target["name"])}</a> <span class="meta">{esc(category)}</span></li>'
            )
        else:
            raise ValueError(
                f"{question['id']}: public question renderer does not yet support related {object_type} objects"
            )
    return "<ul>" + "".join(items) + "</ul>"


def render_question(
    question: dict,
    concept_map: dict[str, dict],
    resource_map: dict[str, dict],
) -> str:
    reviewed = human_date(question["provenance"].get("last_reviewed"))
    status = question["status"].replace("_", " ").capitalize()
    related = _related_question_items(question, concept_map, resource_map)
    body = f"""
<p class="back-link"><a href="/questions/">← All questions</a></p>
<p class="review-meta">Last reviewed: <strong>{esc(reviewed)}</strong> · Status: <strong>{esc(status)}</strong></p>
<section class="notice">
  <strong>Relevant to inspect, not recommended.</strong> This is a bounded synthesis of the current governed catalogue, not a personalised recommendation or proof that a listed resource will work for you.
</section>
<section aria-labelledby="current-understanding-heading">
  <h2 id="current-understanding-heading">Current understanding</h2>
  <p>{esc(question["current_understanding"])}</p>
</section>
<section aria-labelledby="related-things-heading">
  <h2 id="related-things-heading">Related things to inspect</h2>
  {related}
</section>
<section aria-labelledby="evidence-needed-heading">
  <h2 id="evidence-needed-heading">What evidence is still needed</h2>
  {list_items(question["evidence_needed"])}
</section>
<section aria-labelledby="dissent-heading">
  <h2 id="dissent-heading">Where people may disagree</h2>
  {list_items(question.get("dissent", []))}
</section>
<section aria-labelledby="reopen-heading">
  <h2 id="reopen-heading">When this answer should be revisited</h2>
  {list_items(question["reopening_conditions"])}
</section>
<details class="provenance"><summary>Question provenance and review state</summary>
  <p>{esc(question["provenance"]["method"])}</p>
  <div class="meta">Created {esc(question["provenance"]["created"])} · last reviewed {esc(reviewed)} · review state {esc(question["provenance"]["review_state"])}</div>
</details>
"""
    return page_shell(
        question["question"],
        question["why_it_matters"],
        body,
        current="questions",
        path=f"/questions/{question['id']}/",
    )


def sitemap_paths(
    concepts: list[dict],
    resources: list[dict] | None = None,
    questions: list[dict] | None = None,
) -> list[str]:
    if resources is None:
        resources = load_resources()
    if questions is None:
        questions = load_questions()
    paths = _v06.sitemap_paths(concepts, resources)
    paths.append("/questions/")
    paths.extend(f"/questions/{question['id']}/" for question in questions)
    return paths


def render_sitemap(
    concepts: list[dict],
    resources: list[dict],
    questions: list[dict] | None = None,
) -> str:
    if questions is None:
        questions = load_questions()
    urls = "".join(
        f"  <url><loc>{html.escape(PUBLIC_ORIGIN + path)}</loc></url>\n"
        for path in sitemap_paths(concepts, resources, questions)
    )
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{urls}</urlset>\n"
    )


def build(output_dir=DEFAULT_OUTPUT_DIR):
    questions = load_questions()
    if not questions:
        raise ValueError("No question objects found")

    destination = _v06.build(output_dir)
    concepts = load_concepts()
    resources = load_resources()
    concept_map = {concept["id"]: concept for concept in concepts}
    resource_map = {resource["id"]: resource for resource in resources}

    (destination / "index.html").write_text(
        render_index(concepts, resources, questions), encoding="utf-8"
    )
    write_route(destination, "questions", render_questions_index(questions))
    for question in questions:
        write_route(
            destination,
            f"questions/{question['id']}",
            render_question(question, concept_map, resource_map),
        )

    (destination / "sitemap.xml").write_text(
        render_sitemap(concepts, resources, questions), encoding="utf-8"
    )
    return destination


if __name__ == "__main__":
    destination = build()
    print(f"Built The Neurodiverse Oracle public site v0.7 at {destination}")
