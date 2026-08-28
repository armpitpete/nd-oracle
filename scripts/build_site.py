from __future__ import annotations

import html
import sys
from collections import defaultdict
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts import build_site_v08 as _v08
from scripts.build_site_v08 import *

_v06 = _v08._v06
QUESTIONS_DIR = _v08.QUESTIONS_DIR
FEATURED_QUESTION_IDS = list(_v08.FEATURED_QUESTION_IDS)
BOOK_MEDIA_CATEGORIES = set(_v08.BOOK_MEDIA_CATEGORIES)

V09_SIMPLE_EXPLANATIONS = {
    "dyscalculia": "Dyscalculia is a persistent difficulty learning and using number and arithmetic skills; it is not the same as simply being bad at maths.",
    "masking": "Masking or camouflaging is when someone changes or hides parts of how they naturally communicate or behave to meet social expectations.",
    "autistic-burnout": "Autistic burnout is a community and research term for severe, long-lasting exhaustion and reduced capacity reported by some autistic people.",
    "monotropism": "Monotropism is a theory that describes attention as tending to concentrate deeply on a smaller number of interests or demands at once.",
    "interoception": "Interoception is how the nervous system senses and interprets signals from inside the body, such as hunger, heartbeat or temperature.",
    "alexithymia": "Alexithymia describes difficulty identifying or describing emotions; it is not the same thing as autism and can occur across groups.",
    "stimming": "Stimming means repetitive movements, sounds or sensory actions that can serve many functions, including enjoyment or regulation.",
    "communication-differences": "Communication differences include variation in speaking, understanding, timing, non-verbal communication and use of AAC.",
    "task-initiation": "Task initiation is the step between intending to do something and actually starting it; difficulty here can have many causes.",
    "sensory-overload": "Sensory overload is when sensory input becomes overwhelming or difficult to manage; what causes it varies by person and context.",
}
V09_COMMON_QUESTIONS = [
    ("What does dyscalculia mean, and how is it different from ordinary maths difficulty?", "dyscalculia"),
    ("What do people mean by masking or camouflaging?", "masking"),
    ("What is autistic burnout, and how certain is the evidence?", "autistic-burnout"),
    ("What is monotropism?", "monotropism"),
    ("What is interoception?", "interoception"),
    ("What is alexithymia?", "alexithymia"),
    ("Why do people stim?", "stimming"),
    ("What kinds of communication differences can matter?", "communication-differences"),
    ("Why can starting a task be difficult?", "task-initiation"),
    ("What do people mean by sensory overload?", "sensory-overload"),
]
_v06.SIMPLE_EXPLANATIONS.update(V09_SIMPLE_EXPLANATIONS)
_existing_common_targets = {target_id for _question, target_id in _v06.COMMON_QUESTIONS}
for _question, _target_id in V09_COMMON_QUESTIONS:
    if _target_id not in _existing_common_targets:
        _v06.COMMON_QUESTIONS.append((_question, _target_id))
        _existing_common_targets.add(_target_id)
SIMPLE_EXPLANATIONS = _v06.SIMPLE_EXPLANATIONS
COMMON_QUESTIONS = _v06.COMMON_QUESTIONS

QUESTION_GROUP_ORDER = [
    "Daily life & technology",
    "Sensory & environment",
    "Communication",
    "Work",
    "Education & study",
    "Assessment & diagnosis",
    "Health & wellbeing",
    "Relationships & family",
    "Information & support",
    "Games & downtime",
]

QUESTION_GROUP_RULES = [
    (
        "Assessment & diagnosis",
        ("assessment", "diagnos", "referral", "waiting list", "getting assessed"),
    ),
    (
        "Work",
        ("workplace", "work ", "job", "employer", "interview", "access to work", "employment"),
    ),
    (
        "Education & study",
        ("student", "study", "school", "education", "university", "college", "dsa", "send "),
    ),
    (
        "Communication",
        ("communication", "phone", "speaking", "processing time", "aac", "non-speaking", "non speaking", "conversation"),
    ),
    (
        "Sensory & environment",
        ("sensory", "noise", "noisy", "light", "bright", "busy place", "overload", "environment"),
    ),
    (
        "Relationships & family",
        ("parent", "parenting", "family", "relationship", "partner", "child"),
    ),
    (
        "Health & wellbeing",
        ("anxiety", "sleep", "food", "meal", "burnout", "wellbeing", "mental health", "overwhelmed", "overwhelm"),
    ),
    (
        "Games & downtime",
        ("game", "gaming", "downtime", "play"),
    ),
    (
        "Information & support",
        ("information", "support", "organisation", "organization", "autism", "dyslexia", "tourette", "dld", "dyspraxia", "learning disability", "dyscalculia"),
    ),
]

HUB_DEFINITIONS = [
    (
        "needs/daily-life",
        "Daily life",
        "Start with practical everyday tasks: getting started, routines, technology, planning and ordinary activities.",
        {"Daily life & technology", "Games & downtime"},
    ),
    (
        "needs/sensory-environment",
        "Sensory & environment",
        "Find governed routes about sensory load, noisy or bright places, overload and changing the environment around a person.",
        {"Sensory & environment"},
    ),
    (
        "needs/communication",
        "Communication",
        "Find routes for phone calls, processing time, speaking, AAC and communication access without assuming one communication style fits everyone.",
        {"Communication"},
    ),
    (
        "needs/work",
        "Work",
        "Find workplace support, adjustments, disclosure, interviews, job-search support and Access to Work routes.",
        {"Work"},
    ),
    (
        "needs/education-study",
        "Education & study",
        "Find study organisation, disabled-student support, SEND information and education access routes.",
        {"Education & study"},
    ),
    (
        "needs/assessment-diagnosis",
        "Assessment & diagnosis",
        "Find bounded information about assessment and diagnosis routes without turning ND Oracle into a diagnostic test.",
        {"Assessment & diagnosis"},
    ),
    (
        "needs/health-wellbeing",
        "Health & wellbeing",
        "Find current routes around anxiety, sleep, food-related task demands, burnout and wellbeing while keeping clinical boundaries visible.",
        {"Health & wellbeing"},
    ),
    (
        "needs/relationships-family",
        "Relationships & family",
        "Find routes relevant to family life, parenting and relationships where the present catalogue has governed material.",
        {"Relationships & family"},
    ),
]

NAVIGATION_ROUTES = (
    "/needs/",
    "/needs/daily-life/",
    "/needs/sensory-environment/",
    "/needs/communication/",
    "/needs/work/",
    "/needs/education-study/",
    "/needs/assessment-diagnosis/",
    "/needs/health-wellbeing/",
    "/needs/relationships-family/",
    "/types/",
    "/places/",
    "/a-z/",
)
V09_ROUTE_COUNT = 125


def _question_search_text(question: dict) -> str:
    return " ".join(
        str(question.get(field, ""))
        for field in ("question", "why_it_matters", "current_understanding")
    ).casefold()


def classify_question_group(question: dict) -> str:
    text = _question_search_text(question)
    for group, needles in QUESTION_GROUP_RULES:
        if any(needle in text for needle in needles):
            return group
    return "Daily life & technology"


def build_question_groups(questions: list[dict]) -> list[tuple[str, list[str]]]:
    grouped: dict[str, list[str]] = {name: [] for name in QUESTION_GROUP_ORDER}
    for question in sorted(questions, key=lambda item: item["question"].casefold()):
        grouped[classify_question_group(question)].append(question["id"])
    return [(name, grouped[name]) for name in QUESTION_GROUP_ORDER if grouped[name]]


def _sync_question_groups(questions: list[dict]) -> None:
    global QUESTION_GROUPS
    QUESTION_GROUPS = build_question_groups(questions)
    _v08.QUESTION_GROUPS = QUESTION_GROUPS


QUESTION_GROUPS = build_question_groups(load_questions())
_v08.QUESTION_GROUPS = QUESTION_GROUPS


def validate_question_navigation(questions: list[dict]) -> None:
    _sync_question_groups(questions)
    _v08.validate_question_navigation(questions)


def _append_before_main_end(page: str, section: str) -> str:
    marker = "</main>"
    if marker not in page:
        raise ValueError("Cannot locate page main element")
    return page.replace(marker, section + marker, 1)


def render_index(
    concepts: list[dict],
    resources: list[dict],
    questions: list[dict] | None = None,
) -> str:
    if questions is None:
        questions = load_questions()
    _sync_question_groups(questions)
    page = _v08.render_index(concepts, resources, questions)
    browse = """
<section class="start-section" aria-labelledby="browse-whole-heading">
  <h2 id="browse-whole-heading">Browse the whole knowledge base</h2>
  <p class="section-intro">Use needs, content type, geographic scope or the complete A–Z when you do not want to start from a diagnosis.</p>
  <ul class="question-list">
    <li><a href="/needs/">Browse by need</a></li>
    <li><a href="/types/">Browse by content type</a></li>
    <li><a href="/places/">Browse by geographic scope</a></li>
    <li><a href="/a-z/">A–Z of all governed content</a></li>
  </ul>
</section>
"""
    return _append_before_main_end(page, browse)


def render_questions_index(questions: list[dict]) -> str:
    _sync_question_groups(questions)
    page = _v08.render_questions_index(questions)
    browse = """
<section aria-labelledby="question-browse-heading">
  <h2 id="question-browse-heading">Other ways to browse</h2>
  <p><a href="/needs/">Browse practical needs and life areas</a> · <a href="/a-z/">A–Z of all content</a></p>
</section>
"""
    return _append_before_main_end(page, browse)


def related_questions(question: dict, questions: list[dict], limit: int = 5) -> list[dict]:
    refs = {(ref.get("type"), ref.get("id")) for ref in question.get("related_objects", [])}
    ranked: list[tuple[int, str, dict]] = []
    for candidate in questions:
        if candidate["id"] == question["id"]:
            continue
        candidate_refs = {
            (ref.get("type"), ref.get("id"))
            for ref in candidate.get("related_objects", [])
        }
        score = len(refs & candidate_refs)
        if score:
            ranked.append((-score, candidate["question"].casefold(), candidate))
    ranked.sort(key=lambda item: (item[0], item[1]))
    return [item[2] for item in ranked[:limit]]


def render_question(
    question: dict,
    concept_map: dict[str, dict],
    resource_map: dict[str, dict],
    questions: list[dict] | None = None,
) -> str:
    if questions is None:
        questions = load_questions()
    page = _v08.render_question(question, concept_map, resource_map)
    related = related_questions(question, questions)
    if related:
        items = "".join(
            f'<li><a href="/questions/{esc(item["id"])}/">{esc(item["question"])}</a></li>'
            for item in related
        )
    else:
        items = '<li>No adjacent governed question has enough shared material yet.</li>'
    section = f"""
<section aria-labelledby="related-questions-heading">
  <h2 id="related-questions-heading">Related questions</h2>
  <ul>{items}</ul>
</section>
"""
    marker = '<section aria-labelledby="evidence-needed-heading">'
    if marker not in page:
        raise ValueError(f"{question['id']}: cannot locate evidence-needed section")
    return page.replace(marker, section + marker, 1)


def resource_scope(resource: dict) -> tuple[str, str]:
    audience = str(resource.get("audience_or_context", "")).casefold()
    whole = " ".join(
        [
            str(resource.get("description", "")),
            str(resource.get("audience_or_context", "")),
            *[str(item) for item in resource.get("limitations", [])],
            *[str(item) for item in resource.get("cost_or_access_notes", [])],
        ]
    ).casefold()
    if "great britain" in audience or "england, scotland and wales" in audience:
        return (
            "Great Britain",
            "The reviewed audience/scope text identifies England, Scotland and Wales or Great Britain. Northern Ireland may use different routes.",
        )
    if "northern ireland" in audience and "england" not in audience and "scotland" not in audience and "wales" not in audience:
        return ("Northern Ireland", "The reviewed audience/scope text specifically identifies Northern Ireland.")
    if "england" in audience and "scotland" not in audience and "wales" not in audience:
        return ("England", "The reviewed audience/scope text specifically identifies England.")
    if "united kingdom" in audience or " uk " in f" {audience} " or "uk-wide" in whole:
        return ("United Kingdom", "The reviewed listing describes a UK-wide or United Kingdom audience/scope.")
    return (
        "International / not jurisdiction-specific",
        "No narrower UK jurisdiction is asserted by the reviewed audience text; check the resource itself for local availability and eligibility.",
    )


def render_resource(
    resource: dict,
    concept_map: dict[str, dict],
    questions: list[dict],
) -> str:
    page = _v08.render_resource(resource, concept_map, questions)
    label, explanation = resource_scope(resource)
    category = RESOURCE_CATEGORY_LABELS.get(
        resource["category"], resource["category"].replace("_", " ").title()
    )
    section = f"""
<section aria-labelledby="scope-heading">
  <h2 id="scope-heading">Scope for navigation</h2>
  <p><strong>{esc(label)}</strong> · {esc(category)}</p>
  <p class="meta">{esc(explanation)} This label helps navigation; it is not an eligibility or legal determination.</p>
  <p><a href="/places/">Browse resources by place</a> · <a href="/types/">Browse by content type</a></p>
</section>
"""
    marker = '<section aria-labelledby="limits-heading">'
    if marker not in page:
        raise ValueError(f"{resource['id']}: cannot locate limitations section")
    return page.replace(marker, section + marker, 1)


def render_resources_index(resources: list[dict]) -> str:
    page = _v08.render_resources_index(resources)
    section = """
<section aria-labelledby="resource-browse-heading">
  <h2 id="resource-browse-heading">Browse the catalogue</h2>
  <p><a href="/types/">By content type</a> · <a href="/places/">By geographic scope</a> · <a href="/a-z/">A–Z</a></p>
</section>
"""
    return _append_before_main_end(page, section)


def _question_map(questions: list[dict]) -> dict[str, dict]:
    return {question["id"]: question for question in questions}


def _questions_for_groups(questions: list[dict], group_names: set[str]) -> list[dict]:
    mapping = _question_map(questions)
    ids = [
        question_id
        for group, group_ids in QUESTION_GROUPS
        if group in group_names
        for question_id in group_ids
    ]
    return [mapping[question_id] for question_id in ids]


def _linked_content_from_questions(
    questions: list[dict],
    concept_map: dict[str, dict],
    resource_map: dict[str, dict],
) -> tuple[list[dict], list[dict]]:
    concept_ids: set[str] = set()
    resource_ids: set[str] = set()
    for question in questions:
        for ref in question.get("related_objects", []):
            if ref.get("type") == "concept" and ref.get("id") in concept_map:
                concept_ids.add(ref["id"])
            if ref.get("type") == "resource" and ref.get("id") in resource_map:
                resource_ids.add(ref["id"])
    concepts = sorted((concept_map[item] for item in concept_ids), key=lambda item: item["name"].casefold())
    resources = sorted((resource_map[item] for item in resource_ids), key=lambda item: item["name"].casefold())
    return concepts, resources


def render_need_hub(
    route: str,
    title: str,
    intro: str,
    group_names: set[str],
    questions: list[dict],
    concept_map: dict[str, dict],
    resource_map: dict[str, dict],
) -> str:
    selected = _questions_for_groups(questions, group_names)
    concepts, resources = _linked_content_from_questions(selected, concept_map, resource_map)
    question_rows = "".join(_v08.question_link(question) for question in selected)
    concept_items = "".join(
        f'<li><a href="/understand/{esc(item["id"])}/">{esc(item["name"])}</a></li>'
        for item in concepts
    ) or "<li>No topic link is recorded yet.</li>"
    resource_items = "".join(
        f'<li><a href="/resources/{esc(item["id"])}/">{esc(item["name"])}</a></li>'
        for item in resources
    ) or "<li>No resource link is recorded yet.</li>"
    body = f"""
<p class="back-link"><a href="/needs/">← All needs</a></p>
<section class="notice"><strong>Relevant to inspect, not recommended.</strong> This hub groups governed routes; it does not infer a diagnosis or choose support for an individual.</section>
<section aria-labelledby="need-questions-heading">
  <h2 id="need-questions-heading">Practical questions</h2>
  <div class="topic-list">{question_rows}</div>
</section>
<section aria-labelledby="need-topics-heading"><h2 id="need-topics-heading">Related topics</h2><ul>{concept_items}</ul></section>
<section aria-labelledby="need-resources-heading"><h2 id="need-resources-heading">Related resources</h2><ul>{resource_items}</ul></section>
"""
    return page_shell(title, intro, body, current="questions", path=f"/{route}/")


def render_needs_index(questions: list[dict]) -> str:
    _sync_question_groups(questions)
    question_map = _question_map(questions)
    hub_by_group = {
        group: (route, title)
        for route, title, _intro, groups in HUB_DEFINITIONS
        for group in groups
    }
    sections = []
    for group, ids in QUESTION_GROUPS:
        if group in hub_by_group:
            route, title = hub_by_group[group]
            heading = f'<h2><a href="/{esc(route)}/">{esc(title)}</a></h2>'
        else:
            heading = f"<h2>{esc(group)}</h2>"
        links = "".join(
            f'<li><a href="/questions/{esc(question_id)}/">{esc(question_map[question_id]["question"])}</a></li>'
            for question_id in ids
        )
        sections.append(f"<section>{heading}<ul>{links}</ul></section>")
    body = f"""
<section class="notice"><strong>Start with the need, not the label.</strong> Every current governed Question appears here exactly once in its primary navigation group.</section>
{''.join(sections)}
"""
    return page_shell(
        "Browse by need",
        "Start from the problem or life area you are dealing with, then follow governed questions into topics and resources.",
        body,
        current="questions",
        path="/needs/",
    )


def render_types_index(concepts: list[dict], resources: list[dict], questions: list[dict]) -> str:
    sections = [
        f'<section><h2>Questions</h2><p>{len(questions)} governed practical questions.</p><p><a href="/questions/">Browse Questions</a></p></section>',
        f'<section><h2>Topics</h2><p>{len(concepts)} reviewed Concepts.</p><p><a href="/understand/">Browse Topics</a></p></section>',
    ]
    grouped: dict[str, list[dict]] = defaultdict(list)
    for resource in resources:
        grouped[resource["category"]].append(resource)
    preferred = [
        "organisation", "service", "community", "tool", "app", "practical_guide",
        "education_work_resource", "accommodation", "game", "book", "media", "product", "other",
    ]
    for category in preferred:
        items = sorted(grouped.get(category, []), key=lambda item: item["name"].casefold())
        if not items:
            continue
        label = RESOURCE_CATEGORY_LABELS.get(category, category.replace("_", " ").title())
        links = "".join(
            f'<li><a href="/resources/{esc(item["id"])}/">{esc(item["name"])}</a></li>'
            for item in items
        )
        sections.append(f"<section><h2>{esc(label)}</h2><ul>{links}</ul></section>")
    return page_shell(
        "Browse by content type",
        "Separate Questions, Topics, organisations, services, tools, apps, games, books, guides and other governed resources.",
        "".join(sections),
        current="resources",
        path="/types/",
    )


def render_places_index(resources: list[dict]) -> str:
    grouped: dict[str, list[dict]] = defaultdict(list)
    explanations: dict[str, str] = {}
    for resource in resources:
        label, explanation = resource_scope(resource)
        grouped[label].append(resource)
        explanations[label] = explanation
    order = ["United Kingdom", "Great Britain", "England", "Northern Ireland", "International / not jurisdiction-specific"]
    sections = []
    for label in order:
        items = sorted(grouped.get(label, []), key=lambda item: item["name"].casefold())
        if not items:
            continue
        links = "".join(
            f'<li><a href="/resources/{esc(item["id"])}/">{esc(item["name"])}</a></li>'
            for item in items
        )
        sections.append(
            f'<section><h2>{esc(label)}</h2><p class="meta">{esc(explanations[label])}</p><ul>{links}</ul></section>'
        )
    body = (
        '<section class="notice"><strong>Navigation scope, not eligibility.</strong> These groups are derived from each reviewed listing\'s audience and limitation text. Always check the resource itself for current jurisdiction and eligibility.</section>'
        + "".join(sections)
    )
    return page_shell(
        "Browse by geographic scope",
        "Distinguish UK, Great Britain, England, Northern Ireland and resources without a narrower jurisdictional scope.",
        body,
        current="resources",
        path="/places/",
    )


def _az_letter(label: str) -> str:
    for character in label.strip():
        if character.isalnum():
            return character.upper()
    return "#"


def render_az_index(concepts: list[dict], resources: list[dict], questions: list[dict]) -> str:
    entries: list[tuple[str, str, str]] = []
    entries.extend((item["name"], "Topic", f'/understand/{item["id"]}/') for item in concepts)
    entries.extend((item["name"], "Resource", f'/resources/{item["id"]}/') for item in resources)
    entries.extend((item["question"], "Question", f'/questions/{item["id"]}/') for item in questions)
    entries.sort(key=lambda item: item[0].casefold())
    grouped: dict[str, list[tuple[str, str, str]]] = defaultdict(list)
    for entry in entries:
        grouped[_az_letter(entry[0])].append(entry)
    sections = []
    for letter in sorted(grouped, key=lambda value: (value == "#", value)):
        links = "".join(
            f'<li><a href="{esc(route)}">{esc(label)}</a> <span class="meta">{esc(kind)}</span></li>'
            for label, kind, route in grouped[letter]
        )
        sections.append(f'<section><h2>{esc(letter)}</h2><ul>{links}</ul></section>')
    return page_shell(
        "A–Z",
        f"All {len(entries)} governed Topics, Resources and Questions in one alphabetical index.",
        "".join(sections),
        current="resources",
        path="/a-z/",
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
    _sync_question_groups(questions)
    paths = list(_v08.sitemap_paths(concepts, resources, questions))
    paths.extend(NAVIGATION_ROUTES)
    if len(paths) != len(set(paths)):
        raise ValueError("v0.9 sitemap contains duplicate routes")
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
    _sync_question_groups(questions)
    validate_question_navigation(questions)

    destination = _v08.build(output_dir)
    concepts = load_concepts()
    resources = load_resources()
    concept_map = {item["id"]: item for item in concepts}
    resource_map = {item["id"]: item for item in resources}

    (destination / "index.html").write_text(
        render_index(concepts, resources, questions), encoding="utf-8"
    )
    write_route(destination, "questions", render_questions_index(questions))
    write_route(destination, "resources", render_resources_index(resources))

    for question in questions:
        write_route(
            destination,
            f"questions/{question['id']}",
            render_question(question, concept_map, resource_map, questions),
        )
    for resource in resources:
        write_route(
            destination,
            f"resources/{resource['id']}",
            render_resource(resource, concept_map, questions),
        )

    write_route(destination, "needs", render_needs_index(questions))
    for route, title, intro, groups in HUB_DEFINITIONS:
        write_route(
            destination,
            route,
            render_need_hub(route, title, intro, groups, questions, concept_map, resource_map),
        )
    write_route(destination, "types", render_types_index(concepts, resources, questions))
    write_route(destination, "places", render_places_index(resources))
    write_route(destination, "a-z", render_az_index(concepts, resources, questions))

    paths = sitemap_paths(concepts, resources, questions)
    if len(paths) != V09_ROUTE_COUNT:
        raise ValueError(f"Expected {V09_ROUTE_COUNT} v0.9 canonical routes, found {len(paths)}")
    (destination / "sitemap.xml").write_text(
        render_sitemap(concepts, resources, questions), encoding="utf-8"
    )
    return destination


if __name__ == "__main__":
    destination = build()
    print(f"Built The Neurodiverse Oracle public site v0.9 at {destination}")
