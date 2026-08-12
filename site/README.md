# The Neurodiverse Oracle — public site v0.5

This directory contains the presentation layer for the public ND Oracle site.

The v0.5 pass keeps the evidence model unchanged while making the ten-topic public corpus easier to enter and read. The generated Understand pages still come from the authoritative knowledge objects in `objects/concepts/`; the website does not maintain a second copy of claim text, sources, uncertainties or perspectives.

## Current public journey

A visitor can:

1. start from one ordinary-language homepage question for each of the ten current topics;
2. browse all ten reviewed topics under `/understand/`;
3. read a deliberately simple first explanation before the more precise evidence summary;
4. see when each topic was last reviewed;
5. understand what the confidence labels mean;
6. open the evidence and uncertainty behind individual statements only when wanted;
7. inspect different perspectives, related topics, sources and provenance;
8. report accessibility, wording, evidence or broken-page problems through `/feedback/` without a form or tracking on this site;
9. recover from a bad URL through a useful `404.html` page;
10. discover indexable routes through `sitemap.xml` and `robots.txt`.

Primary navigation contains only the core reading destinations:

- `/understand/`
- `/how-it-works/`
- `/about/`

Accessibility, feedback and privacy are available in the footer.

The old `/tools/`, `/games/`, `/resources/`, `/community/` and `/oracle/` routes remain as non-indexed compatibility pages so existing links do not become dead ends. They are deliberately absent from primary navigation and the sitemap until there is useful content to put there.

## Reading-layer contract

The authoritative evidence record and the public first-read layer have different jobs.

- Authoritative concept summaries stay precise and traceable.
- `SIMPLE_EXPLANATIONS` in `scripts/build_site.py` supplies the first-read wording.
- `COMMON_QUESTIONS` supplies the homepage entry route.
- The build fails unless both sets exactly cover the authoritative concept corpus, with one homepage question per topic.

This means future topic expansion cannot silently create a technically valid page with no human-oriented entry route.

## Confidence labels

`/how-it-works/` explains all confidence values supported by the v0.1 concept schema: high, moderate, low, contested and not applicable. A confidence value applies to the exact statement beside it rather than to a person, topic or source. High confidence is not presented as certainty, and `not_applicable` is not presented as an escape from evidence assessment.

## Review dates

Each topic page exposes `provenance.last_reviewed` in ordinary language near the top of the page. The full provenance block remains available lower down. A review date describes the freshness of ND Oracle's review; it is not a claim that no newer evidence exists.

## Feedback boundary

`/feedback/` does not add a local form, account or tracking endpoint. It links to the repository's public GitHub issue tracker and warns readers not to include private health information or personal details. The lack of a private feedback channel is explicitly disclosed as a current limitation.

## Design stance

The public site remains deliberately calm and reading-first:

- semantic HTML;
- system fonts;
- restrained colours;
- visible keyboard focus;
- reading-width content;
- ordinary-language entry points;
- native `<details>` controls for progressive disclosure;
- no required JavaScript;
- no empty feature catalogue presented as a finished product.

## Build

```sh
python scripts/build_site.py
```

The generated site is written to `dist/` and is intentionally not committed.

## Security and privacy defaults

The current site remains static and deliberately narrow:

- no JavaScript;
- no forms;
- no accounts;
- no analytics or advertising trackers;
- no personal-data collection by the generated site;
- no Pages Functions or other server-side runtime;
- restrictive Content Security Policy;
- anti-framing, MIME-sniffing, referrer, permissions and cross-origin headers;
- HSTS emitted with the static deployment headers.

The feedback link leaves the site for GitHub. Any future private feedback channel or feature that stores user data requires a separate privacy and threat-model review.

## Search decision

A separate search runtime is still not justified while the public corpus contains ten topic pages. The homepage now provides a natural-language route to every topic, and `/understand/` exposes the complete corpus in one scan.

Search should be introduced when the corpus becomes large enough that question-led navigation and browsing stop being efficient, rather than adding a JavaScript or runtime dependency in advance of that need.

## Cloudflare Pages release contract

The intended hosting target remains Cloudflare Pages using Direct Upload of the already-built `dist/` directory. The repository is authoritative; Cloudflare receives generated static assets only.

Before any deployment:

1. verify the intended release commit is the exact current `main` commit;
2. require a clean working tree;
3. run the repository validator and complete test suite;
4. build `dist/` from that exact commit;
5. inspect the generated site and security headers;
6. verify the pinned Wrangler version and deployment flags;
7. publish only through the guarded manual production workflow.

The deployment CLI is version-pinned. Updating the Wrangler version is a release-tooling change and must be reviewed rather than silently inherited from `npx` latest.

## Boundary

This v0.5 presentation pass does not change authoritative knowledge claims, create accounts, collect community data, add analytics, introduce an Oracle chatbot, or represent the site as clinical guidance.
