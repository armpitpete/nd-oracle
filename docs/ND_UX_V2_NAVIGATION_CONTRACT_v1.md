# ND-UX-V2 Navigation Contract v1

Date: 2026-09-23  
Status: **FROZEN — PHASE 1**  
Authority: presentation/navigation only  
PR: #168

## Release-blocking acceptance rule

> **A new visitor can tell that ND Oracle contains things such as conditions, books, games and apps, and can reach them without first learning what “Resources”, “Topics”, “Needs” or similar internal categories mean.**

This applies to desktop and narrow/mobile layouts. Automated route checks are necessary but cannot by themselves satisfy the human usability gate.

## Visitor model

The visitor sees concrete things and practical contexts. ND Oracle's internal taxonomy remains implementation machinery.

### Primary categories

| Group | Visitor label | Purpose | Target |
| --- | --- | --- | --- |
| Browse things | **Conditions** | Learn about named conditions and condition-oriented explanations. | `/conditions/` |
| Browse things | **Books** | Find governed book Resources. | `/books/` |
| Browse things | **Games** | Find governed game Resources. | `/games/` |
| Browse things | **Apps & tools** | Find governed apps, software and practical tools. | `/apps-tools/` |
| Browse things | **Organisations & peer groups** | Find organisations, communities and peer-support routes. | `/organisations/` |
| Get help with life | **Work & education** | Find work, study, adjustment and education support. | `/work-education/` |
| Get help with life | **Health & diagnosis** | Find assessment, diagnosis, healthcare access and health-support routes. | `/health-diagnosis/` |
| Get help with life | **Daily living** | Find practical everyday-life support. | `/daily-living/` |
| Check evidence | **Evidence & research** | Inspect evidence, sources, uncertainty and authority boundaries. | `/evidence/` |

Nine is the hard maximum for prominent category choices. They are not visually equal: the five concrete "Browse things" categories form the first recognition group; practical-life categories form a second group; Evidence & research is a quieter authority route.

### Category boundaries

**Conditions** is for learning about a named condition or condition-oriented explanation. It is not a diagnostic tool. **Health & diagnosis** is for assessment, diagnosis processes, healthcare access and clinical support.

**Books, Games, Apps & tools, Organisations & peer groups** are resource-kind views over existing governed Resources. They do not create duplicate Resource authority.

**Work & education** and **Daily living** are practical/context routes. They may surface existing Questions and Resources without cloning them.

**Evidence & research** exposes authority and evidence. It does not rank products or act as a recommendation surface.

If an item belongs in more than one visitor route, ND Oracle keeps one governed object and exposes deterministic links from each applicable route.

## Secondary utilities

Secondary utilities are **Search**, **A–Z**, **Browse everything**, and **Not sure where to start?** They are visually subordinate to the primary categories.

- **Search** → `/find/`;
- **A–Z** → `/a-z/`;
- **Browse everything** → `/types/`;
- **Not sure where to start?** → `/start/` (Phase 2 implementation target).

The uncertainty route is capped at four concrete choices:

1. Something about me
2. Something I need help with
3. Something to read, watch or use
4. Somewhere or someone that can help

It must not grow into another full taxonomy.

## Internal terminology boundary

`Resources`, `Topics`, `Needs` and `Questions` are internal/specialist information-architecture terms. `Find` is a utility concept.

These routes may remain for compatibility and specialist browsing, but **none may be prerequisite vocabulary for reaching ordinary content**. Vague replacements such as "Explore" or "Discover" must not become primary category labels.

The hierarchy is:

**Primary content categories → secondary utilities → deeper/internal browsing tools.**

## Direct reachability

The target pattern is:

**Home → category → item**

An avoidable chain such as:

**Home → Resources → catalogue → type → item**

fails the contract when a direct category route can expose the same governed item safely.

Every category landing page must identify the category clearly, provide a clear route Home, and keep Search and A–Z reachable.

## Visual hierarchy

The existing V2.5 rules remain authoritative:

- calm colour/surface changes mark real section boundaries and are paired with non-colour cues;
- retain the readable base text size;
- use typographic weight and headings to communicate importance;
- keep related content in the same visual field where practical;
- do not use whitespace to split mutually dependent information;
- do not regress to a generic hero or card wall;
- communicate what kinds of content exist before explaining project methodology.

Recognition imagery remains secondary to the category label.

> **Render a cleared visual when it materially helps the user recognise, distinguish or understand the resource.**

Rights/provenance remain fail-closed. Imagery is recognition/navigation material, never Evidence, endorsement or ranking authority. The publisher-supplied *A Kind of Spark* cover remains governed by its recorded no-alteration and editorial re-review conditions.

## Protected authority boundary

Phase 1 changes presentation/navigation authority only. It must not modify:

- governed Resource, Concept, Question, Claim, Evidence or source content;
- schemas or discovery/ranking policy;
- provenance or jurisdiction authority;
- `contracts/current-production.json`;
- production deployment workflow, DNS, Cloudflare project/configuration, secrets or domains.

A discovered content problem is opened separately rather than silently repaired inside navigation work.

## Machine acceptance

Repository tests bind this contract by requiring:

- the exact release-blocking acceptance rule;
- the exact nine visitor-facing categories and grouping;
- the four secondary utilities;
- the four-choice uncertainty-route cap;
- separation of internal terminology from primary labels;
- the direct-reachability rule;
- protected boundaries;
- the existing desktop and narrow Home screenshot capture in the visual-evidence workflow;
- the human-test question and outcome vocabulary.

The tests intentionally do **not** claim that Phase 2 routes already exist. Phase 1 freezes the implementation target; Phase 2 will bind those routes to rendered output.

## Human acceptance

Before the fixed journeys, ask:

> **Without clicking anything, what kinds of things do you think you can find on this website?**

A participant should be able to identify concrete categories such as conditions, books, games or apps without being taught ND Oracle terminology.

Then test direct attempts to find one condition, one book, one game, one app/tool, one organisation/peer group and one practical-help route.

For the participant-facing record use only:

- **Found it**
- **Confusing**
- **Couldn't find it**

The moderator may retain the existing detailed journey fields and map these outcomes to PASS/PARTIAL/FAIL for release evidence.

Aesthetic preference alone does not block release. Repair only demonstrated failures such as wrong first choice, category ambiguity, excessive backtracking, hidden content, loss of orientation, inaccessible controls or task failure.

## Phase 1 exit

Phase 1 is complete when this contract and its machine-readable companion are committed, regression-bound, reflected in V2 authority/completion documents, and validated at one exact candidate SHA. Actual Home/category implementation is Phase 2.
