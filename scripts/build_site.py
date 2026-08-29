from __future__ import annotations

import html
import json
import shutil
import sys
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path
from urllib.parse import urlsplit

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts import discovery

ROOT = Path(__file__).resolve().parents[1]
OBJECTS_DIR = ROOT / "objects" / "concepts"
RESOURCES_DIR = ROOT / "objects" / "resources"
QUESTIONS_DIR = ROOT / "objects" / "questions"
EVIDENCE_DIR = ROOT / "objects" / "evidence"
SITE_DIR = ROOT / "site"
DEFAULT_OUTPUT_DIR = ROOT / "dist"
OUTPUT_MARKER = "nd-oracle-site-v0.2\n"
PUBLIC_ORIGIN = "https://ndoracle.org"
V10_ROUTE_COUNT = 142

PRIMARY_NAV = [
    ("questions", "Questions"),
    ("understand", "Topics"),
    ("resources", "Resources"),
    ("how-it-works", "How it works"),
    ("about", "About"),
]

RESOURCE_CATEGORY_LABELS = {
    "tool": "Tool", "app": "App", "game": "Game", "book": "Book", "media": "Media",
    "service": "Service", "accommodation": "Accommodation", "organisation": "Organisation",
    "community": "Community", "practical_guide": "Practical guide", "product": "Product",
    "education_work_resource": "Education/work resource", "other": "Other",
}
TOOL_CATEGORIES = {"tool", "app", "accommodation", "practical_guide", "product", "education_work_resource"}
COMMUNITY_CATEGORIES = {"organisation", "community", "service"}
BOOK_MEDIA_CATEGORIES = {"book", "media"}

SIMPLE_EXPLANATIONS = {
    "neurodiversity": "People's brains and nervous systems vary. Neurodiversity is a word for that variation, and it is also used when people talk about rights, disability, support and how neurological differences should be understood.",
    "autism": "Autistic people can experience communication, social situations, routines, interests and sensory input differently. Autism looks different from person to person, and support needs can vary.",
    "adhd": "ADHD can affect attention, activity, impulsivity and managing everyday tasks. It can look different between people and situations, and diagnosis needs more than a checklist or a single test.",
    "executive-function": "Executive functions help us hold things in mind, switch attention, pause responses and organise actions towards a goal. Difficulties with them can make starting, planning or finishing tasks hard, but they are not a diagnosis by themselves.",
    "sensory-processing": "People differ in how strongly they notice and respond to sound, light, touch, movement and other sensory input. These differences can affect comfort and everyday life, and they are not unique to one diagnosis.",
    "dyslexia": "Dyslexia mainly affects learning and using word reading and spelling. It can continue into adulthood, and it does not mean that someone has low intelligence.",
    "developmental-coordination-disorder": "Developmental co-ordination disorder (DCD) affects how easily someone learns and carries out coordinated movements. Everyday activities can take more effort, and the difficulties can continue into adulthood.",
    "tourette-syndrome": "Tourette syndrome involves motor and vocal tics that change over time. Swearing is not what defines Tourette syndrome, and support or treatment should depend on what is actually difficult for the person.",
    "learning-disability": "In the UK, a learning disability means lifelong difficulty learning or understanding new information together with difficulty managing everyday life independently. It is not the same thing as a specific learning difficulty such as dyslexia.",
    "developmental-language-disorder": "Developmental language disorder (DLD) is a persistent difficulty understanding and/or using language that affects everyday life. Bilingualism does not cause DLD, and DLD can occur alongside other developmental conditions.",
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

COMMON_QUESTIONS = [
    ("What does neurodiversity mean?", "neurodiversity"), ("What is autism?", "autism"),
    ("What is ADHD?", "adhd"), ("Why can starting or organising tasks feel hard?", "executive-function"),
    ("Why can sound, light or touch feel intense?", "sensory-processing"),
    ("Why can reading or spelling stay difficult?", "dyslexia"),
    ("Why can coordination and everyday movement be hard?", "developmental-coordination-disorder"),
    ("What are tics and Tourette syndrome?", "tourette-syndrome"),
    ("What does learning disability mean in the UK?", "learning-disability"),
    ("Why can understanding or using language be difficult?", "developmental-language-disorder"),
    ("What does dyscalculia mean, and how is it different from ordinary maths difficulty?", "dyscalculia"),
    ("What do people mean by masking or camouflaging?", "masking"),
    ("What is autistic burnout, and how certain is the evidence?", "autistic-burnout"),
    ("What is monotropism?", "monotropism"), ("What is interoception?", "interoception"),
    ("What is alexithymia?", "alexithymia"), ("Why do people stim?", "stimming"),
    ("What kinds of communication differences can matter?", "communication-differences"),
    ("Why can starting a task be difficult?", "task-initiation"),
    ("What do people mean by sensory overload?", "sensory-overload"),
]

QUESTION_GROUPS = [
    ("Daily life & technology", ["task-starting-and-organisation", "make-device-easier-to-use", "meal-planning-and-everyday-food-tasks"]),
    ("Sensory & environment", ["make-noisy-bright-place-easier", "sensory-overload-what-can-i-change"]),
    ("Communication", ["aac-and-nonspeaking-communication", "phone-calls-are-difficult", "processing-time-in-conversations-meetings"]),
    ("Work", ["workplace-support-great-britain", "reasonable-adjustments-at-work-great-britain", "disabled-person-looking-for-work-uk", "disclosing-disability-neurodivergence-at-work", "job-interview-adjustments-great-britain"]),
    ("Education & study", ["disabled-student-support-england", "organising-study-and-assignments", "send-support-school-college-england"]),
    ("Assessment & diagnosis", ["adult-adhd-assessment-england", "adult-autism-assessment-england"]),
    ("Health & wellbeing", ["autism-anxiety-tools", "masking-exhaustion-and-autistic-burnout", "sleep-and-winding-down-routines", "healthcare-communication-adjustments-england"]),
    ("Relationships & family", ["autistic-parent-support-uk", "communication-needs-in-relationships", "neurodivergent-parent-overwhelmed-by-admin"]),
    ("Money & administration", ["disability-benefits-where-start-uk"]),
    ("Mobility & travel", ["adhd-driving-dvla-great-britain", "disabled-travel-support-scotland", "disabled-travel-support-wales", "disabled-travel-support-northern-ireland"]),
    ("Information & support", ["autism-information-and-support", "dyslexia-information-and-support-uk", "tourette-information-and-support-uk", "learning-disability-information-and-support-uk", "dld-information-and-support", "adult-dyspraxia-information-uk", "dyscalculia-information-and-support-uk"]),
    ("Games & downtime", ["low-time-pressure-games"]),
]
FEATURED_QUESTION_IDS = [
    "task-starting-and-organisation", "reasonable-adjustments-at-work-great-britain",
    "disabled-student-support-england", "dld-information-and-support", "low-time-pressure-games",
    "autism-information-and-support", "autism-anxiety-tools",
]
V07_HOMEPAGE_COMPAT_QUESTION_IDS = (
    "task-starting-and-organisation", "low-time-pressure-games", "workplace-support-great-britain",
    "autism-information-and-support", "autism-anxiety-tools",
)
for _qid in V07_HOMEPAGE_COMPAT_QUESTION_IDS:
    if _qid not in FEATURED_QUESTION_IDS:
        FEATURED_QUESTION_IDS.append(_qid)

HUB_DEFINITIONS = [
    ("needs/daily-life", "Daily life", "Start with practical everyday tasks: getting started, routines, technology, planning and ordinary activities.", {"Daily life & technology", "Games & downtime"}),
    ("needs/sensory-environment", "Sensory & environment", "Find governed routes about sensory load, noisy or bright places, overload and changing the environment around a person.", {"Sensory & environment"}),
    ("needs/communication", "Communication", "Find routes for phone calls, processing time, speaking, AAC and communication access without assuming one communication style fits everyone.", {"Communication"}),
    ("needs/work", "Work", "Find workplace support, adjustments, disclosure, interviews, job-search support and Access to Work routes.", {"Work"}),
    ("needs/education-study", "Education & study", "Find study organisation, disabled-student support, SEND information and education access routes.", {"Education & study"}),
    ("needs/assessment-diagnosis", "Assessment & diagnosis", "Find bounded information about assessment and diagnosis routes without turning ND Oracle into a diagnostic test.", {"Assessment & diagnosis"}),
    ("needs/health-wellbeing", "Health & wellbeing", "Find current routes around anxiety, sleep, food-related task demands, burnout, healthcare access and wellbeing while keeping clinical boundaries visible.", {"Health & wellbeing"}),
    ("needs/relationships-family", "Relationships & family", "Find routes relevant to family life, parenting and relationships where the present catalogue has governed material.", {"Relationships & family"}),
]
NAVIGATION_ROUTES = (
    "/needs/", "/needs/daily-life/", "/needs/sensory-environment/", "/needs/communication/",
    "/needs/work/", "/needs/education-study/", "/needs/assessment-diagnosis/",
    "/needs/health-wellbeing/", "/needs/relationships-family/", "/types/", "/places/", "/a-z/",
)

QUESTION_DISCOVERY_HOW_SECTION = (
    '<section><h2>Question-led discovery</h2><p>Practical question pages route an ordinary need across already governed topics and resources. '
    'They show the current bounded synthesis, what is relevant to inspect, what evidence is still missing, where people may disagree and what should cause the answer to be revisited.</p>'
    '<p>A question route is not a personalised recommendation and does not turn a resource listing into proof that it works.</p></section>'
)
QUESTION_DISCOVERY_ABOUT_SECTION = (
    '<section><h2>Start with the problem, not the taxonomy</h2><p>Question-led discovery lets a reader begin with an everyday problem and then move into the governed topics and resources behind the answer. '
    'The question page remains a route through the knowledge commons rather than a new source of authority.</p></section>'
)
FIND_HOW_SECTION = (
    '<section><h2>Governed discovery</h2><p>The <a href="/find/">Find</a> tool uses deterministic local text and editorial-intent matching. '
    'It can rank governed routes, but it cannot create a new fact, diagnose a person or convert relevance into a recommendation. '
    'If no route clears the threshold, it says that the catalogue does not have a governed answer yet.</p></section>'
)
FIND_PRIVACY_SECTION = (
    '<section><h2>Local discovery privacy</h2><p>The /find/ tool ranks the static governed catalogue in your browser. Query text is not submitted in a URL, sent to an AI or search service, stored by ND Oracle, or used for analytics. The page itself and its local script are served like other static site files.</p></section>'
)

STATIC_PAGES = {
    "how-it-works": {
        "title": "How this site works",
        "intro": "Start with what is useful. Open the evidence, uncertainty and provenance only when you want the deeper route.",
        "body": (
            "<section><h2>Useful first</h2><p>The public pages are written for people, not for navigating an internal database. Topics start with a deliberately simple explanation. Resources start with what they are, what they are for and what might make them a poor fit.</p></section>"
            '<section id="confidence"><h2>What the confidence labels mean</h2><p>A confidence label applies only to the exact statement beside it. It is not a score for a whole topic, person or source, and high confidence does not mean certainty.</p>'
            '<dl class="confidence-key"><dt>High</dt><dd>The bounded statement has strong, consistent support from the evidence used for it, with no known disagreement large enough to change the statement substantially.</dd><dt>Moderate</dt><dd>The statement is supported, but important limits, narrower evidence, transfer problems or remaining uncertainty mean it should be read with more caution.</dd><dt>Low</dt><dd>The statement has some support but the evidence is limited, indirect or fragile. Treat it as provisional.</dd><dt>Contested</dt><dd>Credible evidence or perspectives materially disagree. The label preserves that disagreement rather than forcing a false consensus.</dd><dt>Not applicable</dt><dd>An epistemic confidence score is not the right description for that statement; this must not be used merely to avoid assessing evidence.</dd></dl></section>'
            '<section><h2>Being listed is not being endorsed</h2><p>Tools, games, books, services and organisations are catalogued so you can judge them. Existence, popularity and marketing are not evidence that something works. Commercial interests, costs and known limitations stay visible. Any efficacy or safety claim needs its own governed evidence route.</p></section>'
            '<section><h2>Uncertainty stays visible</h2><p>If an important question is unresolved, the site keeps it unresolved. The aim is to save the next person from having to rediscover the same gap.</p></section>'
            '<section><h2>Evidence is inspectable</h2><p>Evidence links sit behind the statements they support. Source details and provenance remain available without dominating the first read.</p></section>'
            '<section><h2>Review dates are visible</h2><p>Pages show when their current record was last reviewed. A review date is not a promise that nothing newer exists; it tells you how fresh this site\'s review is.</p></section>'
            '<section><h2>This is not a diagnosis service</h2><p>The site is for understanding, practical discovery and research traceability. It does not diagnose individuals or replace appropriate clinical, legal, educational or safeguarding judgement.</p></section>'
            + QUESTION_DISCOVERY_HOW_SECTION + FIND_HOW_SECTION
        ), "indexable": True,
    },
    "about": {
        "title": "About",
        "intro": "Useful neurodiversity information is scattered across research, guidance, communities, tools, games and everyday experience. ND Oracle brings those routes together without hiding where they came from.",
        "body": (
            '<section><h2>What it is for</h2><p>You should not have to repeat the same research every time you need to understand a term, find a tool, check a service or work out whether a resource might suit you. ND Oracle keeps useful material connected to its evidence, limitations, disagreement and review state.</p></section>'
            '<section><h2>More than a diagnosis encyclopaedia</h2><p>The project covers the wider neurodiversity ecosystem: concepts, practical tools, apps, games, books and media, services, organisations, communities and accommodations. Sections become public when they contain useful reviewed material rather than appearing as empty promises.</p></section>'
            '<section><h2>Provenance first</h2><p>Underneath the simple reading layer is a provenance-first knowledge commons. That means a serious claim keeps its route back to evidence and uncertainty, while a resource listing stays distinct from an endorsement.</p></section>'
            '<section><h2>What it is not</h2><p>It is not a diagnosis engine, a treatment marketplace, an AI authority or a replacement for professional judgement.</p></section>'
            + QUESTION_DISCOVERY_ABOUT_SECTION
        ), "indexable": True,
    },
    "accessibility": {
        "title": "Accessibility", "intro": "The site is designed to reduce cognitive and sensory burden rather than add to it.",
        "body": '<section><h2>Current approach</h2><p>The site uses semantic HTML, visible keyboard focus, restrained colours, a reading-width content column and no required JavaScript for core navigation or reading.</p><p>Evidence and provenance use native disclosure controls so readers can choose depth without losing keyboard access.</p></section><section><h2>Accessibility problems are defects</h2><p>Interactive features must preserve keyboard access, reduced-motion preferences, readable language and a usable no-script baseline wherever practical.</p><p>If something here is difficult to use, <a href="/feedback/">report the accessibility problem</a>.</p></section>',
        "indexable": True,
    },
    "privacy": {
        "title": "Privacy", "intro": "The current public site is designed to collect no personal data.",
        "body": '<section><h2>Current release</h2><p>There are no accounts, analytics scripts, advertising trackers or personalised profiles in the generated site.</p><p>The feedback page links to the public GitHub issue tracker; following that link leaves this site and uses GitHub\'s service.</p></section><section><h2>External resources</h2><p>Resource pages can link to third-party websites and services. Following those links leaves ND Oracle and the destination\'s own privacy terms apply.</p></section><section><h2>Future features</h2><p>Anything that stores queries, profiles, health information or community submissions requires a separate privacy and threat-model review before release.</p></section>' + FIND_PRIVACY_SECTION,
        "indexable": True,
    },
    "feedback": {
        "title": "Feedback", "intro": "Found something inaccessible, unclear, outdated or broken? You can report it without adding tracking or a form to this site.",
        "body": '<section><h2>Report a problem</h2><p>Use the public ND Oracle issue tracker for accessibility problems, factual concerns, confusing wording, broken links or other defects. Please do not include private health information, contact details or anything else you would not want published.</p><p><a href="https://github.com/armpitpete/nd-oracle/issues/new" rel="noopener noreferrer">Open the public issue tracker</a></p></section><section><h2>What helps</h2><ul><li>The page address.</li><li>What you expected to happen.</li><li>What actually happened or what was difficult to understand.</li><li>For an evidence concern, the exact statement you think needs checking.</li></ul></section><section class="notice"><h2>Current limitation</h2><p>This release does not yet offer a private feedback channel. If the public GitHub route is itself inaccessible to you, that is a known limitation rather than a reason to treat the problem as resolved.</p></section>',
        "indexable": True,
    },
    "oracle": {
        "title": "Oracle", "intro": "The deeper provenance system is the foundation of these pages, not a chatbot presented as an authority.",
        "body": '<p>The current public interface exposes reviewed knowledge through topic, resource and governed question pages. Generated answers are not the source of truth. <a href="/questions/">Start with a governed question</a> or <a href="/how-it-works/">see how the evidence route works</a>.</p>',
        "indexable": False,
    },
}
INDEXED_STATIC_PAGES = tuple(slug for slug, page in STATIC_PAGES.items() if page.get("indexable", True))


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
    return date.fromisoformat(value).strftime("%d %B %Y").lstrip("0")


def _load_json_dir(path: Path, sort_key: str) -> list[dict]:
    items = []
    if not path.is_dir():
        return items
    for file in sorted(path.glob("*.json")):
        items.append(json.loads(file.read_text(encoding="utf-8")))
    return sorted(items, key=lambda x: str(x[sort_key]).casefold())


def load_concepts() -> list[dict]: return _load_json_dir(OBJECTS_DIR, "name")
def load_resources() -> list[dict]: return _load_json_dir(RESOURCES_DIR, "name")
def load_questions() -> list[dict]: return _load_json_dir(QUESTIONS_DIR, "question")
def load_evidence() -> list[dict]: return _load_json_dir(EVIDENCE_DIR, "title")


def validate_reading_layer(concepts: list[dict]) -> None:
    ids = {c["id"] for c in concepts}
    if set(SIMPLE_EXPLANATIONS) != ids:
        raise ValueError(f"Public-reading explanation set must exactly match authoritative concepts: missing={sorted(ids-set(SIMPLE_EXPLANATIONS))}; unexpected={sorted(set(SIMPLE_EXPLANATIONS)-ids)}")
    qids = [cid for _q, cid in COMMON_QUESTIONS]
    if set(qids) != ids or len(qids) != len(ids):
        raise ValueError("Homepage question set must provide exactly one route for every authoritative concept")


def validate_question_navigation(questions: list[dict]) -> None:
    ids = {q["id"] for q in questions}; grouped = [qid for _g, values in QUESTION_GROUPS for qid in values]
    if len(grouped) != len(set(grouped)): raise ValueError("Question navigation groups contain duplicate question IDs")
    if set(grouped) != ids: raise ValueError(f"Question navigation groups must exactly cover current Questions: missing={sorted(ids-set(grouped))}; unexpected={sorted(set(grouped)-ids)}")
    if len(FEATURED_QUESTION_IDS) != len(set(FEATURED_QUESTION_IDS)) or not set(FEATURED_QUESTION_IDS) <= ids: raise ValueError("Featured questions must be unique current Question IDs")


def reader_intro(concept: dict) -> str: return SIMPLE_EXPLANATIONS[concept["id"]]
def list_items(values: list[str]) -> str:
    return '<p class="meta">None recorded.</p>' if not values else "<ul>" + "".join(f"<li>{esc(v)}</li>" for v in values) + "</ul>"

def nav(current: str | None = None) -> str:
    return '<nav class="primary-nav" aria-label="Primary">' + "".join(f'<a href="/{slug}/"{" aria-current=\"page\"" if slug==current else ""}>{esc(label)}</a>' for slug, label in PRIMARY_NAV) + "</nav>"


def page_shell(title: str, intro: str, body: str, *, current: str | None = None, path: str | None = None, indexable: bool = True) -> str:
    canonical = f'  <link rel="canonical" href="{esc(PUBLIC_ORIGIN + path)}">\n' if path is not None else ""
    robots = "" if indexable else '  <meta name="robots" content="noindex, follow">\n'
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="color-scheme" content="light">
  <meta name="theme-color" content="#f4f1ea">
  <meta name="description" content="{esc(intro)}">
{robots}{canonical}  <title>{esc(title)} · The Neurodiverse Oracle</title>
  <link rel="stylesheet" href="/styles.css">
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header"><div class="site-shell header-row"><a class="site-name" href="/">The Neurodiverse Oracle</a>{nav(current)}</div></header>
<main id="main" class="site-shell reading-column"><header class="page-heading"><h1>{esc(title)}</h1><p class="lede">{esc(intro)}</p></header>{body}</main>
<footer class="site-footer"><div class="site-shell footer-row"><span>Useful first. Evidence when you want it.</span><nav aria-label="Footer"><a href="/resources/">Resources</a><a href="/how-it-works/">How it works</a><a href="/accessibility/">Accessibility</a><a href="/feedback/">Feedback</a><a href="/privacy/">Privacy</a></nav></div></footer>
</body>
</html>
'''


def topic_link(c: dict) -> str: return f'<article class="topic-row"><h2><a href="/understand/{esc(c["id"])}/">{esc(c["name"])}</a></h2><p>{esc(reader_intro(c))}</p></article>'
def question_link(q: dict) -> str: return f'<article class="topic-row"><h3><a href="/questions/{esc(q["id"])}/">{esc(q["question"])}</a></h3><p>{esc(q["why_it_matters"])}</p></article>'
def resource_link(r: dict) -> str:
    category = RESOURCE_CATEGORY_LABELS.get(r["category"], r["category"].replace("_", " ").title())
    return f'<article class="resource-row"><div class="resource-row-head"><h3><a href="/resources/{esc(r["id"])}/">{esc(r["name"])}</a></h3><span class="resource-kind">{esc(category)}</span></div><p>{esc(r["description"])}</p><p class="meta">For: {esc(r["audience_or_context"])}</p></article>'

def render_index(concepts: list[dict], resources: list[dict], questions: list[dict] | None = None) -> str:
    if questions is None: questions = load_questions()
    validate_question_navigation(questions); c_map={c["id"]:c for c in concepts}; q_map={q["id"]:q for q in questions}
    question_links="".join(f'<li><a href="/understand/{esc(cid)}/">{esc(q)}</a></li>' for q,cid in COMMON_QUESTIONS if cid in c_map)
    practical="".join(f'<li><a href="/questions/{esc(qid)}/">{esc(q_map[qid]["question"])}</a></li>' for qid in FEATURED_QUESTION_IDS)
    counts=Counter(r["category"] for r in resources); tools=sum(counts[x] for x in TOOL_CATEGORIES); games=counts["game"]; community=sum(counts[x] for x in COMMUNITY_CATEGORIES); books=sum(counts[x] for x in BOOK_MEDIA_CATEGORIES)
    body=f'''<section class="start-section" aria-labelledby="practical-question-heading"><h2 id="practical-question-heading">Start with something you need to do</h2><p class="section-intro">These are governed routes across the current catalogue. They identify things worth inspecting without pretending one answer fits everyone.</p><ul class="question-list">{practical}</ul><p><a href="/questions/">Browse all {len(questions)} practical questions →</a></p></section>
<section class="start-section" aria-labelledby="start-heading"><h2 id="start-heading">Start with a question</h2><p class="section-intro">Choose the question closest to what you are trying to understand. Every current topic has a route from here.</p><ul class="question-list">{question_links}</ul></section>
<section class="ecosystem-callout" aria-labelledby="explore-heading"><h2 id="explore-heading">Explore useful things</h2><p class="section-intro">ND Oracle is more than explanations. Browse reviewed tools, apps, games, books, services and organisations. A listing is not an endorsement: limitations, costs and commercial interests stay visible.</p><div class="entry-grid"><a class="entry-card" href="/tools/"><strong>Tools &amp; practical help</strong><span>{tools} current entries</span></a><a class="entry-card" href="/games/"><strong>Games</strong><span>{games} current entries</span></a><a class="entry-card" href="/books-media/"><strong>Books &amp; media</strong><span>{books} current entries</span></a><a class="entry-card" href="/community/"><strong>Support &amp; organisations</strong><span>{community} current entries</span></a><a class="entry-card" href="/resources/"><strong>Everything</strong><span>{len(resources)} reviewed resources</span></a></div></section>
<section aria-labelledby="topics-heading"><div class="section-heading-row"><div><h2 id="topics-heading">Browse current topics</h2><p class="section-intro">{len(concepts)} evidence-linked topics are available now.</p></div><a class="quiet-link" href="/understand/">See all topics</a></div><div class="topic-list">{"".join(topic_link(c) for c in concepts)}</div></section>
<section class="start-section" aria-labelledby="browse-whole-heading"><h2 id="browse-whole-heading">Browse the whole knowledge base</h2><p class="section-intro">Use needs, content type, geographic scope or the complete A–Z when you do not want to start from a diagnosis.</p><ul class="question-list"><li><a href="/needs/">Browse by need</a></li><li><a href="/types/">Browse by content type</a></li><li><a href="/places/">Browse by geographic scope</a></li><li><a href="/a-z/">A–Z of all governed content</a></li></ul></section>
<section class="start-section" aria-labelledby="find-oracle-heading"><h2 id="find-oracle-heading">Describe the problem in your own words</h2><p>Use local governed discovery when you do not know the name of the Topic, Question or Resource you need.</p><p><a href="/find/">Find a governed route →</a></p></section>
<section class="reading-guide" aria-labelledby="guide-heading"><h2 id="guide-heading">Choose how deep to go</h2><div class="guide-grid"><div><strong>Read the simple version</strong><p>Topic pages start with a short explanation written for a first read.</p></div><div><strong>Judge practical resources</strong><p>Resource pages show intended use, limitations, access and conflicts rather than hiding them behind a recommendation score.</p></div><div><strong>Check the reasoning</strong><p>Where a serious claim is made, evidence and uncertainty remain inspectable.</p></div></div><p><a href="/how-it-works/">How evidence, confidence, uncertainty and resource listings work →</a></p></section>'''
    return page_shell("Understand neurodivergence without doing all the digging yourself", "Start with an ordinary question, find practical resources, and inspect evidence or uncertainty only when you want to go deeper.", body, path="/")


def render_understand_index(concepts: list[dict]) -> str:
    return page_shell("Understand", "Plain-language topic pages with evidence, uncertainty and different perspectives available without forcing you through them first.", f'<section class="notice"><strong>Orientation, not diagnosis.</strong> These pages explain concepts and preserve their evidence routes. They do not diagnose individuals or replace appropriate professional judgement.</section><section aria-labelledby="concepts-heading"><h2 id="concepts-heading">Current topics</h2><p class="section-intro">There are {len(concepts)} reviewed topic pages. Each starts simply and keeps the deeper evidence route available when you want it.</p><div class="topic-list">{"".join(topic_link(c) for c in concepts)}</div></section>', current="understand", path="/understand/")


def _question_uses_ref(q: dict, kind: str, object_id: str) -> bool: return any(r.get("type")==kind and r.get("id")==object_id for r in q.get("related_objects",[]))
def _question_links_for_ref(questions: list[dict], kind: str, object_id: str) -> str:
    matched=[q for q in questions if _question_uses_ref(q,kind,object_id)]
    return '<p class="meta">No practical question route links here yet.</p>' if not matched else "<ul>"+"".join(f'<li><a href="/questions/{esc(q["id"])}/">{esc(q["question"])}</a></li>' for q in matched)+"</ul>"
def _resource_links_for_concept(resources: list[dict], cid: str) -> str:
    matched=[r for r in resources if any(x.get("type")=="concept" and x.get("id")==cid for x in r.get("related_objects",[]))]
    return '<p class="meta">No reviewed resource link recorded yet.</p>' if not matched else "<ul>"+"".join(f'<li><a href="/resources/{esc(r["id"])}/">{esc(r["name"])}</a> <span class="meta">{esc(RESOURCE_CATEGORY_LABELS.get(r["category"],r["category"].replace("_"," ").title()))}</span></li>' for r in matched)+"</ul>"


def render_concept(concept: dict, concept_map: dict[str, dict], resources: list[dict], questions: list[dict]) -> str:
    source_map={s["id"]:s for s in concept["sources"]}; uncertainty_map={u["id"]:u for u in concept["uncertainties"]}; claims=[]
    for claim in concept["claims"]:
        sources=", ".join(f'<a href="#source-{esc(sid)}">{esc(source_map[sid]["citation"])}</a>' for sid in claim["source_ids"])
        uncertainties=", ".join(f'<a href="#uncertainty-{esc(uid)}">{esc(uncertainty_map[uid]["question"])}</a>' for uid in claim["uncertainty_ids"])
        claims.append(f'<article class="claim" id="claim-{esc(claim["id"])}"><div class="claim-head"><h3>{esc(claim["text"])}</h3><span class="confidence">{esc(claim["confidence"])} confidence</span></div><details class="evidence-detail"><summary>Evidence and uncertainty behind this statement</summary><div class="route"><div><span class="route-label">Evidence:</span> {sources}</div><div><span class="route-label">Uncertainty:</span> {uncertainties}</div></div></details></article>')
    uncertainties="".join(f'<article class="uncertainty" id="uncertainty-{esc(u["id"])}"><h3>{esc(u["question"])}</h3><p>{esc(u["why_it_matters"])}</p><details><summary>What could reduce this uncertainty?</summary>{list_items(u["what_would_reduce_it"])}</details><div class="status">Status: {esc(u["status"])}</div></article>' for u in concept["uncertainties"])
    perspectives="".join(f'<article class="perspective"><h3>{esc(p["held_by"])}</h3><p>{esc(p["summary"])}</p><div class="meta">Evidence: {", ".join(f"<a href=\"#source-{esc(sid)}\">{esc(source_map[sid][\"citation\"])}</a>" for sid in p["source_ids"])}</div></article>' for p in concept["perspectives"])
    sources=[]
    for source in concept["sources"]:
        url=safe_http_url(source.get("url")); link=f'<a href="{esc(url)}" rel="noopener noreferrer">Open source</a>' if url else "No safe public URL recorded"
        sources.append(f'<article class="source" id="source-{esc(source["id"])}"><h3>{esc(source["citation"])}</h3><div class="meta">Kind: {esc(source["kind"])} · accessed {esc(source["accessed"])}</div><p>{link}</p></article>')
    relations="".join(f'<li><a href="/understand/{esc(r["target_id"])}/">{esc(concept_map[r["target_id"]]["name"])}</a> — {esc(r["note"])}</li>' for r in concept["relations"])
    reviewed=human_date(concept["provenance"].get("last_reviewed")); next_routes=f'<section aria-labelledby="next-routes-heading"><h2 id="next-routes-heading">Useful next routes</h2><h3>Practical questions</h3>{_question_links_for_ref(questions,"concept",concept["id"])}<h3>Related resources</h3>{_resource_links_for_concept(resources,concept["id"])}</section>'
    body=f'<p class="back-link"><a href="/understand/">← All topics</a></p><p class="review-meta">Last reviewed: <strong>{esc(reviewed)}</strong></p><details class="technical-summary"><summary>More precise description</summary><p>{esc(concept["summary"])}</p></details><section class="at-a-glance" aria-labelledby="glance-heading"><h2 id="glance-heading">At a glance</h2><div class="scope-grid"><div><h3>This page covers</h3>{list_items(concept["scope"]["includes"])}</div><div><h3>It does not mean</h3>{list_items(concept["scope"]["excludes"])}</div></div></section><section aria-labelledby="known-heading"><h2 id="known-heading">What we can say</h2><p class="section-intro">These are bounded statements from the current evidence record. <a href="/how-it-works/#confidence">See what the confidence labels mean</a>. Open a statement only if you want its evidence route.</p>{"".join(claims)}</section><section aria-labelledby="uncertainty-heading"><h2 id="uncertainty-heading">What remains uncertain</h2>{uncertainties}</section><section aria-labelledby="perspectives-heading"><h2 id="perspectives-heading">Different perspectives</h2>{perspectives}</section><section aria-labelledby="related-heading"><h2 id="related-heading">Related topics</h2><ul>{relations}</ul></section>{next_routes}<section aria-labelledby="sources-heading"><h2 id="sources-heading">Sources</h2>{"".join(sources)}</section><details class="provenance"><summary>Page provenance and review state</summary><p>{esc(concept["provenance"]["method"])}</p><div class="meta">Created {esc(concept["provenance"]["created"])} · last reviewed {esc(reviewed)} · review state {esc(concept["provenance"]["review_state"])}</div></details>'
    return page_shell(concept["name"], reader_intro(concept), body, current="understand", path=f'/understand/{concept["id"]}/')


def render_resource_collection(resources: list[dict], *, title: str, intro: str, route: str, categories: set[str] | None = None) -> str:
    selected=[r for r in resources if categories is None or r["category"] in categories]
    subnav='<nav class="resource-subnav" aria-label="Browse resources"><a href="/resources/">All resources</a><a href="/tools/">Tools &amp; practical help</a><a href="/games/">Games</a><a href="/books-media/">Books &amp; media</a><a href="/community/">Support &amp; organisations</a></nav>'
    body=f'<section class="notice"><strong>Listed, not endorsed.</strong> Inclusion means the resource was identified, checked and described. It does not mean ND Oracle has proved that it works or that it will suit you.</section>{subnav}<section aria-labelledby="resource-list-heading"><h2 id="resource-list-heading">{len(selected)} reviewed {"entry" if len(selected)==1 else "entries"}</h2><div class="resource-list">{"".join(resource_link(r) for r in selected)}</div></section>'
    return page_shell(title,intro,body,current="resources",path=f"/{route}/")
def render_resources_index(resources: list[dict]) -> str: return render_resource_collection(resources,title="Resources",intro="Tools, practical guides, games, books, services and organisations, described with their limitations and access conditions visible.",route="resources")
def render_books_media_index(resources: list[dict]) -> str: return render_resource_collection(resources,title="Books & media",intro="Reviewed books and media in the ND Oracle catalogue, with context, limitations and conflicts kept visible.",route="books-media",categories=BOOK_MEDIA_CATEGORIES)

def resource_access_links(resource: dict) -> str:
    links=[]
    for l in resource.get("locators",[]):
        if l.get("type")=="url" and safe_http_url(l.get("value")): links.append(f'<li><a href="{esc(l["value"])}" rel="noopener noreferrer">Visit official resource</a></li>')
        elif l.get("type")!="url": links.append(f'<li>{esc(l.get("type"))}: {esc(l.get("value"))}</li>')
    return "<ul>"+"".join(links)+"</ul>"

def resource_scope(resource: dict) -> tuple[str,str]:
    audience=str(resource.get("audience_or_context","")).casefold(); whole=" ".join([str(resource.get("description","")),audience,*map(str,resource.get("limitations",[]))]).casefold()
    if "great britain" in audience or "england, scotland and wales" in audience: return "Great Britain","The reviewed scope identifies Great Britain (England, Scotland and Wales); Northern Ireland may use a different system."
    if ("england or wales" in audience or "england and wales" in audience) and "scotland" not in audience: return "England and Wales","The reviewed scope specifically identifies England and Wales."
    if "northern ireland" in audience and all(x not in audience for x in ("england","scotland","wales")): return "Northern Ireland","The reviewed scope specifically identifies Northern Ireland."
    if "scotland" in audience and all(x not in audience for x in ("england","wales","northern ireland")): return "Scotland","The reviewed scope specifically identifies Scotland."
    if "wales" in audience and all(x not in audience for x in ("england","scotland","northern ireland")): return "Wales","The reviewed scope specifically identifies Wales."
    if "england" in audience and all(x not in audience for x in ("scotland","wales","northern ireland")): return "England","The reviewed scope specifically identifies England."
    if "united kingdom" in audience or " uk " in f" {audience} " or "uk-wide" in whole: return "United Kingdom","The reviewed listing describes a UK-wide or United Kingdom scope."
    return "International / not jurisdiction-specific","No narrower UK jurisdiction is asserted by the reviewed scope; check the resource itself for local availability and eligibility."

def _evidence_contribution(e: dict, ref: str) -> dict | None: return next((x for x in e.get("contributions",[]) if x.get("claim_ref")==ref),None)
def render_governed_resource_claims(resource: dict, evidence_map: dict[str,dict]) -> str:
    if not resource.get("claims"): return ""
    rows=[]
    for claim in resource["claims"]:
        ref=f'{resource["id"]}#{claim["id"]}'; erows=[]
        for eid in claim.get("evidence_ids",[]):
            e=evidence_map[eid]; contribution=_evidence_contribution(e,ref)
            if contribution is None: raise ValueError(f"{eid}: missing contribution for {ref}")
            loc=e.get("locator",{}); url=loc.get("value") if loc.get("type")=="url" else None; citation=esc(e["citation"])
            if url and safe_http_url(url): citation=f'<a href="{esc(url)}">{citation}</a>'
            erows.append(f'<article class="evidence-card"><h4>{esc(e["title"])}</h4><p>{citation}</p><p><strong>Finding used here:</strong> {esc(contribution["finding"])}</p><p class="meta">Context: {esc(contribution["population_or_context"])} · Method: {esc(contribution["methodology"])}</p><div><strong>Evidence limitations</strong>{list_items([x["text"] for x in contribution.get("limitations",[])])}</div></article>')
        urows="".join(f'<li id="uncertainty-{esc(u["id"])}"><strong>{esc(u["text"])}</strong><br><span class="meta">Why it matters: {esc(u["why_it_matters"])}</span></li>' for u in claim.get("uncertainties",[]))
        rows.append(f'<article class="claim-card" id="claim-{esc(claim["id"])}"><h3>{esc(claim["text"])}</h3><p class="meta">Confidence: <a href="/how-it-works/#confidence">{esc(claim["confidence"].replace("_"," ").title())}</a></p><h4>Evidence route</h4>{"".join(erows)}<h4>Uncertainty and limits</h4><ul>{urows}</ul></article>')
    return '<section aria-labelledby="governed-resource-claims-heading"><h2 id="governed-resource-claims-heading">Governed claims and evidence</h2><section class="notice"><strong>A supported claim is not a recommendation or an individual decision.</strong> Read the exact wording, evidence context and open uncertainty together.</section>'+"".join(rows)+"</section>"

def render_resource(resource: dict, concept_map: dict[str,dict], questions: list[dict], evidence_map: dict[str,dict] | None=None) -> str:
    if evidence_map is None: evidence_map={e["id"]:e for e in load_evidence()}
    category=RESOURCE_CATEGORY_LABELS.get(resource["category"],resource["category"].replace("_"," ").title()); related=[]
    for ref in resource.get("related_objects",[]):
        if ref.get("type")=="concept" and ref.get("id") in concept_map: related.append(f'<li><a href="/understand/{esc(ref["id"])}/">{esc(concept_map[ref["id"]]["name"])}</a></li>')
    reviewed=human_date(resource["provenance"].get("last_reviewed")); qlinks=_question_links_for_ref(questions,"resource",resource["id"]); label,explanation=resource_scope(resource); claims=render_governed_resource_claims(resource,evidence_map)
    claim_note="This resource currently has governed claim records. Open those claims only when their evidence routes are available." if resource.get("claims") else "This listing makes no efficacy or safety claim. It records what the resource is, what it is for, how to reach it and what limitations are already known."
    body=f'<p class="back-link"><a href="/resources/">← All resources</a></p><div class="resource-meta"><span class="resource-kind">{esc(category)}</span><span>Last reviewed: <strong>{esc(reviewed)}</strong></span></div><section class="notice"><strong>Listed, not endorsed.</strong> ND Oracle is helping you inspect this resource, not telling you that it will work for you.</section><section aria-labelledby="use-heading"><h2 id="use-heading">What it is for</h2><p>{esc(resource["intended_use"])}</p></section><section aria-labelledby="audience-heading"><h2 id="audience-heading">Who or what context</h2><p>{esc(resource["audience_or_context"])}</p></section><section aria-labelledby="access-heading"><h2 id="access-heading">Access</h2>{resource_access_links(resource)}</section><section aria-labelledby="related-heading"><h2 id="related-heading">Related topics</h2>{"<ul>"+"".join(related)+"</ul>" if related else "<p class=\"meta\">No topic link recorded yet.</p>"}</section><section aria-labelledby="resource-question-heading"><h2 id="resource-question-heading">Questions that lead here</h2>{qlinks}</section><section aria-labelledby="scope-heading"><h2 id="scope-heading">Scope for navigation</h2><p><strong>{esc(label)}</strong> · {esc(category)}</p><p class="meta">{esc(explanation)} This label helps navigation; it is not an eligibility or legal determination.</p><p><a href="/places/">Browse resources by place</a> · <a href="/types/">Browse by content type</a></p></section>{claims}<section aria-labelledby="limits-heading"><h2 id="limits-heading">Limitations and possible poor fit</h2>{list_items(resource["limitations"])}</section><section aria-labelledby="cost-heading"><h2 id="cost-heading">Cost and access notes</h2>{list_items(resource["cost_or_access_notes"])}</section><section aria-labelledby="conflict-heading"><h2 id="conflict-heading">Ownership and conflicts</h2>{list_items(resource["conflicts_of_interest"])}</section><section class="evidence-status" aria-labelledby="evidence-status-heading"><h2 id="evidence-status-heading">Evidence status</h2><p>{esc(claim_note)}</p></section><details class="provenance"><summary>Page provenance and review state</summary><p>{esc(resource["provenance"]["method"])}</p><div class="meta">Created {esc(resource["provenance"]["created"])} · last reviewed {esc(reviewed)} · review state {esc(resource["provenance"]["review_state"])}</div></details>'
    return page_shell(resource["name"],resource["description"],body,current="resources",path=f'/resources/{resource["id"]}/')

def _related_question_items(question: dict, concept_map: dict[str,dict], resource_map: dict[str,dict], question_map: dict[str,dict]) -> str:
    items=[]
    for ref in question["related_objects"]:
        kind,oid=ref["type"],ref["id"]
        if kind=="concept" and oid in concept_map: items.append(f'<li><a href="/understand/{esc(oid)}/">{esc(concept_map[oid]["name"])}</a> <span class="meta">Topic</span></li>')
        elif kind=="resource" and oid in resource_map: items.append(f'<li><a href="/resources/{esc(oid)}/">{esc(resource_map[oid]["name"])}</a> <span class="meta">{esc(RESOURCE_CATEGORY_LABELS.get(resource_map[oid]["category"],resource_map[oid]["category"].replace("_"," ").title()))}</span></li>')
        elif kind=="question" and oid in question_map: items.append(f'<li><a href="/questions/{esc(oid)}/">{esc(question_map[oid]["question"])}</a> <span class="meta">Question</span></li>')
        else: raise ValueError(f"{question['id']}: missing/unsupported related object {kind}:{oid}")
    return "<ul>"+"".join(items)+"</ul>"
def related_questions(question: dict, questions: list[dict], limit: int=5) -> list[dict]:
    refs={(r.get("type"),r.get("id")) for r in question.get("related_objects",[])}; ranked=[]
    for candidate in questions:
        if candidate["id"]==question["id"]: continue
        score=len(refs & {(r.get("type"),r.get("id")) for r in candidate.get("related_objects",[])})
        if score: ranked.append((-score,candidate["question"].casefold(),candidate))
    ranked.sort(key=lambda x:(x[0],x[1])); return [x[2] for x in ranked[:limit]]
def render_question(question: dict, concept_map: dict[str,dict], resource_map: dict[str,dict], questions: list[dict]|None=None) -> str:
    if questions is None: questions=load_questions()
    qmap={q["id"]:q for q in questions}; reviewed=human_date(question["provenance"].get("last_reviewed")); status=question["status"].replace("_"," ").capitalize(); related=_related_question_items(question,concept_map,resource_map,qmap); adjacent=related_questions(question,questions); adjacent_items="".join(f'<li><a href="/questions/{esc(q["id"])}/">{esc(q["question"])}</a></li>' for q in adjacent) or '<li>No adjacent governed question has enough shared material yet.</li>'
    body=f'<p class="back-link"><a href="/questions/">← All questions</a></p><p class="review-meta">Last reviewed: <strong>{esc(reviewed)}</strong> · Status: <strong>{esc(status)}</strong></p><section class="notice"><strong>Relevant to inspect, not recommended.</strong> This is a bounded synthesis of the current governed catalogue, not a personalised recommendation or proof that a listed resource will work for you.</section><section aria-labelledby="current-understanding-heading"><h2 id="current-understanding-heading">Current understanding</h2><p>{esc(question["current_understanding"])}</p></section><section aria-labelledby="related-things-heading"><h2 id="related-things-heading">Related things to inspect</h2>{related}</section><section aria-labelledby="related-questions-heading"><h2 id="related-questions-heading">Related questions</h2><ul>{adjacent_items}</ul></section><section aria-labelledby="evidence-needed-heading"><h2 id="evidence-needed-heading">What evidence is still needed</h2>{list_items(question["evidence_needed"])}</section><section aria-labelledby="dissent-heading"><h2 id="dissent-heading">Where people may disagree</h2>{list_items(question.get("dissent",[]))}</section><section aria-labelledby="reopen-heading"><h2 id="reopen-heading">When this answer should be revisited</h2>{list_items(question["reopening_conditions"])}</section><details class="provenance"><summary>Question provenance and review state</summary><p>{esc(question["provenance"]["method"])}</p><div class="meta">Created {esc(question["provenance"]["created"])} · last reviewed {esc(reviewed)} · review state {esc(question["provenance"]["review_state"])}</div></details>'
    return page_shell(question["question"],question["why_it_matters"],body,current="questions",path=f'/questions/{question["id"]}/')

def render_questions_index(questions: list[dict]) -> str:
    validate_question_navigation(questions); qmap={q["id"]:q for q in questions}; groups=[]
    for name,ids in QUESTION_GROUPS:
        slug=name.lower().replace(" ","-").replace("&","and"); groups.append(f'<section aria-labelledby="question-group-{esc(slug)}"><h2 id="question-group-{esc(slug)}">{esc(name)}</h2><div class="topic-list">{"".join(question_link(qmap[qid]) for qid in ids)}</div></section>')
    body=f'<section class="notice"><strong>Relevant to inspect, not recommended.</strong> These pages route ordinary needs through reviewed ND Oracle material. They do not diagnose you, choose for you or turn a resource listing into an efficacy claim.</section><section aria-labelledby="questions-heading"><h2 id="questions-heading">{len(questions)} governed practical questions</h2><p class="section-intro">Browse by the kind of problem you are trying to solve. Each page keeps the current synthesis, limitations, disagreement and evidence gaps visible.</p></section>{"".join(groups)}<section aria-labelledby="question-browse-heading"><h2 id="question-browse-heading">Other ways to browse</h2><p><a href="/needs/">Browse practical needs and life areas</a> · <a href="/a-z/">A–Z of all content</a></p></section>'
    return page_shell("Questions","Start with an everyday problem and follow a governed route to relevant topics, tools, games, services or organisations.",body,current="questions",path="/questions/")

def _question_map(questions: list[dict]) -> dict[str,dict]: return {q["id"]:q for q in questions}
def _questions_for_groups(questions: list[dict], group_names: set[str]) -> list[dict]:
    qmap=_question_map(questions); return [qmap[qid] for group,ids in QUESTION_GROUPS if group in group_names for qid in ids]
def _linked_content_from_questions(questions: list[dict], concept_map: dict[str,dict], resource_map: dict[str,dict]) -> tuple[list[dict],list[dict]]:
    cids,rids=set(),set()
    for q in questions:
        for ref in q.get("related_objects",[]):
            if ref.get("type")=="concept" and ref.get("id") in concept_map: cids.add(ref["id"])
            if ref.get("type")=="resource" and ref.get("id") in resource_map: rids.add(ref["id"])
    return sorted((concept_map[x] for x in cids),key=lambda x:x["name"].casefold()),sorted((resource_map[x] for x in rids),key=lambda x:x["name"].casefold())
def render_need_hub(route: str,title: str,intro: str,group_names: set[str],questions: list[dict],concept_map: dict[str,dict],resource_map: dict[str,dict]) -> str:
    selected=_questions_for_groups(questions,group_names); concepts,resources=_linked_content_from_questions(selected,concept_map,resource_map); question_rows="".join(question_link(q) for q in selected); concept_rows="".join(f'<li><a href="/understand/{esc(c["id"])}/">{esc(c["name"])}</a></li>' for c in concepts) or "<li>No topic link is recorded yet.</li>"; resource_rows="".join(f'<li><a href="/resources/{esc(r["id"])}/">{esc(r["name"])}</a></li>' for r in resources) or "<li>No resource link is recorded yet.</li>"
    body=f'<p class="back-link"><a href="/needs/">← All needs</a></p><section class="notice"><strong>Relevant to inspect, not recommended.</strong> This hub groups governed routes; it does not infer a diagnosis or choose support for an individual.</section><section aria-labelledby="need-questions-heading"><h2 id="need-questions-heading">Practical questions</h2><div class="topic-list">{question_rows}</div></section><section aria-labelledby="need-topics-heading"><h2 id="need-topics-heading">Related topics</h2><ul>{concept_rows}</ul></section><section aria-labelledby="need-resources-heading"><h2 id="need-resources-heading">Related resources</h2><ul>{resource_rows}</ul></section>'
    return page_shell(title,intro,body,current="questions",path=f"/{route}/")
def render_needs_index(questions: list[dict]) -> str:
    validate_question_navigation(questions); qmap=_question_map(questions); hub_by_group={g:(route,title) for route,title,_intro,groups in HUB_DEFINITIONS for g in groups}; sections=[]
    for group,ids in QUESTION_GROUPS:
        if group in hub_by_group: route,title=hub_by_group[group]; heading=f'<h2><a href="/{esc(route)}/">{esc(title)}</a></h2>'
        else: heading=f'<h2>{esc(group)}</h2>'
        links="".join(f'<li><a href="/questions/{esc(qid)}/">{esc(qmap[qid]["question"])}</a></li>' for qid in ids); sections.append(f'<section>{heading}<ul>{links}</ul></section>')
    return page_shell("Browse by need","Start from the problem or life area you are dealing with, then follow governed questions into topics and resources.",'<section class="notice"><strong>Start with the need, not the label.</strong> Every current governed Question appears here exactly once in its primary navigation group.</section>'+"".join(sections),current="questions",path="/needs/")
def render_types_index(concepts: list[dict],resources: list[dict],questions: list[dict]) -> str:
    sections=[f'<section><h2>Questions</h2><p>{len(questions)} governed practical questions.</p><p><a href="/questions/">Browse Questions</a></p></section>',f'<section><h2>Topics</h2><p>{len(concepts)} reviewed Concepts.</p><p><a href="/understand/">Browse Topics</a></p></section>']; grouped=defaultdict(list)
    for r in resources: grouped[r["category"]].append(r)
    for category in ["organisation","service","community","tool","app","practical_guide","education_work_resource","accommodation","game","book","media","product","other"]:
        items=sorted(grouped.get(category,[]),key=lambda x:x["name"].casefold())
        if items:
            label=RESOURCE_CATEGORY_LABELS.get(category,category.replace("_"," ").title()); links="".join(f'<li><a href="/resources/{esc(r["id"])}/">{esc(r["name"])}</a></li>' for r in items); sections.append(f'<section><h2>{esc(label)}</h2><ul>{links}</ul></section>')
    return page_shell("Browse by content type","Separate Questions, Topics, organisations, services, tools, apps, games, books, guides and other governed resources.","".join(sections),current="resources",path="/types/")
def render_places_index(resources: list[dict]) -> str:
    grouped,explanations=defaultdict(list),{}
    for resource in resources: label,explanation=resource_scope(resource); grouped[label].append(resource); explanations[label]=explanation
    sections=[]
    for label in ["United Kingdom","Great Britain","England and Wales","England","Scotland","Wales","Northern Ireland","International / not jurisdiction-specific"]:
        items=sorted(grouped.get(label,[]),key=lambda x:x["name"].casefold())
        if items: links="".join(f'<li><a href="/resources/{esc(r["id"])}/">{esc(r["name"])}</a></li>' for r in items); sections.append(f'<section><h2>{esc(label)}</h2><p class="meta">{esc(explanations[label])}</p><ul>{links}</ul></section>')
    body='<section class="notice"><strong>Navigation scope, not eligibility.</strong> These groups come from reviewed audience/scope text. UK-wide, Great Britain, England and Wales, England, Scotland, Wales and Northern Ireland are kept distinct where the governed material supports that distinction.</section>'+"".join(sections)
    return page_shell("Browse by geographic scope","Distinguish national and jurisdiction-specific support instead of treating every UK route as interchangeable.",body,current="resources",path="/places/")
def _az_letter(label: str) -> str: return next((c.upper() for c in label.strip() if c.isalnum()),"#")
def render_az_index(concepts: list[dict],resources: list[dict],questions: list[dict]) -> str:
    entries=[(x["name"],"Topic",f'/understand/{x["id"]}/') for x in concepts]+[(x["name"],"Resource",f'/resources/{x["id"]}/') for x in resources]+[(x["question"],"Question",f'/questions/{x["id"]}/') for x in questions]; grouped=defaultdict(list)
    for entry in sorted(entries,key=lambda x:x[0].casefold()): grouped[_az_letter(entry[0])].append(entry)
    sections=[]
    for letter in sorted(grouped,key=lambda x:(x=="#",x)): links="".join(f'<li><a href="{esc(route)}">{esc(label)}</a> <span class="meta">{esc(kind)}</span></li>' for label,kind,route in grouped[letter]); sections.append(f'<section><h2>{esc(letter)}</h2><ul>{links}</ul></section>')
    return page_shell("A–Z",f"All {len(entries)} governed Topics, Resources and Questions in one alphabetical index.","".join(sections),current="resources",path="/a-z/")

FIND_JS=r'''(() => {
  "use strict";
  const input=document.getElementById("find-input"),button=document.getElementById("find-button"),output=document.getElementById("find-results");
  const index=JSON.parse(document.getElementById("search-index").content.textContent);
  const stop=new Set(["a","an","and","are","can","do","for","i","in","is","it","me","my","of","on","or","the","to","what","with","you","your"]);
  const refusals=["diagnose me","am i autistic","do i have autism","do i have adhd","what medication dose","what dose should i take","stop my medication","which medication should i take","tell me if i am autistic","tell me if i have adhd"];
  const norm=s=>(s||"").toLowerCase().match(/[a-z0-9]+/g)?.join(" ")||"";const tokens=s=>norm(s).split(" ").filter(t=>t.length>1&&!stop.has(t));
  function score(query,record){const qn=norm(query),qt=new Set(tokens(query)),tn=norm(record.title),bn=norm(record.body);let s=0;if(qn===tn)s+=120;else if(tn.includes(qn))s+=55;if(bn.includes(qn))s+=20;const tt=new Set(tokens(record.title)),bt=new Set(tokens(record.body));qt.forEach(t=>{if(tt.has(t))s+=12;if(bt.has(t))s+=3;});(record.intent||[]).forEach(p=>{const pn=norm(p),pt=new Set(tokens(p));if(qn===pn)s+=100;else if(pn.includes(qn)||qn.includes(pn))s+=45;qt.forEach(t=>{if(pt.has(t))s+=9;});});return s;}
  function run(){const query=input.value.trim();output.replaceChildren();if(!query){output.textContent="Type a problem or question first.";return;}const qn=norm(query);if(refusals.some(p=>qn.includes(p))){output.innerHTML='<h2>No governed answer</h2><p>ND Oracle cannot diagnose you, choose medication or make an individual clinical decision. Try browsing <a href="/questions/">Questions</a> or <a href="/needs/">needs</a> instead.</p>';return;}const ranked=index.map(r=>[score(query,r),r]).filter(x=>x[0]>=12).sort((a,b)=>b[0]-a[0]||a[1].kind.localeCompare(b[1].kind)||a[1].title.localeCompare(b[1].title)).slice(0,5);if(!ranked.length){output.innerHTML='<h2>No governed answer yet</h2><p>The current catalogue does not have a strong enough route for that wording. Your query is not stored or sent to a search service. Try <a href="/needs/">browse by need</a>, <a href="/a-z/">A–Z</a>, or report a non-private content gap through <a href="/feedback/">feedback</a>.</p>';return;}const h=document.createElement("h2");h.textContent="Governed routes to inspect";output.appendChild(h);const note=document.createElement("p");note.className="meta";note.textContent="Ranked locally from reviewed ND Oracle content. Relevance is not recommendation.";output.appendChild(note);const list=document.createElement("ol");ranked.forEach(([s,r])=>{const li=document.createElement("li"),a=document.createElement("a"),m=document.createElement("span");a.href=r.route;a.textContent=r.title;li.appendChild(a);m.className="meta";m.textContent=` ${r.kind}`;li.appendChild(m);list.appendChild(li);});output.appendChild(list);}
  button.addEventListener("click",run);input.addEventListener("keydown",e=>{if(e.key==="Enter"){e.preventDefault();run();}});
})();
'''
def render_find_page() -> str:
    index_json=html.escape(discovery.browser_index_json()); body=f'<section class="notice"><strong>Local governed discovery.</strong> Your words stay in this browser page. ND Oracle does not submit the query to a server, AI model, analytics system or search provider.</section><section aria-labelledby="find-heading"><h2 id="find-heading">Describe the problem in your own words</h2><label for="find-input">Problem or question</label><input id="find-input" type="search" autocomplete="off" spellcheck="true" maxlength="500"><button id="find-button" type="button">Find governed routes</button><p class="meta">Examples: “work is too noisy”, “I keep putting off paperwork”, “phone calls are hard”.</p></section><section id="find-results" aria-live="polite" aria-atomic="false"><p>Results will appear here. Relevance means worth inspecting, not recommended.</p></section><noscript><section><h2>Discovery needs JavaScript</h2><p>The rest of ND Oracle works without JavaScript. Use <a href="/questions/">Questions</a>, <a href="/needs/">browse by need</a> or the <a href="/a-z/">A–Z</a> instead.</p></section></noscript><template id="search-index">{index_json}</template><script src="/find.js" defer></script>'
    return page_shell("Find a governed route","Start with ordinary language. Matching happens locally in your browser and points only to governed ND Oracle pages.",body,path="/find/")
def render_static_page(slug: str) -> str:
    page=STATIC_PAGES[slug]; return page_shell(page["title"],page["intro"],page["body"],current=slug if slug in dict(PRIMARY_NAV) else None,path=f"/{slug}/",indexable=page.get("indexable",True))
def render_not_found() -> str:
    body='<section><h2>Try one of these instead</h2><ul class="question-list"><li><a href="/">Go to the homepage</a></li><li><a href="/understand/">Browse current topics</a></li><li><a href="/resources/">Explore tools, games and support</a></li><li><a href="/how-it-works/">See how the site works</a></li><li><a href="/feedback/">Report a broken or confusing page</a></li></ul></section>'
    return page_shell("Page not found","That address does not match a current page, but you can get back to the useful parts of the site here.",body,indexable=False)
def sitemap_paths(concepts: list[dict],resources: list[dict]|None=None,questions: list[dict]|None=None) -> list[str]:
    if resources is None: resources=load_resources()
    if questions is None: questions=load_questions()
    validate_question_navigation(questions); paths=["/","/understand/"]+[f'/understand/{c["id"]}/' for c in concepts]; paths += ["/resources/","/tools/","/games/","/community/","/books-media/"]+[f'/resources/{r["id"]}/' for r in resources]; paths += ["/questions/"]+[f'/questions/{q["id"]}/' for q in questions]; paths += [f'/{slug}/' for slug in INDEXED_STATIC_PAGES]+list(NAVIGATION_ROUTES)+["/find/"]
    if len(paths)!=len(set(paths)): raise ValueError("v1.0 sitemap contains duplicate routes")
    return paths
def render_sitemap(concepts: list[dict],resources: list[dict],questions: list[dict]|None=None) -> str:
    if questions is None: questions=load_questions()
    urls="".join(f"  <url><loc>{html.escape(PUBLIC_ORIGIN+path)}</loc></url>\n" for path in sitemap_paths(concepts,resources,questions)); return '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+urls+'</urlset>\n'
def prepare_output(output_dir: Path) -> None:
    marker=output_dir/".nd-oracle-generated"
    if output_dir.is_symlink(): raise ValueError(f"Refusing to replace symlink output directory: {output_dir}")
    if output_dir.exists():
        if not marker.is_file() or marker.read_text(encoding="utf-8")!=OUTPUT_MARKER: raise ValueError(f"Refusing to replace unmarked output directory: {output_dir}")
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True); marker.write_text(OUTPUT_MARKER,encoding="utf-8")
def write_route(output_dir: Path,route: str,content: str) -> None:
    target=output_dir/route/"index.html"; target.parent.mkdir(parents=True,exist_ok=True); target.write_text(content,encoding="utf-8")
def build(output_dir: Path=DEFAULT_OUTPUT_DIR) -> Path:
    concepts,resources,questions,evidence=load_concepts(),load_resources(),load_questions(),load_evidence()
    if not concepts: raise ValueError("No concept objects found")
    if not questions: raise ValueError("No question objects found")
    validate_reading_layer(concepts); validate_question_navigation(questions); concept_map={c["id"]:c for c in concepts}; resource_map={r["id"]:r for r in resources}; evidence_map={e["id"]:e for e in evidence}; prepare_output(output_dir); shutil.copy2(SITE_DIR/"styles.css",output_dir/"styles.css"); shutil.copy2(SITE_DIR/"_headers",output_dir/"_headers")
    (output_dir/"index.html").write_text(render_index(concepts,resources,questions),encoding="utf-8"); write_route(output_dir,"understand",render_understand_index(concepts)); write_route(output_dir,"resources",render_resources_index(resources)); write_route(output_dir,"tools",render_resource_collection(resources,title="Tools & practical help",intro="Tools, apps, practical guides and products that can make everyday tasks, access, work or study easier to navigate.",route="tools",categories=TOOL_CATEGORIES)); write_route(output_dir,"games",render_resource_collection(resources,title="Games",intro="Games described by play characteristics, pressure, accessibility and possible poor fit — not as treatments or prescriptions.",route="games",categories={"game"})); write_route(output_dir,"community",render_resource_collection(resources,title="Support & organisations",intro="Services, organisations and communities with their scope, geography and limitations kept visible.",route="community",categories=COMMUNITY_CATEGORIES)); write_route(output_dir,"books-media",render_books_media_index(resources)); write_route(output_dir,"questions",render_questions_index(questions))
    for c in concepts: write_route(output_dir,f'understand/{c["id"]}',render_concept(c,concept_map,resources,questions))
    for r in resources: write_route(output_dir,f'resources/{r["id"]}',render_resource(r,concept_map,questions,evidence_map))
    for q in questions: write_route(output_dir,f'questions/{q["id"]}',render_question(q,concept_map,resource_map,questions))
    write_route(output_dir,"needs",render_needs_index(questions))
    for route,title,intro,groups in HUB_DEFINITIONS: write_route(output_dir,route,render_need_hub(route,title,intro,groups,questions,concept_map,resource_map))
    write_route(output_dir,"types",render_types_index(concepts,resources,questions)); write_route(output_dir,"places",render_places_index(resources)); write_route(output_dir,"a-z",render_az_index(concepts,resources,questions)); write_route(output_dir,"find",render_find_page()); (output_dir/"find.js").write_text(FIND_JS,encoding="utf-8")
    for slug in STATIC_PAGES: write_route(output_dir,slug,render_static_page(slug))
    (output_dir/"404.html").write_text(render_not_found(),encoding="utf-8"); paths=sitemap_paths(concepts,resources,questions)
    if len(paths)!=V10_ROUTE_COUNT: raise ValueError(f"Expected {V10_ROUTE_COUNT} v1.0 canonical routes, found {len(paths)}")
    (output_dir/"sitemap.xml").write_text(render_sitemap(concepts,resources,questions),encoding="utf-8"); (output_dir/"robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {PUBLIC_ORIGIN}/sitemap.xml\n",encoding="utf-8"); return output_dir
if __name__=="__main__":
    destination=build(); print(f"Built The Neurodiverse Oracle public site v1.0 candidate at {destination}")
