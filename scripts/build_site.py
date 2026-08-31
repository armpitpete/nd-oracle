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
def _compat06__topic_link(concept: dict) -> str:
    return f"""<article class="topic-row">\n  <h2><a href="/understand/{_compat06__esc(concept['id'])}/">{_compat06__esc(concept['name'])}</a></h2>\n  <p>{_compat06__esc(_compat06__reader_intro(concept))}</p>\n</article>"""
def _compat06__resource_link(resource: dict) -> str:
    category = _compat06__RESOURCE_CATEGORY_LABELS.get(resource['category'], resource['category'].replace('_', ' ').title())
    return f"""<article class="resource-row">\n  <div class="resource-row-head"><h3><a href="/resources/{_compat06__esc(resource['id'])}/">{_compat06__esc(resource['name'])}</a></h3><span class="resource-kind">{_compat06__esc(category)}</span></div>\n  <p>{_compat06__esc(resource['description'])}</p>\n  <p class="meta">For: {_compat06__esc(resource['audience_or_context'])}</p>\n</article>"""
def _compat06__resource_counts(resources: list[dict]) -> Counter:
    return Counter((resource['category'] for resource in resources))
def _compat06__render_index(concepts: list[dict], resources: list[dict]) -> str:
    concept_map = {concept['id']: concept for concept in concepts}
    question_links = []
    for question, concept_id in _compat06__COMMON_QUESTIONS:
        if concept_id not in concept_map:
            raise ValueError(f'Common-question target is missing: {concept_id}')
        question_links.append(f'<li><a href="/understand/{_compat06__esc(concept_id)}/">{_compat06__esc(question)}</a></li>')
    topics = ''.join((_compat06__topic_link(concept) for concept in concepts))
    counts = _compat06__resource_counts(resources)
    tool_count = sum((counts[category] for category in _compat06__TOOL_CATEGORIES))
    game_count = counts['game']
    community_count = sum((counts[category] for category in _compat06__COMMUNITY_CATEGORIES))
    body = f"""\n<section class="start-section" aria-labelledby="start-heading">\n  <h2 id="start-heading">Start with a question</h2>\n  <p class="section-intro">Choose the question closest to what you are trying to understand. Every current topic has a route from here.</p>\n  <ul class="question-list">{''.join(question_links)}</ul>\n</section>\n<section class="ecosystem-callout" aria-labelledby="explore-heading">\n  <h2 id="explore-heading">Explore useful things</h2>\n  <p class="section-intro">ND Oracle is more than explanations. Browse reviewed tools, apps, games, books, services and organisations. A listing is not an endorsement: limitations, costs and commercial interests stay visible.</p>\n  <div class="entry-grid">\n    <a class="entry-card" href="/tools/"><strong>Tools &amp; apps</strong><span>{tool_count} current entries</span></a>\n    <a class="entry-card" href="/games/"><strong>Games</strong><span>{game_count} current entries</span></a>\n    <a class="entry-card" href="/community/"><strong>Support &amp; organisations</strong><span>{community_count} current entries</span></a>\n    <a class="entry-card" href="/resources/"><strong>Everything</strong><span>{len(resources)} reviewed resources</span></a>\n  </div>\n</section>\n<section aria-labelledby="topics-heading">\n  <div class="section-heading-row">\n    <div><h2 id="topics-heading">Browse current topics</h2><p class="section-intro">{len(concepts)} evidence-linked topics are available now.</p></div>\n    <a class="quiet-link" href="/understand/">See all topics</a>\n  </div>\n  <div class="topic-list">{topics}</div>\n</section>\n<section class="reading-guide" aria-labelledby="guide-heading">\n  <h2 id="guide-heading">Choose how deep to go</h2>\n  <div class="guide-grid">\n    <div><strong>Read the simple version</strong><p>Topic pages start with a short explanation written for a first read.</p></div>\n    <div><strong>Judge practical resources</strong><p>Resource pages show intended use, limitations, access and conflicts rather than hiding them behind a recommendation score.</p></div>\n    <div><strong>Check the reasoning</strong><p>Where a serious claim is made, evidence and uncertainty remain inspectable.</p></div>\n  </div>\n  <p><a href="/how-it-works/">How evidence, confidence, uncertainty and resource listings work →</a></p>\n</section>\n"""
    return _compat06__page_shell('Understand neurodivergence without doing all the digging yourself', 'Start with an ordinary question, find practical resources, and inspect evidence or uncertainty only when you want to go deeper.', body, path='/')
def _compat06__render_understand_index(concepts: list[dict]) -> str:
    topics = ''.join((_compat06__topic_link(concept) for concept in concepts))
    body = f'\n<section class="notice">\n  <strong>Orientation, not diagnosis.</strong> These pages explain concepts and preserve their evidence routes. They do not diagnose individuals or replace appropriate professional judgement.\n</section>\n<section aria-labelledby="concepts-heading">\n  <h2 id="concepts-heading">Current topics</h2>\n  <p class="section-intro">There are {len(concepts)} reviewed topic pages. Each starts simply and keeps the deeper evidence route available when you want it.</p>\n  <div class="topic-list">{topics}</div>\n</section>\n'
    return _compat06__page_shell('Understand', 'Plain-language topic pages with evidence, uncertainty and different perspectives available without forcing you through them first.', body, current='understand', path='/understand/')
def _compat06__render_concept(concept: dict, concept_map: dict[str, dict]) -> str:
    source_map = {source['id']: source for source in concept['sources']}
    uncertainty_map = {item['id']: item for item in concept['uncertainties']}
    for claim in concept['claims']:
        for source_id in claim['source_ids']:
            if source_id not in source_map:
                raise ValueError(f"{concept['id']}: missing source {source_id}")
        for uncertainty_id in claim['uncertainty_ids']:
            if uncertainty_id not in uncertainty_map:
                raise ValueError(f"{concept['id']}: missing uncertainty {uncertainty_id}")
    claims = []
    for claim in concept['claims']:
        source_links = ', '.join((f"""<a href="#source-{_compat06__esc(source_id)}">{_compat06__esc(source_map[source_id]['citation'])}</a>""" for source_id in claim['source_ids']))
        uncertainty_links = ', '.join((f"""<a href="#uncertainty-{_compat06__esc(uncertainty_id)}">{_compat06__esc(uncertainty_map[uncertainty_id]['question'])}</a>""" for uncertainty_id in claim['uncertainty_ids']))
        claims.append(f"""<article class="claim" id="claim-{_compat06__esc(claim['id'])}">\n  <div class="claim-head"><h3>{_compat06__esc(claim['text'])}</h3><span class="confidence">{_compat06__esc(claim['confidence'])} confidence</span></div>\n  <details class="evidence-detail">\n    <summary>Evidence and uncertainty behind this statement</summary>\n    <div class="route"><div><span class="route-label">Evidence:</span> {source_links}</div><div><span class="route-label">Uncertainty:</span> {uncertainty_links}</div></div>\n  </details>\n</article>""")
    uncertainties = []
    for item in concept['uncertainties']:
        uncertainties.append(f"""<article class="uncertainty" id="uncertainty-{_compat06__esc(item['id'])}">\n  <h3>{_compat06__esc(item['question'])}</h3>\n  <p>{_compat06__esc(item['why_it_matters'])}</p>\n  <details><summary>What could reduce this uncertainty?</summary>{_compat06__list_items(item['what_would_reduce_it'])}</details>\n  <div class="status">Status: {_compat06__esc(item['status'])}</div>\n</article>""")
    perspectives = []
    for item in concept['perspectives']:
        source_links = ', '.join((f"""<a href="#source-{_compat06__esc(source_id)}">{_compat06__esc(source_map[source_id]['citation'])}</a>""" for source_id in item['source_ids']))
        perspectives.append(f"""<article class="perspective">\n  <h3>{_compat06__esc(item['held_by'])}</h3>\n  <p>{_compat06__esc(item['summary'])}</p>\n  <div class="meta">Evidence: {source_links}</div>\n</article>""")
    sources = []
    for source in concept['sources']:
        url = _compat06__safe_http_url(source.get('url'))
        link = f'<a href="{_compat06__esc(url)}" rel="noopener noreferrer">Open source</a>' if url else 'No safe public URL recorded'
        sources.append(f"""<article class="source" id="source-{_compat06__esc(source['id'])}">\n  <h3>{_compat06__esc(source['citation'])}</h3>\n  <div class="meta">Kind: {_compat06__esc(source['kind'])} · accessed {_compat06__esc(source['accessed'])}</div>\n  <p>{link}</p>\n</article>""")
    relations = []
    for relation in concept['relations']:
        target_id = relation['target_id']
        if target_id not in concept_map:
            raise ValueError(f"{concept['id']}: missing related concept {target_id}")
        relations.append(f"""<li><a href="/understand/{_compat06__esc(target_id)}/">{_compat06__esc(concept_map[target_id]['name'])}</a> — {_compat06__esc(relation['note'])}</li>""")
    reviewed = _compat06__human_date(concept['provenance'].get('last_reviewed'))
    body = f"""\n<p class="back-link"><a href="/understand/">← All topics</a></p>\n<p class="review-meta">Last reviewed: <strong>{_compat06__esc(reviewed)}</strong></p>\n<details class="technical-summary"><summary>More precise description</summary><p>{_compat06__esc(concept['summary'])}</p></details>\n<section class="at-a-glance" aria-labelledby="glance-heading">\n  <h2 id="glance-heading">At a glance</h2>\n  <div class="scope-grid">\n    <div><h3>This page covers</h3>{_compat06__list_items(concept['scope']['includes'])}</div>\n    <div><h3>It does not mean</h3>{_compat06__list_items(concept['scope']['excludes'])}</div>\n  </div>\n</section>\n<section aria-labelledby="known-heading"><h2 id="known-heading">What we can say</h2><p class="section-intro">These are bounded statements from the current evidence record. <a href="/how-it-works/#confidence">See what the confidence labels mean</a>. Open a statement only if you want its evidence route.</p>{''.join(claims)}</section>\n<section aria-labelledby="uncertainty-heading"><h2 id="uncertainty-heading">What remains uncertain</h2>{''.join(uncertainties)}</section>\n<section aria-labelledby="perspectives-heading"><h2 id="perspectives-heading">Different perspectives</h2>{''.join(perspectives)}</section>\n<section aria-labelledby="related-heading"><h2 id="related-heading">Related topics</h2><ul>{''.join(relations)}</ul></section>\n<section aria-labelledby="sources-heading"><h2 id="sources-heading">Sources</h2>{''.join(sources)}</section>\n<details class="provenance"><summary>Page provenance and review state</summary><p>{_compat06__esc(concept['provenance']['method'])}</p><div class="meta">Created {_compat06__esc(concept['provenance']['created'])} · last reviewed {_compat06__esc(reviewed)} · review state {_compat06__esc(concept['provenance']['review_state'])}</div></details>\n"""
    return _compat06__page_shell(concept['name'], _compat06__reader_intro(concept), body, current='understand', path=f"/understand/{concept['id']}/")
def _compat06__render_resource_collection(resources: list[dict], *, title: str, intro: str, route: str, categories: set[str] | None=None) -> str:
    selected = [resource for resource in resources if categories is None or resource['category'] in categories]
    rows = ''.join((_compat06__resource_link(resource) for resource in selected))
    body = f"""\n<section class="notice">\n  <strong>Listed, not endorsed.</strong> Inclusion means the resource was identified, checked and described. It does not mean ND Oracle has proved that it works or that it will suit you.\n</section>\n<nav class="resource-subnav" aria-label="Explore resources">\n  <a href="/resources/">Everything</a>\n  <a href="/tools/">Tools &amp; apps</a>\n  <a href="/games/">Games</a>\n  <a href="/community/">Support &amp; organisations</a>\n</nav>\n<section aria-labelledby="resource-list-heading">\n  <h2 id="resource-list-heading">{len(selected)} reviewed {('entry' if len(selected) == 1 else 'entries')}</h2>\n  <div class="resource-list">{rows}</div>\n</section>\n"""
    return _compat06__page_shell(title, intro, body, current='resources', path=f'/{route}/')
def _compat06__render_resources_index(resources: list[dict]) -> str:
    return _compat06__render_resource_collection(resources, title='Explore', intro='Tools, apps, games, books, services and organisations, described with their limitations and access conditions visible.', route='resources')
def _compat06__resource_access_links(resource: dict) -> str:
    links = []
    for locator in resource.get('locators', []):
        locator_type = locator.get('type')
        value = locator.get('value')
        if locator_type == 'url':
            url = _compat06__safe_http_url(value)
            if url:
                links.append(f'<li><a href="{_compat06__esc(url)}" rel="noopener noreferrer">Visit official resource</a></li>')
        else:
            links.append(f'<li>{_compat06__esc(locator_type)}: {_compat06__esc(value)}</li>')
    return '<ul>' + ''.join(links) + '</ul>'
def _compat06__render_resource(resource: dict, concept_map: dict[str, dict]) -> str:
    category = _compat06__RESOURCE_CATEGORY_LABELS.get(resource['category'], resource['category'].replace('_', ' ').title())
    related = []
    for ref in resource.get('related_objects', []):
        if ref.get('type') != 'concept':
            continue
        concept = concept_map.get(ref.get('id'))
        if concept is not None:
            related.append(f"""<li><a href="/understand/{_compat06__esc(concept['id'])}/">{_compat06__esc(concept['name'])}</a></li>""")
    related_html = '<ul>' + ''.join(related) + '</ul>' if related else '<p class="meta">No topic link recorded yet.</p>'
    reviewed = _compat06__human_date(resource['provenance'].get('last_reviewed'))
    claim_note = 'This resource currently has governed claim records. Open those claims only when their evidence routes are available.' if resource.get('claims') else 'This listing makes no efficacy or safety claim. It records what the resource is, what it is for, how to reach it and what limitations are already known.'
    body = f"""\n<p class="back-link"><a href="/resources/">← All resources</a></p>\n<div class="resource-meta"><span class="resource-kind">{_compat06__esc(category)}</span><span>Last reviewed: <strong>{_compat06__esc(reviewed)}</strong></span></div>\n<section class="notice"><strong>Listed, not endorsed.</strong> ND Oracle is helping you inspect this resource, not telling you that it will work for you.</section>\n<section aria-labelledby="use-heading"><h2 id="use-heading">What it is for</h2><p>{_compat06__esc(resource['intended_use'])}</p></section>\n<section aria-labelledby="audience-heading"><h2 id="audience-heading">Who or what context</h2><p>{_compat06__esc(resource['audience_or_context'])}</p></section>\n<section aria-labelledby="access-heading"><h2 id="access-heading">Access</h2>{_compat06__resource_access_links(resource)}</section>\n<section aria-labelledby="related-heading"><h2 id="related-heading">Related topics</h2>{related_html}</section>\n<section aria-labelledby="limits-heading"><h2 id="limits-heading">Limitations and possible poor fit</h2>{_compat06__list_items(resource['limitations'])}</section>\n<section aria-labelledby="cost-heading"><h2 id="cost-heading">Cost and access notes</h2>{_compat06__list_items(resource['cost_or_access_notes'])}</section>\n<section aria-labelledby="conflict-heading"><h2 id="conflict-heading">Ownership and conflicts</h2>{_compat06__list_items(resource['conflicts_of_interest'])}</section>\n<section class="evidence-status" aria-labelledby="evidence-status-heading"><h2 id="evidence-status-heading">Evidence status</h2><p>{_compat06__esc(claim_note)}</p></section>\n<details class="provenance"><summary>Page provenance and review state</summary><p>{_compat06__esc(resource['provenance']['method'])}</p><div class="meta">Created {_compat06__esc(resource['provenance']['created'])} · last reviewed {_compat06__esc(reviewed)} · review state {_compat06__esc(resource['provenance']['review_state'])}</div></details>\n"""
    return _compat06__page_shell(resource['name'], resource['description'], body, current='resources', path=f"/resources/{resource['id']}/")
def _compat06__render_static_page(slug: str) -> str:
    page = _compat06__STATIC_PAGES[slug]
    return _compat06__page_shell(page['title'], page['intro'], page['body'], current=slug if slug in dict(_compat06__PRIMARY_NAV) else None, path=f'/{slug}/', indexable=page.get('indexable', True))
def _compat06__render_not_found() -> str:
    body = '\n<section>\n  <h2>Try one of these instead</h2>\n  <ul class="question-list">\n    <li><a href="/">Go to the homepage</a></li>\n    <li><a href="/understand/">Browse current topics</a></li>\n    <li><a href="/resources/">Explore tools, games and support</a></li>\n    <li><a href="/how-it-works/">See how the site works</a></li>\n    <li><a href="/feedback/">Report a broken or confusing page</a></li>\n  </ul>\n</section>\n'
    return _compat06__page_shell('Page not found', 'That address does not match a current page, but you can get back to the useful parts of the site here.', body, indexable=False)
def _compat06__sitemap_paths(concepts: list[dict], resources: list[dict] | None=None) -> list[str]:
    if resources is None:
        resources = _compat06__load_resources()
    paths = ['/', '/understand/', '/resources/', '/tools/', '/games/', '/community/']
    paths.extend((f"/understand/{concept['id']}/" for concept in concepts))
    paths.extend((f"/resources/{resource['id']}/" for resource in resources))
    paths.extend((f'/{slug}/' for slug in _compat06__INDEXED_STATIC_PAGES))
    return paths
def _compat06__render_sitemap(concepts: list[dict], resources: list[dict]) -> str:
    urls = ''.join((f'  <url><loc>{html.escape(_compat06__PUBLIC_ORIGIN + path)}</loc></url>\n' for path in _compat06__sitemap_paths(concepts, resources)))
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n'
def _compat06__prepare_output(output_dir: Path) -> None:
    marker = output_dir / '.nd-oracle-generated'
    if output_dir.is_symlink():
        raise ValueError(f'Refusing to replace symlink output directory: {output_dir}')
    if output_dir.exists():
        if not marker.is_file() or marker.read_text(encoding='utf-8') != _compat06__OUTPUT_MARKER:
            raise ValueError(f'Refusing to replace unmarked output directory: {output_dir}')
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True)
    marker.write_text(_compat06__OUTPUT_MARKER, encoding='utf-8')
def _compat06__write_route(output_dir: Path, route: str, content: str) -> None:
    target = output_dir / route / 'index.html'
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding='utf-8')
def _compat06__build(output_dir: Path=_compat06__DEFAULT_OUTPUT_DIR) -> Path:
    concepts = _compat06__load_concepts()
    resources = _compat06__load_resources()
    if not concepts:
        raise ValueError('No concept objects found')
    _compat06__validate_reading_layer(concepts)
    concept_map = {concept['id']: concept for concept in concepts}
    _compat06__prepare_output(output_dir)
    shutil.copy2(_compat06__SITE_DIR / 'styles.css', output_dir / 'styles.css')
    shutil.copy2(_compat06__SITE_DIR / '_headers', output_dir / '_headers')
    (output_dir / 'index.html').write_text(_compat06__render_index(concepts, resources), encoding='utf-8')
    _compat06__write_route(output_dir, 'understand', _compat06__render_understand_index(concepts))
    _compat06__write_route(output_dir, 'resources', _compat06__render_resources_index(resources))
    _compat06__write_route(output_dir, 'tools', _compat06__render_resource_collection(resources, title='Tools & apps', intro='Practical tools, apps and products you can inspect by purpose, access, limitations and conflicts rather than by hype.', route='tools', categories=_compat06__TOOL_CATEGORIES))
    _compat06__write_route(output_dir, 'games', _compat06__render_resource_collection(resources, title='Games', intro='Games described by play characteristics, pressure, accessibility and possible poor fit — not as treatments or prescriptions.', route='games', categories={'game'}))
    _compat06__write_route(output_dir, 'community', _compat06__render_resource_collection(resources, title='Support & organisations', intro='Services, organisations and communities with their scope, geography and limitations kept visible.', route='community', categories=_compat06__COMMUNITY_CATEGORIES))
    for concept in concepts:
        _compat06__write_route(output_dir, f"understand/{concept['id']}", _compat06__render_concept(concept, concept_map))
    for resource in resources:
        _compat06__write_route(output_dir, f"resources/{resource['id']}", _compat06__render_resource(resource, concept_map))
    for slug in _compat06__STATIC_PAGES:
        _compat06__write_route(output_dir, slug, _compat06__render_static_page(slug))
    (output_dir / '404.html').write_text(_compat06__render_not_found(), encoding='utf-8')
    (output_dir / 'sitemap.xml').write_text(_compat06__render_sitemap(concepts, resources), encoding='utf-8')
    (output_dir / 'robots.txt').write_text(f'User-agent: *\nAllow: /\nSitemap: {_compat06__PUBLIC_ORIGIN}/sitemap.xml\n', encoding='utf-8')
    return output_dir

# ---- v08 compatibility foundation ----
if __package__ in {None, ''}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
_compat08__QUESTIONS_DIR = _compat06__ROOT / 'objects' / 'questions'
_compat08__PRIMARY_NAV = [('questions', 'Questions'), ('understand', 'Topics'), ('resources', 'Resources'), ('how-it-works', 'How it works'), ('about', 'About')]
_compat06__PRIMARY_NAV = _compat08__PRIMARY_NAV
if not '_compat06___V08_ORIGINAL_PAGE_SHELL' in globals():
    _compat06___V08_ORIGINAL_PAGE_SHELL = _compat06__page_shell
_compat08___page_shell_v06 = _compat06___V08_ORIGINAL_PAGE_SHELL
def _compat08__page_shell(*args, **kwargs) -> str:
    page = _compat08___page_shell_v06(*args, **kwargs)
    return page.replace('<a href="/resources/">Explore</a>', '<a href="/resources/">Resources</a>')
_compat06__page_shell = _compat08__page_shell
_compat08__BOOK_MEDIA_CATEGORIES = {'book', 'media'}
_compat08__QUESTION_GROUPS = [('Everyday life & technology', ['task-starting-and-organisation', 'make-device-easier-to-use']), ('Work & study', ['workplace-support-great-britain', 'reasonable-adjustments-at-work-great-britain', 'disabled-student-support-england', 'disabled-person-looking-for-work-uk']), ('Finding information & support', ['autism-information-and-support', 'dyslexia-information-and-support-uk', 'tourette-information-and-support-uk', 'learning-disability-information-and-support-uk', 'dld-information-and-support', 'adult-dyspraxia-information-uk']), ('Games & downtime', ['low-time-pressure-games']), ('Anxiety & self-management', ['autism-anxiety-tools'])]
_compat08__FEATURED_QUESTION_IDS = ['task-starting-and-organisation', 'reasonable-adjustments-at-work-great-britain', 'disabled-student-support-england', 'dld-information-and-support', 'low-time-pressure-games', 'autism-information-and-support']
_compat08__QUESTION_DISCOVERY_HOW_SECTION = '<section><h2>Question-led discovery</h2><p>Practical question pages route an ordinary need across already governed topics and resources. They show the current bounded synthesis, what is relevant to inspect, what evidence is still missing, where people may disagree and what should cause the answer to be revisited.</p><p>A question route is not a personalised recommendation and does not turn a resource listing into proof that it works.</p></section>'
_compat08__QUESTION_DISCOVERY_ABOUT_SECTION = '<section><h2>Start with the problem, not the taxonomy</h2><p>Question-led discovery lets a reader begin with an everyday problem and then move into the governed topics and resources behind the answer. The question page remains a route through the knowledge commons rather than a new source of authority.</p></section>'
if _compat08__QUESTION_DISCOVERY_HOW_SECTION not in _compat06__STATIC_PAGES['how-it-works']['body']:
    _compat06__STATIC_PAGES['how-it-works']['body'] += _compat08__QUESTION_DISCOVERY_HOW_SECTION
if _compat08__QUESTION_DISCOVERY_ABOUT_SECTION not in _compat06__STATIC_PAGES['about']['body']:
    _compat06__STATIC_PAGES['about']['body'] += _compat08__QUESTION_DISCOVERY_ABOUT_SECTION
_compat06__STATIC_PAGES['oracle']['body'] = '<p>The current public interface exposes reviewed knowledge through topic, resource and governed question pages. Generated answers are not the source of truth. <a href="/questions/">Start with a governed question</a> or <a href="/how-it-works/">see how the evidence route works</a>.</p>'
_compat08__STATIC_PAGES = _compat06__STATIC_PAGES
_compat08___RESOURCE_SUBNAV_V06 = '<nav class="resource-subnav" aria-label="Explore resources">\n  <a href="/resources/">Everything</a>\n  <a href="/tools/">Tools &amp; apps</a>\n  <a href="/games/">Games</a>\n  <a href="/community/">Support &amp; organisations</a>\n</nav>'
_compat08___RESOURCE_SUBNAV_V08 = '<nav class="resource-subnav" aria-label="Browse resources">\n  <a href="/resources/">All resources</a>\n  <a href="/tools/">Tools &amp; practical help</a>\n  <a href="/games/">Games</a>\n  <a href="/books-media/">Books &amp; media</a>\n  <a href="/community/">Support &amp; organisations</a>\n</nav>'
_compat08___render_resource_collection_v06 = _compat06__render_resource_collection
def _compat08__render_resource_collection(resources: list[dict], *, title: str, intro: str, route: str, categories: set[str] | None=None) -> str:
    page = _compat08___render_resource_collection_v06(resources, title=title, intro=intro, route=route, categories=categories)
    if _compat08___RESOURCE_SUBNAV_V06 not in page:
        raise ValueError('Cannot locate v0.6 resource sub-navigation')
    return page.replace(_compat08___RESOURCE_SUBNAV_V06, _compat08___RESOURCE_SUBNAV_V08, 1)
def _compat08__render_resources_index(resources: list[dict]) -> str:
    return _compat08__render_resource_collection(resources, title='Resources', intro='Tools, practical guides, games, books, services and organisations, described with their limitations and access conditions visible.', route='resources')
def _compat08__load_questions() -> list[dict]:
    questions = []
    if not _compat08__QUESTIONS_DIR.is_dir():
        return questions
    for path in sorted(_compat08__QUESTIONS_DIR.glob('*.json')):
        with path.open('r', encoding='utf-8') as handle:
            questions.append(json.load(handle))
    return sorted(questions, key=lambda item: item['question'].casefold())
def _compat08__validate_question_navigation(questions: list[dict]) -> None:
    question_ids = {question['id'] for question in questions}
    grouped_ids = [question_id for _, ids in _compat08__QUESTION_GROUPS for question_id in ids]
    grouped_set = set(grouped_ids)
    if len(grouped_ids) != len(grouped_set):
        raise ValueError('Question navigation groups contain duplicate question IDs')
    if grouped_set != question_ids:
        raise ValueError(f'Question navigation groups must exactly cover the governed Question corpus: missing={sorted(question_ids - grouped_set)}; unexpected={sorted(grouped_set - question_ids)}')
    featured_set = set(_compat08__FEATURED_QUESTION_IDS)
    if len(_compat08__FEATURED_QUESTION_IDS) != len(featured_set) or not featured_set <= question_ids:
        raise ValueError('Featured questions must be unique governed Question IDs')
def _compat08__question_link(question: dict) -> str:
    return f"""<article class="topic-row">\n  <h3><a href="/questions/{_compat06__esc(question['id'])}/">{_compat06__esc(question['question'])}</a></h3>\n  <p>{_compat06__esc(question['why_it_matters'])}</p>\n</article>"""
def _compat08__render_index(concepts: list[dict], resources: list[dict], questions: list[dict] | None=None) -> str:
    if questions is None:
        questions = _compat08__load_questions()
    _compat08__validate_question_navigation(questions)
    question_map = {question['id']: question for question in questions}
    base = _compat06__render_index(concepts, resources)
    practical_links = ''.join((f"""<li><a href="/questions/{_compat06__esc(question_id)}/">{_compat06__esc(question_map[question_id]['question'])}</a></li>""" for question_id in _compat08__FEATURED_QUESTION_IDS))
    practical = f'\n<section class="start-section" aria-labelledby="practical-question-heading">\n  <h2 id="practical-question-heading">Start with something you need to do</h2>\n  <p class="section-intro">These are governed routes across the current catalogue. They identify things worth inspecting without pretending one answer fits everyone.</p>\n  <ul class="question-list">{practical_links}</ul>\n  <p><a href="/questions/">Browse all {len(questions)} practical questions →</a></p>\n</section>\n'
    needle = '<section class="start-section" aria-labelledby="start-heading">'
    if needle not in base:
        raise ValueError('Cannot locate v0.6 homepage start section')
    base = base.replace(needle, practical + needle, 1)
    base = base.replace('<a class="entry-card" href="/tools/"><strong>Tools &amp; apps</strong>', '<a class="entry-card" href="/tools/"><strong>Tools &amp; practical help</strong>', 1)
    book_media_count = sum((1 for resource in resources if resource['category'] in _compat08__BOOK_MEDIA_CATEGORIES))
    everything_card = f'<a class="entry-card" href="/resources/"><strong>Everything</strong><span>{len(resources)} reviewed resources</span></a>'
    books_card = f'<a class="entry-card" href="/books-media/"><strong>Books &amp; media</strong><span>{book_media_count} current entries</span></a>'
    if everything_card not in base:
        raise ValueError('Cannot locate homepage all-resources card')
    return base.replace(everything_card, books_card + everything_card, 1)
def _compat08__render_questions_index(questions: list[dict]) -> str:
    _compat08__validate_question_navigation(questions)
    question_map = {question['id']: question for question in questions}
    groups = []
    for group_name, ids in _compat08__QUESTION_GROUPS:
        group_slug = group_name.lower().replace(' ', '-').replace('&', 'and')
        rows = ''.join((_compat08__question_link(question_map[question_id]) for question_id in ids))
        groups.append(f'<section aria-labelledby="question-group-{_compat06__esc(group_slug)}"><h2 id="question-group-{_compat06__esc(group_slug)}">{_compat06__esc(group_name)}</h2><div class="topic-list">{rows}</div></section>')
    body = f"""\n<section class="notice">\n  <strong>Relevant to inspect, not recommended.</strong> These pages route ordinary needs through reviewed ND Oracle material. They do not diagnose you, choose for you or turn a resource listing into an efficacy claim.\n</section>\n<section aria-labelledby="questions-heading">\n  <h2 id="questions-heading">{len(questions)} governed practical questions</h2>\n  <p class="section-intro">Browse by the kind of problem you are trying to solve. Each page keeps the current synthesis, limitations, disagreement and evidence gaps visible.</p>\n</section>\n{''.join(groups)}\n"""
    return _compat08__page_shell('Questions', 'Start with an everyday problem and follow a governed route to relevant topics, tools, games, services or organisations.', body, current='questions', path='/questions/')
def _compat08___related_question_items(question: dict, concept_map: dict[str, dict], resource_map: dict[str, dict]) -> str:
    items = []
    for ref in question['related_objects']:
        object_type = ref['type']
        object_id = ref['id']
        if object_type == 'concept':
            target = concept_map.get(object_id)
            if target is None:
                raise ValueError(f"{question['id']}: missing related concept {object_id}")
            items.append(f"""<li><a href="/understand/{_compat06__esc(object_id)}/">{_compat06__esc(target['name'])}</a> <span class="meta">Topic</span></li>""")
        elif object_type == 'resource':
            target = resource_map.get(object_id)
            if target is None:
                raise ValueError(f"{question['id']}: missing related resource {object_id}")
            category = _compat06__RESOURCE_CATEGORY_LABELS.get(target['category'], target['category'].replace('_', ' ').title())
            items.append(f"""<li><a href="/resources/{_compat06__esc(object_id)}/">{_compat06__esc(target['name'])}</a> <span class="meta">{_compat06__esc(category)}</span></li>""")
        else:
            raise ValueError(f"{question['id']}: public question renderer does not yet support related {object_type} objects")
    return '<ul>' + ''.join(items) + '</ul>'
def _compat08__render_question(question: dict, concept_map: dict[str, dict], resource_map: dict[str, dict]) -> str:
    reviewed = _compat06__human_date(question['provenance'].get('last_reviewed'))
    status = question['status'].replace('_', ' ').capitalize()
    related = _compat08___related_question_items(question, concept_map, resource_map)
    body = f"""\n<p class="back-link"><a href="/questions/">← All questions</a></p>\n<p class="review-meta">Last reviewed: <strong>{_compat06__esc(reviewed)}</strong> · Status: <strong>{_compat06__esc(status)}</strong></p>\n<section class="notice">\n  <strong>Relevant to inspect, not recommended.</strong> This is a bounded synthesis of the current governed catalogue, not a personalised recommendation or proof that a listed resource will work for you.\n</section>\n<section aria-labelledby="current-understanding-heading">\n  <h2 id="current-understanding-heading">Current understanding</h2>\n  <p>{_compat06__esc(question['current_understanding'])}</p>\n</section>\n<section aria-labelledby="related-things-heading">\n  <h2 id="related-things-heading">Related things to inspect</h2>\n  {related}\n</section>\n<section aria-labelledby="evidence-needed-heading">\n  <h2 id="evidence-needed-heading">What evidence is still needed</h2>\n  {_compat06__list_items(question['evidence_needed'])}\n</section>\n<section aria-labelledby="dissent-heading">\n  <h2 id="dissent-heading">Where people may disagree</h2>\n  {_compat06__list_items(question.get('dissent', []))}\n</section>\n<section aria-labelledby="reopen-heading">\n  <h2 id="reopen-heading">When this answer should be revisited</h2>\n  {_compat06__list_items(question['reopening_conditions'])}\n</section>\n<details class="provenance"><summary>Question provenance and review state</summary>\n  <p>{_compat06__esc(question['provenance']['method'])}</p>\n  <div class="meta">Created {_compat06__esc(question['provenance']['created'])} · last reviewed {_compat06__esc(reviewed)} · review state {_compat06__esc(question['provenance']['review_state'])}</div>\n</details>\n"""
    return _compat08__page_shell(question['question'], question['why_it_matters'], body, current='questions', path=f"/questions/{question['id']}/")
def _compat08___question_uses_ref(question: dict, object_type: str, object_id: str) -> bool:
    return any((ref.get('type') == object_type and ref.get('id') == object_id for ref in question.get('related_objects', [])))
def _compat08___question_links_for_ref(questions: list[dict], object_type: str, object_id: str) -> str:
    matched = [question for question in questions if _compat08___question_uses_ref(question, object_type, object_id)]
    if not matched:
        return '<p class="meta">No practical question route links here yet.</p>'
    return '<ul>' + ''.join((f"""<li><a href="/questions/{_compat06__esc(question['id'])}/">{_compat06__esc(question['question'])}</a></li>""" for question in matched)) + '</ul>'
def _compat08___resource_links_for_concept(resources: list[dict], concept_id: str) -> str:
    matched = [resource for resource in resources if any((ref.get('type') == 'concept' and ref.get('id') == concept_id for ref in resource.get('related_objects', [])))]
    if not matched:
        return '<p class="meta">No reviewed resource link recorded yet.</p>'
    return '<ul>' + ''.join((f"""<li><a href="/resources/{_compat06__esc(resource['id'])}/">{_compat06__esc(resource['name'])}</a> <span class="meta">{_compat06__esc(_compat06__RESOURCE_CATEGORY_LABELS.get(resource['category'], resource['category'].replace('_', ' ').title()))}</span></li>""" for resource in matched)) + '</ul>'
def _compat08__render_concept(concept: dict, concept_map: dict[str, dict], resources: list[dict], questions: list[dict]) -> str:
    page = _compat06__render_concept(concept, concept_map)
    needle = '<section aria-labelledby="sources-heading">'
    if needle not in page:
        raise ValueError(f"{concept['id']}: cannot locate sources section for navigation injection")
    discovery_section = f"""\n<section aria-labelledby="next-routes-heading">\n  <h2 id="next-routes-heading">Useful next routes</h2>\n  <h3>Practical questions</h3>\n  {_compat08___question_links_for_ref(questions, 'concept', concept['id'])}\n  <h3>Related resources</h3>\n  {_compat08___resource_links_for_concept(resources, concept['id'])}\n</section>\n"""
    return page.replace(needle, discovery_section + needle, 1)
def _compat08__render_resource(resource: dict, concept_map: dict[str, dict], questions: list[dict]) -> str:
    page = _compat06__render_resource(resource, concept_map)
    needle = '<section aria-labelledby="limits-heading">'
    if needle not in page:
        raise ValueError(f"{resource['id']}: cannot locate limitations section for navigation injection")
    discovery_section = f"""\n<section aria-labelledby="resource-question-heading">\n  <h2 id="resource-question-heading">Questions that lead here</h2>\n  {_compat08___question_links_for_ref(questions, 'resource', resource['id'])}\n</section>\n"""
    return page.replace(needle, discovery_section + needle, 1)
def _compat08__render_books_media_index(resources: list[dict]) -> str:
    return _compat08__render_resource_collection(resources, title='Books & media', intro='Reviewed books and media in the ND Oracle catalogue, with context, limitations and conflicts kept visible.', route='books-media', categories=_compat08__BOOK_MEDIA_CATEGORIES)
def _compat08__sitemap_paths(concepts: list[dict], resources: list[dict] | None=None, questions: list[dict] | None=None) -> list[str]:
    if resources is None:
        resources = _compat06__load_resources()
    if questions is None:
        questions = _compat08__load_questions()
    paths = _compat06__sitemap_paths(concepts, resources)
    paths.append('/books-media/')
    paths.append('/questions/')
    paths.extend((f"/questions/{question['id']}/" for question in questions))
    return paths
def _compat08__render_sitemap(concepts: list[dict], resources: list[dict], questions: list[dict] | None=None) -> str:
    if questions is None:
        questions = _compat08__load_questions()
    urls = ''.join((f'  <url><loc>{html.escape(_compat06__PUBLIC_ORIGIN + path)}</loc></url>\n' for path in _compat08__sitemap_paths(concepts, resources, questions)))
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n'
def _compat08__build(output_dir=_compat06__DEFAULT_OUTPUT_DIR):
    questions = _compat08__load_questions()
    if not questions:
        raise ValueError('No question objects found')
    _compat08__validate_question_navigation(questions)
    destination = _compat06__build(output_dir)
    concepts = _compat06__load_concepts()
    resources = _compat06__load_resources()
    concept_map = {concept['id']: concept for concept in concepts}
    resource_map = {resource['id']: resource for resource in resources}
    (destination / 'index.html').write_text(_compat08__render_index(concepts, resources, questions), encoding='utf-8')
    _compat06__write_route(destination, 'resources', _compat08__render_resources_index(resources))
    _compat06__write_route(destination, 'tools', _compat08__render_resource_collection(resources, title='Tools & practical help', intro='Tools, apps, practical guides and products that can make everyday tasks, access, work or study easier to navigate.', route='tools', categories=_compat06__TOOL_CATEGORIES))
    _compat06__write_route(destination, 'games', _compat08__render_resource_collection(resources, title='Games', intro='Games described by play characteristics, pressure, accessibility and possible poor fit — not as treatments or prescriptions.', route='games', categories={'game'}))
    _compat06__write_route(destination, 'community', _compat08__render_resource_collection(resources, title='Support & organisations', intro='Services, organisations and communities with their scope, geography and limitations kept visible.', route='community', categories=_compat06__COMMUNITY_CATEGORIES))
    _compat06__write_route(destination, 'books-media', _compat08__render_books_media_index(resources))
    for concept in concepts:
        _compat06__write_route(destination, f"understand/{concept['id']}", _compat08__render_concept(concept, concept_map, resources, questions))
    for resource in resources:
        _compat06__write_route(destination, f"resources/{resource['id']}", _compat08__render_resource(resource, concept_map, questions))
    _compat06__write_route(destination, 'questions', _compat08__render_questions_index(questions))
    for question in questions:
        _compat06__write_route(destination, f"questions/{question['id']}", _compat08__render_question(question, concept_map, resource_map))
    (destination / 'sitemap.xml').write_text(_compat08__render_sitemap(concepts, resources, questions), encoding='utf-8')
    return destination

# ---- v09 compatibility foundation ----
if __package__ in {None, ''}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
_compat09__QUESTIONS_DIR = _compat08__QUESTIONS_DIR
_compat09__FEATURED_QUESTION_IDS = list(_compat08__FEATURED_QUESTION_IDS)
_compat09__V07_HOMEPAGE_COMPAT_QUESTION_IDS = ('task-starting-and-organisation', 'low-time-pressure-games', 'workplace-support-great-britain', 'autism-information-and-support', 'autism-anxiety-tools')
for _question_id in _compat09__V07_HOMEPAGE_COMPAT_QUESTION_IDS:
    if _question_id not in _compat09__FEATURED_QUESTION_IDS:
        _compat09__FEATURED_QUESTION_IDS.append(_question_id)
_compat08__FEATURED_QUESTION_IDS = _compat09__FEATURED_QUESTION_IDS
_compat09__BOOK_MEDIA_CATEGORIES = set(_compat08__BOOK_MEDIA_CATEGORIES)
_compat09__V09_SIMPLE_EXPLANATIONS = {'dyscalculia': 'Dyscalculia is a persistent difficulty learning and using number and arithmetic skills; it is not the same as simply being bad at maths.', 'masking': 'Masking or camouflaging is when someone changes or hides parts of how they naturally communicate or behave to meet social expectations.', 'autistic-burnout': 'Autistic burnout is a community and research term for severe, long-lasting exhaustion and reduced capacity reported by some autistic people.', 'monotropism': 'Monotropism is a theory that describes attention as tending to concentrate deeply on a smaller number of interests or demands at once.', 'interoception': 'Interoception is how the nervous system senses and interprets signals from inside the body, such as hunger, heartbeat or temperature.', 'alexithymia': 'Alexithymia describes difficulty identifying or describing emotions; it is not the same thing as autism and can occur across groups.', 'stimming': 'Stimming means repetitive movements, sounds or sensory actions that can serve many functions, including enjoyment or regulation.', 'communication-differences': 'Communication differences include variation in speaking, understanding, timing, non-verbal communication and use of AAC.', 'task-initiation': 'Task initiation is the step between intending to do something and actually starting it; difficulty here can have many causes.', 'sensory-overload': 'Sensory overload is when sensory input becomes overwhelming or difficult to manage; what causes it varies by person and context.'}
_compat09__V09_COMMON_QUESTIONS = [('What does dyscalculia mean, and how is it different from ordinary maths difficulty?', 'dyscalculia'), ('What do people mean by masking or camouflaging?', 'masking'), ('What is autistic burnout, and how certain is the evidence?', 'autistic-burnout'), ('What is monotropism?', 'monotropism'), ('What is interoception?', 'interoception'), ('What is alexithymia?', 'alexithymia'), ('Why do people stim?', 'stimming'), ('What kinds of communication differences can matter?', 'communication-differences'), ('Why can starting a task be difficult?', 'task-initiation'), ('What do people mean by sensory overload?', 'sensory-overload')]
_compat06__SIMPLE_EXPLANATIONS.update(_compat09__V09_SIMPLE_EXPLANATIONS)
_compat09___existing_common_targets = {target_id for _question, target_id in _compat06__COMMON_QUESTIONS}
for _question, _target_id in _compat09__V09_COMMON_QUESTIONS:
    if _target_id not in _compat09___existing_common_targets:
        _compat06__COMMON_QUESTIONS.append((_question, _target_id))
        _compat09___existing_common_targets.add(_target_id)
_compat09__SIMPLE_EXPLANATIONS = _compat06__SIMPLE_EXPLANATIONS
_compat09__COMMON_QUESTIONS = _compat06__COMMON_QUESTIONS
_compat09__QUESTION_GROUPS = [('Daily life & technology', ['task-starting-and-organisation', 'make-device-easier-to-use', 'meal-planning-and-everyday-food-tasks']), ('Sensory & environment', ['make-noisy-bright-place-easier', 'sensory-overload-what-can-i-change']), ('Communication', ['aac-and-nonspeaking-communication', 'phone-calls-are-difficult', 'processing-time-in-conversations-meetings']), ('Work', ['workplace-support-great-britain', 'reasonable-adjustments-at-work-great-britain', 'disabled-person-looking-for-work-uk', 'disclosing-disability-neurodivergence-at-work', 'job-interview-adjustments-great-britain']), ('Education & study', ['disabled-student-support-england', 'organising-study-and-assignments', 'send-support-school-college-england']), ('Assessment & diagnosis', ['adult-adhd-assessment-england', 'adult-autism-assessment-england']), ('Health & wellbeing', ['autism-anxiety-tools', 'masking-exhaustion-and-autistic-burnout', 'sleep-and-winding-down-routines']), ('Relationships & family', ['autistic-parent-support-uk']), ('Information & support', ['autism-information-and-support', 'dyslexia-information-and-support-uk', 'tourette-information-and-support-uk', 'learning-disability-information-and-support-uk', 'dld-information-and-support', 'adult-dyspraxia-information-uk', 'dyscalculia-information-and-support-uk']), ('Games & downtime', ['low-time-pressure-games'])]
_compat08__QUESTION_GROUPS = _compat09__QUESTION_GROUPS
_compat09__HUB_DEFINITIONS = [('needs/daily-life', 'Daily life', 'Start with practical everyday tasks: getting started, routines, technology, planning and ordinary activities.', {'Daily life & technology', 'Games & downtime'}), ('needs/sensory-environment', 'Sensory & environment', 'Find governed routes about sensory load, noisy or bright places, overload and changing the environment around a person.', {'Sensory & environment'}), ('needs/communication', 'Communication', 'Find routes for phone calls, processing time, speaking, AAC and communication access without assuming one communication style fits everyone.', {'Communication'}), ('needs/work', 'Work', 'Find workplace support, adjustments, disclosure, interviews, job-search support and Access to Work routes.', {'Work'}), ('needs/education-study', 'Education & study', 'Find study organisation, disabled-student support, SEND information and education access routes.', {'Education & study'}), ('needs/assessment-diagnosis', 'Assessment & diagnosis', 'Find bounded information about assessment and diagnosis routes without turning ND Oracle into a diagnostic test.', {'Assessment & diagnosis'}), ('needs/health-wellbeing', 'Health & wellbeing', 'Find current routes around anxiety, sleep, food-related task demands, burnout and wellbeing while keeping clinical boundaries visible.', {'Health & wellbeing'}), ('needs/relationships-family', 'Relationships & family', 'Find routes relevant to family life, parenting and relationships where the present catalogue has governed material.', {'Relationships & family'})]
_compat09__NAVIGATION_ROUTES = ('/needs/', '/needs/daily-life/', '/needs/sensory-environment/', '/needs/communication/', '/needs/work/', '/needs/education-study/', '/needs/assessment-diagnosis/', '/needs/health-wellbeing/', '/needs/relationships-family/', '/types/', '/places/', '/a-z/')
_compat09__V09_ROUTE_COUNT = 125
def _compat09__validate_question_navigation(questions: list[dict]) -> None:
    _compat08__QUESTION_GROUPS = _compat09__QUESTION_GROUPS
    _compat08__validate_question_navigation(questions)
def _compat09___append_before_main_end(page: str, section: str) -> str:
    marker = '</main>'
    if marker not in page:
        raise ValueError('Cannot locate page main element')
    return page.replace(marker, section + marker, 1)
def _compat09__render_index(concepts: list[dict], resources: list[dict], questions: list[dict] | None=None) -> str:
    if questions is None:
        questions = _compat08__load_questions()
    _compat09__validate_question_navigation(questions)
    page = _compat08__render_index(concepts, resources, questions)
    browse = '\n<section class="start-section" aria-labelledby="browse-whole-heading">\n  <h2 id="browse-whole-heading">Browse the whole knowledge base</h2>\n  <p class="section-intro">Use needs, content type, geographic scope or the complete A–Z when you do not want to start from a diagnosis.</p>\n  <ul class="question-list">\n    <li><a href="/needs/">Browse by need</a></li>\n    <li><a href="/types/">Browse by content type</a></li>\n    <li><a href="/places/">Browse by geographic scope</a></li>\n    <li><a href="/a-z/">A–Z of all governed content</a></li>\n  </ul>\n</section>\n'
    return _compat09___append_before_main_end(page, browse)
def _compat09__render_questions_index(questions: list[dict]) -> str:
    _compat09__validate_question_navigation(questions)
    page = _compat08__render_questions_index(questions)
    browse = '\n<section aria-labelledby="question-browse-heading">\n  <h2 id="question-browse-heading">Other ways to browse</h2>\n  <p><a href="/needs/">Browse practical needs and life areas</a> · <a href="/a-z/">A–Z of all content</a></p>\n</section>\n'
    return _compat09___append_before_main_end(page, browse)
def _compat09__related_questions(question: dict, questions: list[dict], limit: int=5) -> list[dict]:
    refs = {(ref.get('type'), ref.get('id')) for ref in question.get('related_objects', [])}
    ranked: list[tuple[int, str, dict]] = []
    for candidate in questions:
        if candidate['id'] == question['id']:
            continue
        candidate_refs = {(ref.get('type'), ref.get('id')) for ref in candidate.get('related_objects', [])}
        score = len(refs & candidate_refs)
        if score:
            ranked.append((-score, candidate['question'].casefold(), candidate))
    ranked.sort(key=lambda item: (item[0], item[1]))
    return [item[2] for item in ranked[:limit]]
def _compat09__render_question(question: dict, concept_map: dict[str, dict], resource_map: dict[str, dict], questions: list[dict] | None=None) -> str:
    if questions is None:
        questions = _compat08__load_questions()
    page = _compat08__render_question(question, concept_map, resource_map)
    related = _compat09__related_questions(question, questions)
    if related:
        items = ''.join((f"""<li><a href="/questions/{_compat06__esc(item['id'])}/">{_compat06__esc(item['question'])}</a></li>""" for item in related))
    else:
        items = '<li>No adjacent governed question has enough shared material yet.</li>'
    section = f'\n<section aria-labelledby="related-questions-heading">\n  <h2 id="related-questions-heading">Related questions</h2>\n  <ul>{items}</ul>\n</section>\n'
    marker = '<section aria-labelledby="evidence-needed-heading">'
    if marker not in page:
        raise ValueError(f"{question['id']}: cannot locate evidence-needed section")
    return page.replace(marker, section + marker, 1)
def _compat09__resource_scope(resource: dict) -> tuple[str, str]:
    audience = str(resource.get('audience_or_context', '')).casefold()
    whole = ' '.join([str(resource.get('description', '')), str(resource.get('audience_or_context', '')), *[str(item) for item in resource.get('limitations', [])], *[str(item) for item in resource.get('cost_or_access_notes', [])]]).casefold()
    if 'great britain' in audience or 'england, scotland and wales' in audience:
        return ('Great Britain', 'The reviewed audience/scope text identifies England, Scotland and Wales or Great Britain. Northern Ireland may use different routes.')
    if 'northern ireland' in audience and 'england' not in audience and ('scotland' not in audience) and ('wales' not in audience):
        return ('Northern Ireland', 'The reviewed audience/scope text specifically identifies Northern Ireland.')
    if 'england' in audience and 'scotland' not in audience and ('wales' not in audience):
        return ('England', 'The reviewed audience/scope text specifically identifies England.')
    if 'united kingdom' in audience or ' uk ' in f' {audience} ' or 'uk-wide' in whole:
        return ('United Kingdom', 'The reviewed listing describes a UK-wide or United Kingdom audience/scope.')
    return ('International / not jurisdiction-specific', 'No narrower UK jurisdiction is asserted by the reviewed audience text; check the resource itself for local availability and eligibility.')
def _compat09__render_resource(resource: dict, concept_map: dict[str, dict], questions: list[dict]) -> str:
    page = _compat08__render_resource(resource, concept_map, questions)
    label, explanation = _compat09__resource_scope(resource)
    category = _compat06__RESOURCE_CATEGORY_LABELS.get(resource['category'], resource['category'].replace('_', ' ').title())
    section = f'\n<section aria-labelledby="scope-heading">\n  <h2 id="scope-heading">Scope for navigation</h2>\n  <p><strong>{_compat06__esc(label)}</strong> · {_compat06__esc(category)}</p>\n  <p class="meta">{_compat06__esc(explanation)} This label helps navigation; it is not an eligibility or legal determination.</p>\n  <p><a href="/places/">Browse resources by place</a> · <a href="/types/">Browse by content type</a></p>\n</section>\n'
    marker = '<section aria-labelledby="limits-heading">'
    if marker not in page:
        raise ValueError(f"{resource['id']}: cannot locate limitations section")
    return page.replace(marker, section + marker, 1)
def _compat09__render_resources_index(resources: list[dict]) -> str:
    page = _compat08__render_resources_index(resources)
    section = '\n<section aria-labelledby="resource-browse-heading">\n  <h2 id="resource-browse-heading">Browse the catalogue</h2>\n  <p><a href="/types/">By content type</a> · <a href="/places/">By geographic scope</a> · <a href="/a-z/">A–Z</a></p>\n</section>\n'
    return _compat09___append_before_main_end(page, section)
def _compat09___question_map(questions: list[dict]) -> dict[str, dict]:
    return {question['id']: question for question in questions}
def _compat09___questions_for_groups(questions: list[dict], group_names: set[str]) -> list[dict]:
    mapping = _compat09___question_map(questions)
    ids = [question_id for group, group_ids in _compat09__QUESTION_GROUPS if group in group_names for question_id in group_ids]
    return [mapping[question_id] for question_id in ids]
def _compat09___linked_content_from_questions(questions: list[dict], concept_map: dict[str, dict], resource_map: dict[str, dict]) -> tuple[list[dict], list[dict]]:
    concept_ids: set[str] = set()
    resource_ids: set[str] = set()
    for question in questions:
        for ref in question.get('related_objects', []):
            if ref.get('type') == 'concept' and ref.get('id') in concept_map:
                concept_ids.add(ref['id'])
            if ref.get('type') == 'resource' and ref.get('id') in resource_map:
                resource_ids.add(ref['id'])
    concepts = sorted((concept_map[item] for item in concept_ids), key=lambda item: item['name'].casefold())
    resources = sorted((resource_map[item] for item in resource_ids), key=lambda item: item['name'].casefold())
    return (concepts, resources)
def _compat09__render_need_hub(route: str, title: str, intro: str, group_names: set[str], questions: list[dict], concept_map: dict[str, dict], resource_map: dict[str, dict]) -> str:
    selected = _compat09___questions_for_groups(questions, group_names)
    concepts, resources = _compat09___linked_content_from_questions(selected, concept_map, resource_map)
    question_rows = ''.join((_compat08__question_link(question) for question in selected))
    concept_items = ''.join((f"""<li><a href="/understand/{_compat06__esc(item['id'])}/">{_compat06__esc(item['name'])}</a></li>""" for item in concepts)) or '<li>No topic link is recorded yet.</li>'
    resource_items = ''.join((f"""<li><a href="/resources/{_compat06__esc(item['id'])}/">{_compat06__esc(item['name'])}</a></li>""" for item in resources)) or '<li>No resource link is recorded yet.</li>'
    body = f'\n<p class="back-link"><a href="/needs/">← All needs</a></p>\n<section class="notice"><strong>Relevant to inspect, not recommended.</strong> This hub groups governed routes; it does not infer a diagnosis or choose support for an individual.</section>\n<section aria-labelledby="need-questions-heading">\n  <h2 id="need-questions-heading">Practical questions</h2>\n  <div class="topic-list">{question_rows}</div>\n</section>\n<section aria-labelledby="need-topics-heading"><h2 id="need-topics-heading">Related topics</h2><ul>{concept_items}</ul></section>\n<section aria-labelledby="need-resources-heading"><h2 id="need-resources-heading">Related resources</h2><ul>{resource_items}</ul></section>\n'
    return _compat08__page_shell(title, intro, body, current='questions', path=f'/{route}/')
def _compat09__render_needs_index(questions: list[dict]) -> str:
    _compat09__validate_question_navigation(questions)
    question_map = _compat09___question_map(questions)
    hub_by_group = {group: (route, title) for route, title, _intro, groups in _compat09__HUB_DEFINITIONS for group in groups}
    sections = []
    for group, ids in _compat09__QUESTION_GROUPS:
        if group in hub_by_group:
            route, title = hub_by_group[group]
            heading = f'<h2><a href="/{_compat06__esc(route)}/">{_compat06__esc(title)}</a></h2>'
        else:
            heading = f'<h2>{_compat06__esc(group)}</h2>'
        links = ''.join((f"""<li><a href="/questions/{_compat06__esc(question_id)}/">{_compat06__esc(question_map[question_id]['question'])}</a></li>""" for question_id in ids))
        sections.append(f'<section>{heading}<ul>{links}</ul></section>')
    body = f"""\n<section class="notice"><strong>Start with the need, not the label.</strong> Every current governed Question appears here exactly once in its primary navigation group.</section>\n{''.join(sections)}\n"""
    return _compat08__page_shell('Browse by need', 'Start from the problem or life area you are dealing with, then follow governed questions into topics and resources.', body, current='questions', path='/needs/')
def _compat09__render_types_index(concepts: list[dict], resources: list[dict], questions: list[dict]) -> str:
    sections = [f'<section><h2>Questions</h2><p>{len(questions)} governed practical questions.</p><p><a href="/questions/">Browse Questions</a></p></section>', f'<section><h2>Topics</h2><p>{len(concepts)} reviewed Concepts.</p><p><a href="/understand/">Browse Topics</a></p></section>']
    grouped: dict[str, list[dict]] = defaultdict(list)
    for resource in resources:
        grouped[resource['category']].append(resource)
    preferred = ['organisation', 'service', 'community', 'tool', 'app', 'practical_guide', 'education_work_resource', 'accommodation', 'game', 'book', 'media', 'product', 'other']
    for category in preferred:
        items = sorted(grouped.get(category, []), key=lambda item: item['name'].casefold())
        if not items:
            continue
        label = _compat06__RESOURCE_CATEGORY_LABELS.get(category, category.replace('_', ' ').title())
        links = ''.join((f"""<li><a href="/resources/{_compat06__esc(item['id'])}/">{_compat06__esc(item['name'])}</a></li>""" for item in items))
        sections.append(f'<section><h2>{_compat06__esc(label)}</h2><ul>{links}</ul></section>')
    return _compat08__page_shell('Browse by content type', 'Separate Questions, Topics, organisations, services, tools, apps, games, books, guides and other governed resources.', ''.join(sections), current='resources', path='/types/')
def _compat09__render_places_index(resources: list[dict]) -> str:
    grouped: dict[str, list[dict]] = defaultdict(list)
    explanations: dict[str, str] = {}
    for resource in resources:
        label, explanation = _compat09__resource_scope(resource)
        grouped[label].append(resource)
        explanations[label] = explanation
    order = ['United Kingdom', 'Great Britain', 'England', 'Northern Ireland', 'International / not jurisdiction-specific']
    sections = []
    for label in order:
        items = sorted(grouped.get(label, []), key=lambda item: item['name'].casefold())
        if not items:
            continue
        links = ''.join((f"""<li><a href="/resources/{_compat06__esc(item['id'])}/">{_compat06__esc(item['name'])}</a></li>""" for item in items))
        sections.append(f'<section><h2>{_compat06__esc(label)}</h2><p class="meta">{_compat06__esc(explanations[label])}</p><ul>{links}</ul></section>')
    body = '<section class="notice"><strong>Navigation scope, not eligibility.</strong> These groups are derived from each reviewed listing\'s audience and limitation text. Always check the resource itself for current jurisdiction and eligibility.</section>' + ''.join(sections)
    return _compat08__page_shell('Browse by geographic scope', 'Distinguish UK, Great Britain, England, Northern Ireland and resources without a narrower jurisdictional scope.', body, current='resources', path='/places/')
def _compat09___az_letter(label: str) -> str:
    for character in label.strip():
        if character.isalnum():
            return character.upper()
    return '#'
def _compat09__render_az_index(concepts: list[dict], resources: list[dict], questions: list[dict]) -> str:
    entries: list[tuple[str, str, str]] = []
    entries.extend(((item['name'], 'Topic', f"/understand/{item['id']}/") for item in concepts))
    entries.extend(((item['name'], 'Resource', f"/resources/{item['id']}/") for item in resources))
    entries.extend(((item['question'], 'Question', f"/questions/{item['id']}/") for item in questions))
    entries.sort(key=lambda item: item[0].casefold())
    grouped: dict[str, list[tuple[str, str, str]]] = defaultdict(list)
    for entry in entries:
        grouped[_compat09___az_letter(entry[0])].append(entry)
    sections = []
    for letter in sorted(grouped, key=lambda value: (value == '#', value)):
        links = ''.join((f'<li><a href="{_compat06__esc(route)}">{_compat06__esc(label)}</a> <span class="meta">{_compat06__esc(kind)}</span></li>' for label, kind, route in grouped[letter]))
        sections.append(f'<section><h2>{_compat06__esc(letter)}</h2><ul>{links}</ul></section>')
    return _compat08__page_shell('A–Z', f'All {len(entries)} governed Topics, Resources and Questions in one alphabetical index.', ''.join(sections), current='resources', path='/a-z/')
def _compat09__sitemap_paths(concepts: list[dict], resources: list[dict] | None=None, questions: list[dict] | None=None) -> list[str]:
    if resources is None:
        resources = _compat06__load_resources()
    if questions is None:
        questions = _compat08__load_questions()
    _compat09__validate_question_navigation(questions)
    paths = list(_compat08__sitemap_paths(concepts, resources, questions))
    paths.extend(_compat09__NAVIGATION_ROUTES)
    if len(paths) != len(set(paths)):
        raise ValueError('v0.9 sitemap contains duplicate routes')
    return paths
def _compat09__render_sitemap(concepts: list[dict], resources: list[dict], questions: list[dict] | None=None) -> str:
    if questions is None:
        questions = _compat08__load_questions()
    urls = ''.join((f'  <url><loc>{html.escape(_compat06__PUBLIC_ORIGIN + path)}</loc></url>\n' for path in _compat09__sitemap_paths(concepts, resources, questions)))
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n'
def _compat09__build(output_dir=_compat06__DEFAULT_OUTPUT_DIR):
    questions = _compat08__load_questions()
    _compat09__validate_question_navigation(questions)
    destination = _compat08__build(output_dir)
    concepts = _compat06__load_concepts()
    resources = _compat06__load_resources()
    concept_map = {item['id']: item for item in concepts}
    resource_map = {item['id']: item for item in resources}
    (destination / 'index.html').write_text(_compat09__render_index(concepts, resources, questions), encoding='utf-8')
    _compat06__write_route(destination, 'questions', _compat09__render_questions_index(questions))
    _compat06__write_route(destination, 'resources', _compat09__render_resources_index(resources))
    for question in questions:
        _compat06__write_route(destination, f"questions/{question['id']}", _compat09__render_question(question, concept_map, resource_map, questions))
    for resource in resources:
        _compat06__write_route(destination, f"resources/{resource['id']}", _compat09__render_resource(resource, concept_map, questions))
    _compat06__write_route(destination, 'needs', _compat09__render_needs_index(questions))
    for route, title, intro, groups in _compat09__HUB_DEFINITIONS:
        _compat06__write_route(destination, route, _compat09__render_need_hub(route, title, intro, groups, questions, concept_map, resource_map))
    _compat06__write_route(destination, 'types', _compat09__render_types_index(concepts, resources, questions))
    _compat06__write_route(destination, 'places', _compat09__render_places_index(resources))
    _compat06__write_route(destination, 'a-z', _compat09__render_az_index(concepts, resources, questions))
    paths = _compat09__sitemap_paths(concepts, resources, questions)
    if len(paths) != _compat09__V09_ROUTE_COUNT:
        raise ValueError(f'Expected {_compat09__V09_ROUTE_COUNT} v0.9 canonical routes, found {len(paths)}')
    (destination / 'sitemap.xml').write_text(_compat09__render_sitemap(concepts, resources, questions), encoding='utf-8')
    return destination

# ---- current v1.0 builder ----
if __package__ in {None, ''}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
EVIDENCE_DIR = _compat06__ROOT / 'objects' / 'evidence'
V10_ROUTE_COUNT = 148
QUESTION_GROUPS = [('Daily life & technology', ['task-starting-and-organisation', 'make-device-easier-to-use', 'meal-planning-and-everyday-food-tasks']), ('Sensory & environment', ['make-noisy-bright-place-easier', 'sensory-overload-what-can-i-change']), ('Communication', ['aac-and-nonspeaking-communication', 'phone-calls-are-difficult', 'processing-time-in-conversations-meetings']), ('Work', ['workplace-support-great-britain', 'reasonable-adjustments-at-work-great-britain', 'disabled-person-looking-for-work-uk', 'disclosing-disability-neurodivergence-at-work', 'job-interview-adjustments-great-britain']), ('Education & study', ['disabled-student-support-england', 'disabled-student-support-scotland', 'disabled-student-support-wales', 'disabled-student-support-northern-ireland', 'organising-study-and-assignments', 'send-support-school-college-england']), ('Assessment & diagnosis', ['adult-adhd-assessment-england', 'adult-autism-assessment-england']), ('Health & wellbeing', ['autism-anxiety-tools', 'masking-exhaustion-and-autistic-burnout', 'sleep-and-winding-down-routines', 'healthcare-communication-adjustments-england']), ('Relationships & family', ['autistic-parent-support-uk', 'communication-needs-in-relationships', 'neurodivergent-parent-overwhelmed-by-admin']), ('Money & administration', ['disability-benefits-where-start-uk']), ('Mobility & travel', ['adhd-driving-dvla-great-britain', 'disabled-travel-support-scotland', 'disabled-travel-support-wales', 'disabled-travel-support-northern-ireland']), ('Information & support', ['autism-information-and-support', 'dyslexia-information-and-support-uk', 'tourette-information-and-support-uk', 'learning-disability-information-and-support-uk', 'dld-information-and-support', 'adult-dyspraxia-information-uk', 'dyscalculia-information-and-support-uk']), ('Games & downtime', ['low-time-pressure-games'])]
_compat09__QUESTION_GROUPS = QUESTION_GROUPS
_compat08__QUESTION_GROUPS = QUESTION_GROUPS
_compat09__V09_ROUTE_COUNT = 147
def load_evidence() -> list[dict]:
    if not EVIDENCE_DIR.is_dir():
        return []
    items = []
    for path in sorted(EVIDENCE_DIR.glob('*.json')):
        items.append(json.loads(path.read_text(encoding='utf-8')))
    return sorted(items, key=lambda item: item['title'].casefold())
def validate_question_navigation(questions: list[dict]) -> None:
    question_ids = {item['id'] for item in questions}
    grouped = [item for _group, ids in QUESTION_GROUPS for item in ids]
    if len(grouped) != len(set(grouped)):
        raise ValueError('Question navigation groups contain duplicates')
    if set(grouped) != question_ids:
        raise ValueError(f'v1.0 Question groups must exactly cover current Questions: missing={sorted(question_ids - set(grouped))}; unexpected={sorted(set(grouped) - question_ids)}')
    _compat09__validate_question_navigation(questions)
def resource_scope(resource: dict) -> tuple[str, str]:
    audience = str(resource.get('audience_or_context', '')).casefold()
    whole = ' '.join([str(resource.get('description', '')), audience, *[str(item) for item in resource.get('limitations', [])]]).casefold()
    if 'great britain' in audience or 'england, scotland and wales' in audience:
        return ('Great Britain', 'The reviewed scope identifies Great Britain (England, Scotland and Wales); Northern Ireland may use a different system.')
    if ('england or wales' in audience or 'england and wales' in audience) and 'scotland' not in audience:
        return ('England and Wales', 'The reviewed scope specifically identifies England and Wales.')
    if 'northern ireland' in audience and all((term not in audience for term in ('england', 'scotland', 'wales'))):
        return ('Northern Ireland', 'The reviewed scope specifically identifies Northern Ireland.')
    if 'scotland' in audience and all((term not in audience for term in ('england', 'wales', 'northern ireland'))):
        return ('Scotland', 'The reviewed scope specifically identifies Scotland.')
    if 'wales' in audience and all((term not in audience for term in ('england', 'scotland', 'northern ireland'))):
        return ('Wales', 'The reviewed scope specifically identifies Wales.')
    if 'england' in audience and all((term not in audience for term in ('scotland', 'wales', 'northern ireland'))):
        return ('England', 'The reviewed scope specifically identifies England.')
    if 'united kingdom' in audience or ' uk ' in f' {audience} ' or 'uk-wide' in whole:
        return ('United Kingdom', 'The reviewed listing describes a UK-wide or United Kingdom scope.')
    return ('International / not jurisdiction-specific', 'No narrower UK jurisdiction is asserted by the reviewed scope; check the resource itself for local availability and eligibility.')
_compat09__resource_scope = resource_scope
def _evidence_contribution(evidence: dict, claim_ref: str) -> dict | None:
    for item in evidence.get('contributions', []):
        if item.get('claim_ref') == claim_ref:
            return item
    return None
def render_governed_resource_claims(resource: dict, evidence_map: dict[str, dict]) -> str:
    claims = resource.get('claims', [])
    if not claims:
        return ''
    rows = []
    for claim in claims:
        claim_ref = f"{resource['id']}#{claim['id']}"
        evidence_rows = []
        for evidence_id in claim.get('evidence_ids', []):
            evidence = evidence_map.get(evidence_id)
            if evidence is None:
                raise ValueError(f'{claim_ref}: missing evidence {evidence_id}')
            contribution = _evidence_contribution(evidence, claim_ref)
            if contribution is None:
                raise ValueError(f'{evidence_id}: missing contribution for {claim_ref}')
            locator = evidence.get('locator', {})
            raw_url = locator.get('value') if locator.get('type') == 'url' else None
            citation = _compat06__esc(evidence['citation'])
            if raw_url and _compat06__safe_http_url(raw_url):
                citation = f'<a href="{_compat06__esc(raw_url)}">{citation}</a>'
            limits = _compat06__list_items([item['text'] for item in contribution.get('limitations', [])])
            evidence_rows.append(f"""<article class="evidence-card"><h4>{_compat06__esc(evidence['title'])}</h4><p>{citation}</p><p><strong>Finding used here:</strong> {_compat06__esc(contribution['finding'])}</p><p class="meta">Context: {_compat06__esc(contribution['population_or_context'])} · Method: {_compat06__esc(contribution['methodology'])}</p><div><strong>Evidence limitations</strong>{limits}</div></article>""")
        uncertainty_rows = ''.join((f"""<li id="uncertainty-{_compat06__esc(item['id'])}"><strong>{_compat06__esc(item['text'])}</strong><br><span class="meta">Why it matters: {_compat06__esc(item['why_it_matters'])}</span></li>""" for item in claim.get('uncertainties', [])))
        confidence = claim['confidence'].replace('_', ' ').title()
        rows.append(f"""<article class="claim-card" id="claim-{_compat06__esc(claim['id'])}"><h3>{_compat06__esc(claim['text'])}</h3><p class="meta">Confidence: <a href="/how-it-works/#confidence">{_compat06__esc(confidence)}</a></p><h4>Evidence route</h4>{''.join(evidence_rows)}<h4>Uncertainty and limits</h4><ul>{uncertainty_rows}</ul></article>""")
    return '<section aria-labelledby="governed-resource-claims-heading"><h2 id="governed-resource-claims-heading">Governed claims and evidence</h2><section class="notice"><strong>A supported claim is not a recommendation or an individual decision.</strong> Read the exact wording, evidence context and open uncertainty together.</section>' + ''.join(rows) + '</section>'
def render_resource(resource: dict, concept_map: dict[str, dict], questions: list[dict], evidence_map: dict[str, dict] | None=None) -> str:
    page = _compat09__render_resource(resource, concept_map, questions)
    if evidence_map is None:
        evidence_map = {item['id']: item for item in load_evidence()}
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
    order = ['United Kingdom', 'Great Britain', 'England and Wales', 'England', 'Scotland', 'Wales', 'Northern Ireland', 'International / not jurisdiction-specific']
    sections = []
    for label in order:
        items = sorted(grouped.get(label, []), key=lambda item: item['name'].casefold())
        if not items:
            continue
        links = ''.join((f"""<li><a href="/resources/{_compat06__esc(item['id'])}/">{_compat06__esc(item['name'])}</a></li>""" for item in items))
        sections.append(f'<section><h2>{_compat06__esc(label)}</h2><p class="meta">{_compat06__esc(explanations[label])}</p><ul>{links}</ul></section>')
    body = '<section class="notice"><strong>Navigation scope, not eligibility.</strong> These groups come from reviewed audience/scope text. UK-wide, Great Britain, England and Wales, England, Scotland, Wales and Northern Ireland are kept distinct where the governed material supports that distinction.</section>' + ''.join(sections)
    return _compat08__page_shell('Browse by geographic scope', 'Distinguish national and jurisdiction-specific support instead of treating every UK route as interchangeable.', body, current='resources', path='/places/')
FIND_JS = '(() => {\n  "use strict";\n  const input = document.getElementById("find-input");\n  const button = document.getElementById("find-button");\n  const output = document.getElementById("find-results");\n  const raw = document.getElementById("search-index").content.textContent;\n  const index = JSON.parse(raw);\n  const stop = new Set(["a","an","and","are","can","do","for","i","in","is","it","me","my","of","on","or","the","to","what","with","you","your"]);\n  const refusals = ["diagnose me","am i autistic","do i have autism","do i have adhd","what medication dose","what dose should i take","stop my medication","which medication should i take","tell me if i am autistic","tell me if i have adhd"];\n  const norm = s => (s || "").toLowerCase().match(/[a-z0-9]+/g)?.join(" ") || "";\n  const tokens = s => norm(s).split(" ").filter(t => t.length > 1 && !stop.has(t));\n  function score(query, record) {\n    const qn = norm(query); const qt = new Set(tokens(query));\n    const tn = norm(record.title); const bn = norm(record.body); let s = 0;\n    if (qn === tn) s += 120; else if (tn.includes(qn)) s += 55;\n    if (bn.includes(qn)) s += 20;\n    const tt = new Set(tokens(record.title)); const bt = new Set(tokens(record.body));\n    qt.forEach(t => { if (tt.has(t)) s += 12; if (bt.has(t)) s += 3; });\n    (record.intent || []).forEach(p => { const pn = norm(p); const pt = new Set(tokens(p));\n      if (qn === pn) s += 100; else if (pn.includes(qn) || qn.includes(pn)) s += 45;\n      qt.forEach(t => { if (pt.has(t)) s += 9; });\n    });\n    return s;\n  }\n  function run() {\n    const query = input.value.trim(); output.replaceChildren();\n    if (!query) { output.textContent = "Type a problem or question first."; return; }\n    const qn = norm(query);\n    if (refusals.some(p => qn.includes(p))) {\n      output.innerHTML = \'<h2>No governed answer</h2><p>ND Oracle cannot diagnose you, choose medication or make an individual clinical decision. Try browsing <a href="/questions/">Questions</a> or <a href="/needs/">needs</a> instead.</p>\';\n      return;\n    }\n    const ranked = index.map(r => [score(query,r),r]).filter(x => x[0] >= 12)\n      .sort((a,b) => b[0]-a[0] || a[1].kind.localeCompare(b[1].kind) || a[1].title.localeCompare(b[1].title)).slice(0,5);\n    if (!ranked.length) {\n      output.innerHTML = \'<h2>No governed answer yet</h2><p>The current catalogue does not have a strong enough route for that wording. Your query is not stored or sent to a search service. Try <a href="/needs/">browse by need</a>, <a href="/a-z/">A–Z</a>, or report a non-private content gap through <a href="/feedback/">feedback</a>.</p>\';\n      return;\n    }\n    const h = document.createElement("h2"); h.textContent = "Governed routes to inspect"; output.appendChild(h);\n    const note = document.createElement("p"); note.className="meta"; note.textContent="Ranked locally from reviewed ND Oracle content. Relevance is not recommendation."; output.appendChild(note);\n    const list = document.createElement("ol");\n    ranked.forEach(([s,r]) => { const li=document.createElement("li"); const a=document.createElement("a"); a.href=r.route; a.textContent=r.title; li.appendChild(a); const m=document.createElement("span"); m.className="meta"; m.textContent=` ${r.kind}`; li.appendChild(m); list.appendChild(li); });\n    output.appendChild(list);\n  }\n  button.addEventListener("click", run);\n  input.addEventListener("keydown", e => { if (e.key === "Enter") { e.preventDefault(); run(); } });\n})();\n'
def render_find_page() -> str:
    index_json = html.escape(discovery.browser_index_json())
    body = f'\n<section class="notice"><strong>Local governed discovery.</strong> Your words stay in this browser page. ND Oracle does not submit the query to a server, AI model, analytics system or search provider.</section>\n<section aria-labelledby="find-heading">\n  <h2 id="find-heading">Describe the problem in your own words</h2>\n  <label for="find-input">Problem or question</label>\n  <input id="find-input" type="search" autocomplete="off" spellcheck="true" maxlength="500">\n  <button id="find-button" type="button">Find governed routes</button>\n  <p class="meta">Examples: “work is too noisy”, “I keep putting off paperwork”, “phone calls are hard”.</p>\n</section>\n<section id="find-results" aria-live="polite" aria-atomic="false"><p>Results will appear here. Relevance means worth inspecting, not recommended.</p></section>\n<noscript><section><h2>Discovery needs JavaScript</h2><p>The rest of ND Oracle works without JavaScript. Use <a href="/questions/">Questions</a>, <a href="/needs/">browse by need</a> or the <a href="/a-z/">A–Z</a> instead.</p></section></noscript>\n<template id="search-index">{index_json}</template>\n<script src="/find.js" defer></script>\n'
    return _compat08__page_shell('Find a governed route', 'Start with ordinary language. Matching happens locally in your browser and points only to governed ND Oracle pages.', body, current=None, path='/find/')
def _append_before_main_end(page: str, section: str) -> str:
    if '</main>' not in page:
        raise ValueError('Cannot locate main element')
    return page.replace('</main>', section + '</main>', 1)
def sitemap_paths(concepts: list[dict], resources: list[dict] | None=None, questions: list[dict] | None=None) -> list[str]:
    if resources is None:
        resources = _compat06__load_resources()
    if questions is None:
        questions = _compat08__load_questions()
    paths = list(_compat09__sitemap_paths(concepts, resources, questions))
    paths.append('/find/')
    if len(paths) != len(set(paths)):
        raise ValueError('v1.0 sitemap contains duplicate routes')
    return paths
def render_sitemap(concepts: list[dict], resources: list[dict], questions: list[dict] | None=None) -> str:
    if questions is None:
        questions = _compat08__load_questions()
    urls = ''.join((f'  <url><loc>{html.escape(_compat06__PUBLIC_ORIGIN + path)}</loc></url>\n' for path in sitemap_paths(concepts, resources, questions)))
    return '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + '</urlset>\n'
def build(output_dir=_compat06__DEFAULT_OUTPUT_DIR):
    questions = _compat08__load_questions()
    validate_question_navigation(questions)
    destination = _compat09__build(output_dir)
    concepts = _compat06__load_concepts()
    resources = _compat06__load_resources()
    evidence = load_evidence()
    concept_map = {item['id']: item for item in concepts}
    evidence_map = {item['id']: item for item in evidence}
    for resource in resources:
        _compat06__write_route(destination, f"resources/{resource['id']}", render_resource(resource, concept_map, questions, evidence_map))
    _compat06__write_route(destination, 'places', render_places_index(resources))
    _compat06__write_route(destination, 'find', render_find_page())
    (destination / 'find.js').write_text((_compat06__ROOT / 'scripts' / 'discovery_browser.js').read_text(encoding='utf-8'), encoding='utf-8')
    home = (destination / 'index.html').read_text(encoding='utf-8')
    find_section = '<section class="start-section" aria-labelledby="find-oracle-heading"><h2 id="find-oracle-heading">Describe the problem in your own words</h2><p>Use local governed discovery when you do not know the name of the Topic, Question or Resource you need.</p><p><a href="/find/">Find a governed route →</a></p></section>'
    (destination / 'index.html').write_text(_append_before_main_end(home, find_section), encoding='utf-8')
    for route, section in {'privacy': '<section><h2>Local discovery privacy</h2><p>The /find/ tool ranks the static governed catalogue in your browser. Query text is not submitted in a URL, sent to an AI or search service, stored by ND Oracle, or used for analytics. The page itself and its local script are served like other static site files.</p></section>', 'how-it-works': '<section><h2>Governed discovery</h2><p>The /find/ tool uses deterministic local text and editorial-intent matching. It can rank governed routes, but it cannot create a new fact, diagnose a person or convert relevance into a recommendation. If no route clears the threshold, it says that the catalogue does not have a governed answer yet.</p></section>'}.items():
        path = destination / route / 'index.html'
        path.write_text(_append_before_main_end(path.read_text(encoding='utf-8'), section), encoding='utf-8')
    headers = (destination / '_headers').read_text(encoding='utf-8')
    headers = headers.replace("script-src 'none'", "script-src 'self'")
    (destination / '_headers').write_text(headers, encoding='utf-8')
    paths = sitemap_paths(concepts, resources, questions)
    if len(paths) != V10_ROUTE_COUNT:
        raise ValueError(f'Expected {V10_ROUTE_COUNT} v1.0 canonical routes, found {len(paths)}')
    (destination / 'sitemap.xml').write_text(render_sitemap(concepts, resources, questions), encoding='utf-8')
    return destination

# Public compatibility names retained for callers/tests.
BOOK_MEDIA_CATEGORIES = _compat09__BOOK_MEDIA_CATEGORIES
COMMON_QUESTIONS = _compat09__COMMON_QUESTIONS
COMMUNITY_CATEGORIES = _compat06__COMMUNITY_CATEGORIES
DEFAULT_OUTPUT_DIR = _compat06__DEFAULT_OUTPUT_DIR
FEATURED_QUESTION_IDS = _compat09__FEATURED_QUESTION_IDS
HUB_DEFINITIONS = _compat09__HUB_DEFINITIONS
INDEXED_STATIC_PAGES = _compat06__INDEXED_STATIC_PAGES
NAVIGATION_ROUTES = _compat09__NAVIGATION_ROUTES
OBJECTS_DIR = _compat06__OBJECTS_DIR
OUTPUT_MARKER = _compat06__OUTPUT_MARKER
PRIMARY_NAV = _compat08__PRIMARY_NAV
PUBLIC_ORIGIN = _compat06__PUBLIC_ORIGIN
QUESTIONS_DIR = _compat09__QUESTIONS_DIR
QUESTION_DISCOVERY_ABOUT_SECTION = _compat08__QUESTION_DISCOVERY_ABOUT_SECTION
QUESTION_DISCOVERY_HOW_SECTION = _compat08__QUESTION_DISCOVERY_HOW_SECTION
RESOURCES_DIR = _compat06__RESOURCES_DIR
RESOURCE_CATEGORY_LABELS = _compat06__RESOURCE_CATEGORY_LABELS
ROOT = _compat06__ROOT
SIMPLE_EXPLANATIONS = _compat09__SIMPLE_EXPLANATIONS
SITE_DIR = _compat06__SITE_DIR
STATIC_PAGES = _compat08__STATIC_PAGES
TOOL_CATEGORIES = _compat06__TOOL_CATEGORIES
V07_HOMEPAGE_COMPAT_QUESTION_IDS = _compat09__V07_HOMEPAGE_COMPAT_QUESTION_IDS
V09_COMMON_QUESTIONS = _compat09__V09_COMMON_QUESTIONS
V09_ROUTE_COUNT = _compat09__V09_ROUTE_COUNT
V09_SIMPLE_EXPLANATIONS = _compat09__V09_SIMPLE_EXPLANATIONS
esc = _compat06__esc
human_date = _compat06__human_date
list_items = _compat06__list_items
load_concepts = _compat06__load_concepts
load_questions = _compat08__load_questions
load_resources = _compat06__load_resources
nav = _compat06__nav
page_shell = _compat08__page_shell
prepare_output = _compat06__prepare_output
question_link = _compat08__question_link
reader_intro = _compat06__reader_intro
related_questions = _compat09__related_questions
render_az_index = _compat09__render_az_index
render_books_media_index = _compat08__render_books_media_index
render_concept = _compat08__render_concept
render_index = _compat09__render_index
render_need_hub = _compat09__render_need_hub
render_needs_index = _compat09__render_needs_index
render_not_found = _compat06__render_not_found
render_question = _compat09__render_question
render_questions_index = _compat09__render_questions_index
render_resource_collection = _compat08__render_resource_collection
render_resources_index = _compat09__render_resources_index
render_static_page = _compat06__render_static_page
render_types_index = _compat09__render_types_index
render_understand_index = _compat06__render_understand_index
resource_access_links = _compat06__resource_access_links
resource_counts = _compat06__resource_counts
resource_link = _compat06__resource_link
safe_http_url = _compat06__safe_http_url
topic_link = _compat06__topic_link
validate_reading_layer = _compat06__validate_reading_layer
write_route = _compat06__write_route

# ---- command-line entrypoint ----
if __name__ == '__main__':
    destination = build()
    print(f'Built The Neurodiverse Oracle public site v1.0 candidate at {destination}')
