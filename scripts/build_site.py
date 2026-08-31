from __future__ import annotations

import sys
from pathlib import Path

if __package__ in {None, ''}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

# Generated once from the accepted historical builder layers.
# The current runtime is intentionally a single module with no executable
# historical builder import chain and no cross-module global mutation.
import html
import json
import shutil
from collections import Counter
from datetime import date
from pathlib import Path
from urllib.parse import urlsplit
import sys
from collections import defaultdict
from scripts import discovery

# ---- v06 compatibility foundation ----
_compat06__ROOT = Path(__file__).resolve().parents[1]
_compat06__OBJECTS_DIR = _compat06__ROOT / 'objects' / 'concepts'
_compat06__RESOURCES_DIR = _compat06__ROOT / 'objects' / 'resources'
_compat06__SITE_DIR = _compat06__ROOT / 'site'
_compat06__DEFAULT_OUTPUT_DIR = _compat06__ROOT / 'dist'
_compat06__OUTPUT_MARKER = 'nd-oracle-site-v0.2\n'
_compat06__PUBLIC_ORIGIN = 'https://ndoracle.org'
_compat06__PRIMARY_NAV = [('understand', 'Understand'), ('resources', 'Explore'), ('how-it-works', 'How it works'), ('about', 'About')]
_compat06__RESOURCE_CATEGORY_LABELS = {'tool': 'Tool', 'app': 'App', 'game': 'Game', 'book': 'Book', 'media': 'Media', 'service': 'Service', 'accommodation': 'Accommodation', 'organisation': 'Organisation', 'community': 'Community', 'practical_guide': 'Practical guide', 'product': 'Product', 'education_work_resource': 'Education/work resource', 'other': 'Other'}
_compat06__TOOL_CATEGORIES = {'tool', 'app', 'accommodation', 'practical_guide', 'product', 'education_work_resource'}
_compat06__COMMUNITY_CATEGORIES = {'organisation', 'community', 'service'}
_compat06__SIMPLE_EXPLANATIONS = {'neurodiversity': "People's brains and nervous systems vary. Neurodiversity is a word for that variation, and it is also used when people talk about rights, disability, support and how neurological differences should be understood.", 'autism': 'Autistic people can experience communication, social situations, routines, interests and sensory input differently. Autism looks different from person to person, and support needs can vary.', 'adhd': 'ADHD can affect attention, activity, impulsivity and managing everyday tasks. It can look different between people and situations, and diagnosis needs more than a checklist or a single test.', 'executive-function': 'Executive functions help us hold things in mind, switch attention, pause responses and organise actions towards a goal. Difficulties with them can make starting, planning or finishing tasks hard, but they are not a diagnosis by themselves.', 'sensory-processing': 'People differ in how strongly they notice and respond to sound, light, touch, movement and other sensory input. These differences can affect comfort and everyday life, and they are not unique to one diagnosis.', 'dyslexia': 'Dyslexia mainly affects learning and using word reading and spelling. It can continue into adulthood, and it does not mean that someone has low intelligence.', 'developmental-coordination-disorder': 'Developmental co-ordination disorder (DCD) affects how easily someone learns and carries out coordinated movements. Everyday activities can take more effort, and the difficulties can continue into adulthood.', 'tourette-syndrome': 'Tourette syndrome involves motor and vocal tics that change over time. Swearing is not what defines Tourette syndrome, and support or treatment should depend on what is actually difficult for the person.', 'learning-disability': 'In the UK, a learning disability means lifelong difficulty learning or understanding new information together with difficulty managing everyday life independently. It is not the same thing as a specific learning difficulty such as dyslexia.', 'developmental-language-disorder': 'Developmental language disorder (DLD) is a persistent difficulty understanding and/or using language that affects everyday life. Bilingualism does not cause DLD, and DLD can occur alongside other developmental conditions.'}
_compat06__COMMON_QUESTIONS = [('What does neurodiversity mean?', 'neurodiversity'), ('What is autism?', 'autism'), ('What is ADHD?', 'adhd'), ('Why can starting or organising tasks feel hard?', 'executive-function'), ('Why can sound, light or touch feel intense?', 'sensory-processing'), ('Why can reading or spelling stay difficult?', 'dyslexia'), ('Why can coordination and everyday movement be hard?', 'developmental-coordination-disorder'), ('What are tics and Tourette syndrome?', 'tourette-syndrome'), ('What does learning disability mean in the UK?', 'learning-disability'), ('Why can understanding or using language be difficult?', 'developmental-language-disorder')]
_compat06__STATIC_PAGES = {'how-it-works': {'title': 'How this site works', 'intro': 'Start with what is useful. Open the evidence, uncertainty and provenance only when you want the deeper route.', 'body': '<section><h2>Useful first</h2><p>The public pages are written for people, not for navigating an internal database. Topics start with a deliberately simple explanation. Resources start with what they are, what they are for and what might make them a poor fit.</p></section><section id="confidence"><h2>What the confidence labels mean</h2><p>A confidence label applies only to the exact statement beside it. It is not a score for a whole topic, person or source, and high confidence does not mean certainty.</p><dl class="confidence-key"><dt>High</dt><dd>The bounded statement has strong, consistent support from the evidence used for it, with no known disagreement large enough to change the statement substantially.</dd><dt>Moderate</dt><dd>The statement is supported, but important limits, narrower evidence, transfer problems or remaining uncertainty mean it should be read with more caution.</dd><dt>Low</dt><dd>The statement has some support but the evidence is limited, indirect or fragile. Treat it as provisional.</dd><dt>Contested</dt><dd>Credible evidence or perspectives materially disagree. The label preserves that disagreement rather than forcing a false consensus.</dd><dt>Not applicable</dt><dd>An epistemic confidence score is not the right description for that statement; this must not be used merely to avoid assessing evidence.</dd></dl></section><section><h2>Being listed is not being endorsed</h2><p>Tools, games, books, services and organisations are catalogued so you can judge them. Existence, popularity and marketing are not evidence that something works. Commercial interests, costs and known limitations stay visible. Any efficacy or safety claim needs its own governed evidence route.</p></section><section><h2>Uncertainty stays visible</h2><p>If an important question is unresolved, the site keeps it unresolved. The aim is to save the next person from having to rediscover the same gap.</p></section><section><h2>Evidence is inspectable</h2><p>Evidence links sit behind the statements they support. Source details and provenance remain available without dominating the first read.</p></section><section><h2>Review dates are visible</h2><p>Pages show when their current record was last reviewed. A review date is not a promise that nothing newer exists; it tells you how fresh this site\'s review is.</p></section><section><h2>This is not a diagnosis service</h2><p>The site is for understanding, practical discovery and research traceability. It does not diagnose individuals or replace appropriate clinical, legal, educational or safeguarding judgement.</p></section>', 'indexable': True}, 'about': {'title': 'About', 'intro': 'Useful neurodiversity information is scattered across research, guidance, communities, tools, games and everyday experience. ND Oracle brings those routes together without hiding where they came from.', 'body': '<section><h2>What it is for</h2><p>You should not have to repeat the same research every time you need to understand a term, find a tool, check a service or work out whether a resource might suit you. ND Oracle keeps useful material connected to its evidence, limitations, disagreement and review state.</p></section><section><h2>More than a diagnosis encyclopaedia</h2><p>The project covers the wider neurodiversity ecosystem: concepts, practical tools, apps, games, books and media, services, organisations, communities and accommodations. Sections become public when they contain useful reviewed material rather than appearing as empty promises.</p></section><section><h2>Provenance first</h2><p>Underneath the simple reading layer is a provenance-first knowledge commons. That means a serious claim keeps its route back to evidence and uncertainty, while a resource listing stays distinct from an endorsement.</p></section><section><h2>What it is not</h2><p>It is not a diagnosis engine, a treatment marketplace, an AI authority or a replacement for professional judgement.</p></section>', 'indexable': True}, 'accessibility': {'title': 'Accessibility', 'intro': 'The site is designed to reduce cognitive and sensory burden rather than add to it.', 'body': '<section><h2>Current approach</h2><p>The site uses semantic HTML, visible keyboard focus, restrained colours, a reading-width content column and no required JavaScript.</p><p>Evidence and provenance use native disclosure controls so readers can choose depth without losing keyboard access.</p></section><section><h2>Accessibility problems are defects</h2><p>Future interactive features must preserve keyboard access, reduced-motion preferences, readable language and a usable no-script baseline wherever practical.</p><p>If something here is difficult to use, <a href="/feedback/">report the accessibility problem</a>.</p></section>', 'indexable': True}, 'privacy': {'title': 'Privacy', 'intro': 'The current public site is designed to collect no personal data.', 'body': "<section><h2>Current release</h2><p>There are no accounts, forms, analytics scripts, advertising trackers or personalised features in the generated site.</p><p>The feedback page links to the public GitHub issue tracker; following that link leaves this site and uses GitHub's service.</p></section><section><h2>External resources</h2><p>Resource pages can link to third-party websites and services. Following those links leaves ND Oracle and the destination's own privacy terms apply.</p></section><section><h2>Future features</h2><p>Anything that stores queries, profiles, health information or community submissions requires a separate privacy and threat-model review before release.</p></section>", 'indexable': True}, 'feedback': {'title': 'Feedback', 'intro': 'Found something inaccessible, unclear, outdated or broken? You can report it without adding tracking or a form to this site.', 'body': '<section><h2>Report a problem</h2><p>Use the public ND Oracle issue tracker for accessibility problems, factual concerns, confusing wording, broken links or other defects. Please do not include private health information, contact details or anything else you would not want published.</p><p><a href="https://github.com/armpitpete/nd-oracle/issues/new" rel="noopener noreferrer">Open the public issue tracker</a></p></section><section><h2>What helps</h2><ul><li>The page address.</li><li>What you expected to happen.</li><li>What actually happened or what was difficult to understand.</li><li>For an evidence concern, the exact statement you think needs checking.</li></ul></section><section class="notice"><h2>Current limitation</h2><p>This release does not yet offer a private feedback channel. If the public GitHub route is itself inaccessible to you, that is a known limitation rather than a reason to treat the problem as resolved.</p></section>', 'indexable': True}, 'oracle': {'title': 'Oracle', 'intro': 'The deeper provenance system is the foundation of these pages, not a chatbot presented as an authority.', 'body': '<p>The current public interface exposes reviewed knowledge through topic and resource pages. Generated answers are not the source of truth. <a href="/how-it-works/">See how the evidence route works</a>.</p>', 'indexable': False}}
_compat06__INDEXED_STATIC_PAGES = tuple((slug for slug, page in _compat06__STATIC_PAGES.items() if page.get('indexable', True)))
def _compat06__esc(value: object) -> str:
    return html.escape(str(value), quote=True)
def _compat06__safe_http_url(value: object) -> str | None:
    if not isinstance(value, str):
        return None
    parsed = urlsplit(value)
    if parsed.scheme not in {'http', 'https'} or not parsed.netloc:
        return None
    return value
def _compat06__human_date(value: str | None) -> str:
    if value is None:
        return 'Not yet reviewed'
    parsed = date.fromisoformat(value)
    return parsed.strftime('%d %B %Y').lstrip('0')
def _compat06__load_concepts() -> list[dict]:
    concepts = []
    for path in sorted(_compat06__OBJECTS_DIR.glob('*.json')):
        with path.open('r', encoding='utf-8') as handle:
            concepts.append(json.load(handle))
    return sorted(concepts, key=lambda item: item['name'].casefold())
def _compat06__load_resources() -> list[dict]:
    resources = []
    if not _compat06__RESOURCES_DIR.is_dir():
        return resources
    for path in sorted(_compat06__RESOURCES_DIR.glob('*.json')):
        with path.open('r', encoding='utf-8') as handle:
            resources.append(json.load(handle))
    return sorted(resources, key=lambda item: item['name'].casefold())
def _compat06__validate_reading_layer(concepts: list[dict]) -> None:
    concept_ids = {concept['id'] for concept in concepts}
    explanation_ids = set(_compat06__SIMPLE_EXPLANATIONS)
    question_ids = {concept_id for _, concept_id in _compat06__COMMON_QUESTIONS}
    if explanation_ids != concept_ids:
        raise ValueError(f'Public-reading explanation set must exactly match authoritative concepts: missing={sorted(concept_ids - explanation_ids)}; unexpected={sorted(explanation_ids - concept_ids)}')
    if question_ids != concept_ids or len(_compat06__COMMON_QUESTIONS) != len(concept_ids):
        raise ValueError(f'Homepage question set must provide exactly one route for every authoritative concept: missing={sorted(concept_ids - question_ids)}; unexpected={sorted(question_ids - concept_ids)}')
def _compat06__reader_intro(concept: dict) -> str:
    return _compat06__SIMPLE_EXPLANATIONS[concept['id']]
def _compat06__list_items(values: list[str]) -> str:
    if not values:
        return '<p class="meta">None recorded.</p>'
    return '<ul>' + ''.join((f'<li>{_compat06__esc(value)}</li>' for value in values)) + '</ul>'
def _compat06__nav(current: str | None=None) -> str:
    links = []
    for slug, label in _compat06__PRIMARY_NAV:
        current_attr = ' aria-current="page"' if slug == current else ''
        links.append(f'<a href="/{slug}/"{current_attr}>{_compat06__esc(label)}</a>')
    return '<nav class="primary-nav" aria-label="Primary">' + ''.join(links) + '</nav>'
def _compat06__page_shell(title: str, intro: str, body: str, *, current: str | None=None, path: str | None=None, indexable: bool=True) -> str:
    canonical = ''
    if path is not None:
        canonical_url = _compat06__PUBLIC_ORIGIN + path
        canonical = f'  <link rel="canonical" href="{_compat06__esc(canonical_url)}">\n'
    robots = '' if indexable else '  <meta name="robots" content="noindex, follow">\n'
    return f'<!doctype html>\n<html lang="en">\n<head>\n  <meta charset="utf-8">\n  <meta name="viewport" content="width=device-width, initial-scale=1">\n  <meta name="color-scheme" content="light">\n  <meta name="theme-color" content="#f4f1ea">\n  <meta name="description" content="{_compat06__esc(intro)}">\n{robots}{canonical}  <title>{_compat06__esc(title)} · The Neurodiverse Oracle</title>\n  <link rel="stylesheet" href="/styles.css">\n</head>\n<body>\n<a class="skip-link" href="#main">Skip to content</a>\n<header class="site-header">\n  <div class="site-shell header-row">\n    <a class="site-name" href="/">The Neurodiverse Oracle</a>\n    {_compat06__nav(current)}\n  </div>\n</header>\n<main id="main" class="site-shell reading-column">\n  <header class="page-heading">\n    <h1>{_compat06__esc(title)}</h1>\n    <p class="lede">{_compat06__esc(intro)}</p>\n  </header>\n  {body}\n</main>\n<footer class="site-footer">\n  <div class="site-shell footer-row">\n    <span>Useful first. Evidence when you want it.</span>\n    <nav aria-label="Footer">\n      <a href="/resources/">Explore</a>\n      <a href="/how-it-works/">How it works</a>\n      <a href="/accessibility/">Accessibility</a>\n      <a href="/feedback/">Feedback</a>\n      <a href="/privacy/">Privacy</a>\n    </nav>\n  </div>\n</footer>\n</body>\n</html>\n'
# ... intentionally omitted in this write ...
