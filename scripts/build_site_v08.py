from __future__ import annotations

import html
import json
import sys
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts import build_site_v06 as _v06
from scripts.build_site_v06 import *

QUESTIONS_DIR = ROOT / "objects" / "questions"

PRIMARY_NAV = [
    ("questions", "Questions"),
    ("understand", "Topics"),
    ("resources", "Resources"),
    ("how-it-works", "How it works"),
    ("about", "About"),
]
_v06.PRIMARY_NAV = PRIMARY_NAV

# Keep one immutable handle to the proven v0.6 page shell. Tests reload this
# module repeatedly, so a v0.8 wrapper must never wrap an earlier v0.8 wrapper.
if not hasattr(_v06, "_V08_ORIGINAL_PAGE_SHELL"):
    _v06._V08_ORIGINAL_PAGE_SHELL = _v06.page_shell
_page_shell_v06 = _v06._V08_ORIGINAL_PAGE_SHELL


def page_shell(*args, **kwargs) -> str:
    page = _page_shell_v06(*args, **kwargs)
    return page.replace('<a href="/resources/">Explore</a>', '<a href="/resources/">Resources</a>')


_v06.page_shell = page_shell

BOOK_MEDIA_CATEGORIES = {"book", "media"}

QUESTION_GROUPS = [
    (
        "Everyday life & technology",
        [
            "task-starting-and-organisation",
            "make-device-easier-to-use",
        ],
    ),
    (
        "Work & study",
        [
            "workplace-support-great-britain",
            "reasonable-adjustments-at-work-great-britain",
            "disabled-student-support-england",
            "disabled-person-looking-for-work-uk",
        ],
    ),
    (
        "Finding information & support",
        [
            "autism-information-and-support",
            "dyslexia-information-and-support-uk",
            "tourette-information-and-support-uk",
            "learning-disability-information-and-support-uk",
            "dld-information-and-support",
            "adult-dyspraxia-information-uk",
        ],
    ),
    (
        "Games & downtime",
        ["low-time-pressure-games"],
    ),
    (
        "Anxiety & self-management",
        ["autism-anxiety-tools"],
    ),
]

FEATURED_QUESTION_IDS = [
    "task-starting-and-organisation",
    "reasonable-adjustments-at-work-great-britain",
    "disabled-student-support-england",
    "dld-information-and-support",
    "low-time-pressure-games",
    "autism-information-and-support",
]

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

_RESOURCE_SUBNAV_V06 = (
    '<nav class="resource-subnav" aria-label="Explore resources">\n'
    '  <a href="/resources/">Everything</a>\n'
    '  <a href="/tools/">Tools &amp; apps</a>\n'
    '  <a href="/games/">Games</a>\n'
    '  <a href="/community/">Support &amp; organisations</a>\n'
    '</nav>'
)
_RESOURCE_SUBNAV_V08 = (
    '<nav class="resource-subnav" aria-label="Browse resources">\n'
    '  <a href="/resources/">All resources</a>\n'
    '  <a href="/tools/">Tools &amp; practical help</a>\n'
    '  <a href="/games/">Games</a>\n'
    '  <a href="/books-media/">Books &amp; media</a>\n'
    '  <a href="/community/">Support &amp; organisations</a>\n'
    '</nav>'
)
_render_resource_collection_v06 = _v06.render_resource_collection


def render_resource_collection(
    resources: list[dict],
    *,
    title: str,
    intro: str,
    route: str,
    categories: set[str] | None = None,
) -> str:
    page = _render_resource_collection_v06(
        resources,
        title=title,
        intro=intro,
        route=route,
        categories=categories,
    )
    if _RESOURCE_SUBNAV_V06 not in page:
        raise ValueError("Cannot locate v0.6 resource sub-navigation")
    return page.replace(_RESOURCE_SUBNAV_V06, _RESOURCE_SUBNAV_V08, 1)


def render_resources_index(resources: list[dict]) -> str:
    return render_resource_collection(
        resources,
        title="Resources",
        intro="Tools, practical guides, games, books, services and organisations, described with their limitations and access conditions visible.",
        route="resources",
    )


def load_questions() -> list[dict]:
    questions = []
    if not QUESTIONS_DIR.is_dir():
        return questions
    for path in sorted(QUESTIONS_DIR.glob("*.json")):
        with path.open("r", encoding="utf-8") as handle:
            questions.append(json.load(handle))
    return sorted(questions, key=lambda item: item["question"].casefold())


def validate_question_navigation(questions: list[dict]) -> None:
    question_ids = {question["id"] for question in questions}
    grouped_ids = [question_id for _, ids in QUESTION_GROUPS for question_id in ids]
    grouped_set = set(grouped_ids)
    if len(grouped_ids) != len(grouped_set):
        raise ValueError("Question navigation groups contain duplicate question IDs")
    if grouped_set != question_ids:
        raise ValueError(
            "Question navigation groups must exactly cover the governed Question corpus: "
            f"missing={sorted(question_ids - grouped_set)}; unexpected={sorted(grouped_set - question_ids)}"
        )
    featured_set = set(FEATURED_QUESTION_IDS)
    if len(FEATURED_QUESTION_IDS) != len(featured_set) or not featured_set <= question_ids:
        raise ValueError("Featured questions must be unique governed Question IDs")


def question_link(question: dict) -> str:
    return f"""<article class="topic-row">
  <h3><a href="/questions/{esc(question['id'])}/">{esc(question['question'])}</a></h3>
  <p>{esc(question['why_it_matters'])}</p>
</article>"""


def render_index(
    concepts: list[dict],
    resources: list[dict],
    questions: list[dict] | None = None,
) -> str:
    if questions is None:
        questions = load_questions()
    validate_question_navigation(questions)
    question_map = {question["id"]: question for question in questions}
    base = _v06.render_index(concepts, resources)
    practical_links = "".join(
        f'<li><a href="/questions/{esc(question_id)}/">{esc(question_map[question_id]["question"])}</a></li>'
        for question_id in FEATURED_QUESTION_IDS
    )
    practical = f"""
<section class="start-section" aria-labelledby="practical-question-heading">
  <h2 id="practical-question-heading">Start with something you need to do</h2>
  <p class="section-intro">These are governed routes across the current catalogue. They identify things worth inspecting without pretending one answer fits everyone.</p>
  <ul class="question-list">{practical_links}</ul>
  <p><a href="/questions/">Browse all {len(questions)} practical questions →</a></p>
</section>
"""
    needle = '<section class="start-section" aria-labelledby="start-heading">'
    if needle not in base:
        raise ValueError("Cannot locate v0.6 homepage start section")
    base = base.replace(needle, practical + needle, 1)

    base = base.replace(
        '<a class="entry-card" href="/tools/"><strong>Tools &amp; apps</strong>',
        '<a class="entry-card" href="/tools/"><strong>Tools &amp; practical help</strong>',
        1,
    )
    book_media_count = sum(1 for resource in resources if resource["category"] in BOOK_MEDIA_CATEGORIES)
    everything_card = (
        f'<a class="entry-card" href="/resources/"><strong>Everything</strong><span>{len(resources)} reviewed resources</span></a>'
    )
    books_card = (
        f'<a class="entry-card" href="/books-media/"><strong>Books &amp; media</strong><span>{book_media_count} current entries</span></a>'
    )
    if everything_card not in base:
        raise ValueError("Cannot locate homepage all-resources card")
    return base.replace(everything_card, books_card + everything_card, 1)


def render_questions_index(questions: list[dict]) -> str:
    validate_question_navigation(questions)
    question_map = {question["id"]: question for question in questions}
    groups = []
    for group_name, ids in QUESTION_GROUPS:
        group_slug = group_name.lower().replace(" ", "-").replace("&", "and")
        rows = "".join(question_link(question_map[question_id]) for question_id in ids)
        groups.append(
            f'<section aria-labelledby="question-group-{esc(group_slug)}">'
            f'<h2 id="question-group-{esc(group_slug)}">{esc(group_name)}</h2>'
            f'<div class="topic-list">{rows}</div></section>'
        )
    body = f"""
<section class="notice">
  <strong>Relevant to inspect, not recommended.</strong> These pages route ordinary needs through reviewed ND Oracle material. They do not diagnose you, choose for you or turn a resource listing into an efficacy claim.
</section>
<section aria-labelledby="questions-heading">
  <h2 id="questions-heading">{len(questions)} governed practical questions</h2>
  <p class="section-intro">Browse by the kind of problem you are trying to solve. Each page keeps the current synthesis, limitations, disagreement and evidence gaps visible.</p>
</section>
{''.join(groups)}
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


def _question_uses_ref(question: dict, object_type: str, object_id: str) -> bool:
    return any(
        ref.get("type") == object_type and ref.get("id") == object_id
        for ref in question.get("related_objects", [])
    )


def _question_links_for_ref(questions: list[dict], object_type: str, object_id: str) -> str:
    matched = [question for question in questions if _question_uses_ref(question, object_type, object_id)]
    if not matched:
        return '<p class="meta">No practical question route links here yet.</p>'
    return "<ul>" + "".join(
        f'<li><a href="/questions/{esc(question["id"])}/">{esc(question["question"])}</a></li>'
        for question in matched
    ) + "</ul>"


def _resource_links_for_concept(resources: list[dict], concept_id: str) -> str:
    matched = [
        resource
        for resource in resources
        if any(
            ref.get("type") == "concept" and ref.get("id") == concept_id
            for ref in resource.get("related_objects", [])
        )
    ]
    if not matched:
        return '<p class="meta">No reviewed resource link recorded yet.</p>'
    return "<ul>" + "".join(
        f'<li><a href="/resources/{esc(resource["id"])}/">{esc(resource["name"])}</a> '
        f'<span class="meta">{esc(RESOURCE_CATEGORY_LABELS.get(resource["category"], resource["category"].replace("_", " ").title()))}</span></li>'
        for resource in matched
    ) + "</ul>"


def render_concept(
    concept: dict,
    concept_map: dict[str, dict],
    resources: list[dict],
    questions: list[dict],
) -> str:
    page = _v06.render_concept(concept, concept_map)
    needle = '<section aria-labelledby="sources-heading">'
    if needle not in page:
        raise ValueError(f"{concept['id']}: cannot locate sources section for navigation injection")
    discovery = f"""
<section aria-labelledby="next-routes-heading">
  <h2 id="next-routes-heading">Useful next routes</h2>
  <h3>Practical questions</h3>
  {_question_links_for_ref(questions, "concept", concept["id"])}
  <h3>Related resources</h3>
  {_resource_links_for_concept(resources, concept["id"])}
</section>
"""
    return page.replace(needle, discovery + needle, 1)


def render_resource(
    resource: dict,
    concept_map: dict[str, dict],
    questions: list[dict],
) -> str:
    page = _v06.render_resource(resource, concept_map)
    needle = '<section aria-labelledby="limits-heading">'
    if needle not in page:
        raise ValueError(f"{resource['id']}: cannot locate limitations section for navigation injection")
    discovery = f"""
<section aria-labelledby="resource-question-heading">
  <h2 id="resource-question-heading">Questions that lead here</h2>
  {_question_links_for_ref(questions, "resource", resource["id"])}
</section>
"""
    return page.replace(needle, discovery + needle, 1)


def render_books_media_index(resources: list[dict]) -> str:
    return render_resource_collection(
        resources,
        title="Books & media",
        intro="Reviewed books and media in the ND Oracle catalogue, with context, limitations and conflicts kept visible.",
        route="books-media",
        categories=BOOK_MEDIA_CATEGORIES,
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
    paths.append("/books-media/")
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
    validate_question_navigation(questions)

    destination = _v06.build(output_dir)
    concepts = load_concepts()
    resources = load_resources()
    concept_map = {concept["id"]: concept for concept in concepts}
    resource_map = {resource["id"]: resource for resource in resources}

    (destination / "index.html").write_text(
        render_index(concepts, resources, questions), encoding="utf-8"
    )
    write_route(destination, "resources", render_resources_index(resources))
    write_route(
        destination,
        "tools",
        render_resource_collection(
            resources,
            title="Tools & practical help",
            intro="Tools, apps, practical guides and products that can make everyday tasks, access, work or study easier to navigate.",
            route="tools",
            categories=TOOL_CATEGORIES,
        ),
    )
    write_route(
        destination,
        "games",
        render_resource_collection(
            resources,
            title="Games",
            intro="Games described by play characteristics, pressure, accessibility and possible poor fit — not as treatments or prescriptions.",
            route="games",
            categories={"game"},
        ),
    )
    write_route(
        destination,
        "community",
        render_resource_collection(
            resources,
            title="Support & organisations",
            intro="Services, organisations and communities with their scope, geography and limitations kept visible.",
            route="community",
            categories=COMMUNITY_CATEGORIES,
        ),
    )
    write_route(destination, "books-media", render_books_media_index(resources))

    for concept in concepts:
        write_route(
            destination,
            f"understand/{concept['id']}",
            render_concept(concept, concept_map, resources, questions),
        )
    for resource in resources:
        write_route(
            destination,
            f"resources/{resource['id']}",
            render_resource(resource, concept_map, questions),
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
    print(f"Built The Neurodiverse Oracle public site v0.8 at {destination}")
