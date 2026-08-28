# ND Oracle content and navigation v0.8

## Priority

v0.8 prioritises **content breadth and findability**. It is not a visual redesign and it does not introduce an AI answer surface.

The governing product problem is simple: a larger knowledge commons is only useful if a reader can reach relevant material from the problem they actually have, without already knowing the right diagnosis, organisation name or internal object type.

## Corpus target for this release

The v0.8 candidate contains 49 authoritative objects:

- 10 reviewed Concepts;
- 25 reviewed Resources;
- 14 reviewed practical Questions.

The ten new Resource entries add current routes for:

- dyslexia information and support;
- Tourette syndrome information and support;
- learning-disability information and support;
- DLD awareness and adult support;
- built-in device accessibility;
- reasonable adjustments at work in Great Britain;
- Disabled Students' Allowance in England;
- disability-related job-search support in the UK;
- adult dyspraxia/DCD information.

All ten remain claimless Resource listings. First-party service descriptions establish identity, current purpose and access; they are not independent evidence of efficacy, safety, legal entitlement or individual fit.

## Navigation contract

### Primary navigation

Use plain content labels:

- `Questions`
- `Topics`
- `Resources`
- `How it works`
- `About`

The existing `/understand/` and `/resources/` canonical paths remain stable.

### Questions

The Question index must exactly cover the governed Question corpus and group it by ordinary need rather than diagnosis:

1. Everyday life & technology
2. Work & study
3. Finding information & support
4. Games & downtime
5. Anxiety & self-management

Every governed Question must appear in exactly one group. The homepage may feature a smaller set, but it must route clearly to the complete Question index.

### Resources

Resource browsing exposes:

- All resources
- Tools & practical help
- Games
- Books & media
- Support & organisations

`Tools & practical help` intentionally includes more than software: practical guides, accommodations, education/work resources and products already share the existing tool-oriented category route.

### Cross-navigation

Pages must not become dead ends as the corpus grows:

- Topic pages show practical Questions that reference the Topic and reviewed Resources linked to it.
- Resource pages show governed Questions that lead to the Resource.
- Question pages continue to link the governed Concepts and Resources used by their bounded synthesis.

This creates a navigable loop:

`ordinary need → Question → Topic/Resource → related Question/Resource`

## Public route contract

The v0.8 candidate contains 62 canonical indexable routes:

- the inherited v0.6 static/topic/collection routes;
- all 25 current Resource detail routes;
- `/books-media/`;
- `/questions/`;
- all 14 current Question detail routes.

The production verifier derives Resource and Question detail routes from the authoritative corpus so future content growth cannot silently leave new objects outside the live contract.

The accepted v0.7 five-Question verifier remains available as a frozen compatibility contract. v0.8 adds its own full-corpus content/navigation contract.

## Non-goals

v0.8 does not add:

- visual redesign;
- free-text question submission;
- AI/chat answers;
- recommendation scoring or personalised ranking;
- accounts or query storage;
- analytics or profiling;
- new efficacy, safety or diagnostic claims;
- a schema version change.

## Acceptance criteria

- all 49 authoritative objects validate and all governed references resolve;
- all ten new Resources remain reviewed and claimless;
- all 14 Questions are reachable from the grouped Question index;
- the Question group configuration exactly covers the authoritative Question corpus;
- all 25 Resources and 14 Questions have canonical detail routes and sitemap entries;
- `/books-media/` is a canonical browse route;
- Topic, Resource and Question pages expose the required cross-links;
- the direct build and verifier entrypoints remain regression-tested;
- the v0.8 verifier accepts the actual locally generated site before production deployment;
- production remains v0.7 until a separate exact-main deployment is authorised and live verification passes.
